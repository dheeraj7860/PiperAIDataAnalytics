"""
CRUD (Create, Read, Update, Delete) operations for database models.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from .auth import get_password_hash
from .config import VALID_CHAPTERS


# ============ User CRUD Operations ============

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Get a user by email address.
    
    Args:
        db: Database session
        email: User email
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Create a new user with hashed password.
    
    Args:
        db: Database session
        user: UserCreate schema with user data
        
    Returns:
        Created User object
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        trainee_name=user.trainee_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """
    Get all users (for admin purposes).
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of User objects
    """
    return db.query(models.User).offset(skip).limit(limit).all()


# ============ Performance Data CRUD Operations ============

def create_performance_data(
    db: Session,
    email: str,
    chapter_data: List[dict]
) -> models.PerformanceData:
    """
    Create a new performance data record with auto-filled missing chapters.
    
    Args:
        db: Database session
        email: User email
        chapter_data: List of chapter performance dictionaries
        
    Returns:
        Created PerformanceData object
    """
    # Get list of submitted chapter names
    submitted_chapters = {chapter["chapter"] for chapter in chapter_data}
    
    # Auto-fill missing chapters
    complete_chapter_data = list(chapter_data)
    for chapter in VALID_CHAPTERS:
        if chapter not in submitted_chapters:
            complete_chapter_data.append({
                "chapter": chapter,
                "score": "NA",
                "status": "Not Completed"
            })
    
    # Sort by chapter order in VALID_CHAPTERS
    chapter_order = {chapter: idx for idx, chapter in enumerate(VALID_CHAPTERS)}
    complete_chapter_data.sort(key=lambda x: chapter_order.get(x["chapter"], 999))
    
    db_performance = models.PerformanceData(
        email=email,
        chapter_data=complete_chapter_data
    )
    db.add(db_performance)
    db.commit()
    db.refresh(db_performance)
    return db_performance


def get_user_performance_data(
    db: Session,
    email: str,
    skip: int = 0,
    limit: int = 100
) -> List[models.PerformanceData]:
    """
    Get all performance data for a specific user.
    
    Args:
        db: Database session
        email: User email
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of PerformanceData objects
    """
    return db.query(models.PerformanceData).filter(
        models.PerformanceData.email == email
    ).order_by(
        models.PerformanceData.session_timestamp.desc()
    ).offset(skip).limit(limit).all()


def get_performance_by_session_id(
    db: Session,
    session_id: int
) -> Optional[models.PerformanceData]:
    """
    Get performance data by session ID.
    
    Args:
        db: Database session
        session_id: Session ID (performance data record ID)
        
    Returns:
        PerformanceData object if found, None otherwise
    """
    return db.query(models.PerformanceData).filter(
        models.PerformanceData.id == session_id
    ).first()


def get_all_performance_data(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[models.PerformanceData]:
    """
    Get all performance data across all users (for admin purposes).
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of PerformanceData objects
    """
    return db.query(models.PerformanceData).order_by(
        models.PerformanceData.session_timestamp.desc()
    ).offset(skip).limit(limit).all()

