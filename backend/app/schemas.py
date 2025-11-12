"""
Pydantic schemas for request/response validation and data modeling.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Union
from datetime import datetime
from .config import VALID_CHAPTERS, VALID_STATUSES, VALID_ROLES, MIN_SCORE, MAX_SCORE


# ============ User Schemas ============

class UserCreate(BaseModel):
    """Schema for user registration request."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    role: str = Field(..., description="Role must be 'Trainee' or 'Admin'")
    trainee_name: str = Field(..., min_length=1, description="Trainee name is required")
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v not in VALID_ROLES:
            raise ValueError(f"Role must be one of {VALID_ROLES}")
        return v


class UserLogin(BaseModel):
    """Schema for user login request."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user data response."""
    email: str
    role: str
    trainee_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Performance Data Schemas ============

class ChapterData(BaseModel):
    """Schema for individual chapter performance data."""
    chapter: str = Field(..., description="Chapter name (must be one of the valid chapters)")
    score: Union[int, str] = Field(..., description="Score (0-10) or 'NA' for not attempted")
    status: str = Field(..., description="Status: Completed, Pending, or Not Completed")
    
    @field_validator('chapter')
    @classmethod
    def validate_chapter(cls, v):
        if v not in VALID_CHAPTERS:
            raise ValueError(f"Chapter must be one of {VALID_CHAPTERS}")
        return v
    
    @field_validator('score')
    @classmethod
    def validate_score(cls, v):
        if isinstance(v, str):
            if v != "NA":
                raise ValueError("Score must be an integer (0-10) or 'NA'")
            return v
        if isinstance(v, int):
            if v < MIN_SCORE or v > MAX_SCORE:
                raise ValueError(f"Score must be between {MIN_SCORE} and {MAX_SCORE}")
            return v
        raise ValueError("Score must be an integer (0-10) or 'NA'")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v not in VALID_STATUSES:
            raise ValueError(f"Status must be one of {VALID_STATUSES}")
        return v


class PerformanceSubmit(BaseModel):
    """Schema for performance data submission from Unity game."""
    email: EmailStr = Field(..., description="Email of the user")
    chapters: List[ChapterData] = Field(..., description="List of chapter performance data")
    
    @field_validator('chapters')
    @classmethod
    def validate_chapters_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError("At least one chapter must be provided")
        return v


class PerformanceResponse(BaseModel):
    """Schema for performance data response."""
    id: int
    email: str
    session_timestamp: datetime
    chapter_data: List[dict]
    
    class Config:
        from_attributes = True


class PerformanceSubmitResponse(BaseModel):
    """Schema for successful performance submission response."""
    message: str
    session_id: int
    session_timestamp: datetime


# ============ Error Schemas ============

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str

