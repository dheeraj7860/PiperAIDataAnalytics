"""
Main FastAPI application for Piper Alpha Training Progress Tracking System.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
import os
import tempfile

from . import models, schemas, crud, auth
from .database import get_db, init_db, engine
from .config import settings

# Initialize FastAPI app with metadata
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    """Initialize database tables on application startup."""
    init_db()
    print(f">>> {settings.API_TITLE} v{settings.API_VERSION} started successfully!")


# ============ Health Check Endpoint ============

@app.get("/", tags=["Health"])
def read_root():
    """
    Health check endpoint to verify API is running.
    """
    return {
        "message": "Piper Alpha Training API is running",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }


# ============ Authentication Endpoints ============

@app.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
    summary="Register a new user",
    description="Register a new trainee or admin user. Email must be unique."
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    - **email**: Unique email address
    - **password**: Password (minimum 8 characters)
    - **role**: Must be "Trainee" or "Admin"
    - **trainee_name**: Full name of the trainee
    """
    # Check if user already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    return crud.create_user(db=db, user=user)


@app.post(
    "/login",
    response_model=schemas.Token,
    tags=["Authentication"],
    summary="Login to get access token",
    description="Authenticate with email and password to receive JWT access token."
)
def login(
    user_login: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password to receive JWT access token.
    
    - **email**: Registered email address
    - **password**: User password
    
    Returns JWT access token valid for 30 days.
    """
    user = auth.authenticate_user(db, user_login.email, user_login.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get(
    "/me",
    response_model=schemas.UserResponse,
    tags=["Authentication"],
    summary="Get current user info",
    description="Get information about the currently authenticated user."
)
def read_users_me(
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Get current authenticated user's information.
    Requires valid JWT token in Authorization header.
    """
    return current_user


# ============ Performance Data Endpoints ============

@app.post(
    "/performance",
    response_model=schemas.PerformanceSubmitResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Performance Data"],
    summary="Submit performance data (No Auth Required)",
    description="Submit training performance data from Unity game. Auto-fills missing chapters."
)
def submit_performance(
    performance: schemas.PerformanceSubmit,
    db: Session = Depends(get_db)
):
    """
    Submit performance data for a training session (called by Unity game).
    
    - **email**: Email of the user (must exist in database)
    - **chapters**: List of chapter performance data
    
    Missing chapters will be automatically filled with score="NA" and status="Not Completed".
    Returns session_id for future reference.
    
    **No authentication required** - Unity game can submit data directly.
    """
    # Verify user exists
    user = crud.get_user_by_email(db, email=performance.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with email: {performance.email}"
        )
    
    # Convert Pydantic models to dictionaries
    chapter_data_dicts = [chapter.model_dump() for chapter in performance.chapters]
    
    # Create performance record (auto-fills missing chapters)
    db_performance = crud.create_performance_data(
        db=db,
        email=performance.email,
        chapter_data=chapter_data_dicts
    )
    
    return {
        "message": "Performance data submitted successfully",
        "session_id": db_performance.id,
        "session_timestamp": db_performance.session_timestamp
    }


@app.get(
    "/performance/{email}",
    response_model=List[schemas.PerformanceResponse],
    tags=["Performance Data"],
    summary="Get user's performance data (Auth Required)",
    description="Get all performance sessions for a specific user. Requires authentication."
)
def get_performance(
    email: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Get all performance data for a specific user.
    
    **Authentication required.**
    Users can only view their own data unless they are Admin.
    
    - **email**: Email of the user whose data to retrieve
    """
    # Check authorization: users can only see their own data, admins can see all
    if current_user.email != email and current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's data"
        )
    
    # Verify the requested user exists
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with email: {email}"
        )
    
    # Get performance data
    performance_data = crud.get_user_performance_data(db, email=email)
    
    if not performance_data:
        return []  # Return empty list if no data
    
    return performance_data


# ============ PDF Report Endpoints ============

@app.get(
    "/download-report/{session_id}",
    tags=["Reports"],
    summary="Download PDF report (Auth Required)",
    description="Generate and download PDF report for a specific training session."
)
def download_report(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Generate and download PDF report for a specific session.
    
    **Authentication required.**
    Users can only download their own reports unless they are Admin.
    
    - **session_id**: ID of the performance session
    """
    # Get performance data
    performance = crud.get_performance_by_session_id(db, session_id=session_id)
    
    if not performance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Performance session not found with ID: {session_id}"
        )
    
    # Check authorization
    if current_user.email != performance.email and current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to download this report"
        )
    
    # Get user details
    user = crud.get_user_by_email(db, email=performance.email)
    
    # Generate PDF (import here to avoid circular imports)
    from .pdf_generator import generate_course_report
    
    user_data = {
        "email": user.email,
        "trainee_name": user.trainee_name,
        "role": user.role
    }
    
    session_data = {
        "session_id": performance.id,
        "session_timestamp": performance.session_timestamp,
        "chapter_data": performance.chapter_data
    }
    
    pdf_buffer = generate_course_report(user_data, session_data)
    
    # Return PDF as streaming response
    filename = f"PiperAlpha_Report_{user.trainee_name.replace(' ', '_')}_{performance.session_timestamp.strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Reset buffer position to beginning
    pdf_buffer.seek(0)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


# ============ Admin Endpoints ============

@app.get(
    "/admin/users",
    response_model=List[schemas.UserResponse],
    tags=["Admin"],
    summary="Get all users (Admin Only)",
    description="Get list of all registered users. Admin access required."
)
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin_user)
):
    """
    Get all registered users (Admin only).
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users


@app.get(
    "/admin/all-sessions",
    response_model=List[schemas.PerformanceResponse],
    tags=["Admin"],
    summary="Get all performance sessions (Admin Only)",
    description="Get all performance sessions across all users. Admin access required."
)
def get_all_sessions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin_user)
):
    """
    Get all performance sessions across all users (Admin only).
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    sessions = crud.get_all_performance_data(db, skip=skip, limit=limit)
    return sessions

