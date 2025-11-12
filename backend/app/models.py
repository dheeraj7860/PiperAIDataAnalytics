"""
SQLAlchemy database models for Users and Performance Data.
"""

from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    """
    User model for storing trainee and admin accounts.
    """
    __tablename__ = "users"
    
    email = Column(String, primary_key=True, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "Trainee" or "Admin"
    trainee_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to performance data
    performance_data = relationship("PerformanceData", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role}', name='{self.trainee_name}')>"


class PerformanceData(Base):
    """
    Performance data model for storing training session results.
    Stores chapter-wise performance data as JSON.
    """
    __tablename__ = "performance_data"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, ForeignKey("users.email", ondelete="CASCADE"), nullable=False, index=True)
    session_timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    chapter_data = Column(JSON, nullable=False)  # Stores list of chapter dictionaries
    
    # Relationship to user
    user = relationship("User", back_populates="performance_data")
    
    def __repr__(self):
        return f"<PerformanceData(id={self.id}, email='{self.email}', timestamp='{self.session_timestamp}')>"

