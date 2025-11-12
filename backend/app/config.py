"""
Configuration settings for the Piper Alpha Training System backend.
Loads environment variables and defines application constants.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./piper_alpha.db"  # Default to SQLite for development
    
    # JWT Authentication
    SECRET_KEY: str = "dev-secret-key-change-in-production"  # MUST be changed in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 30
    
    # API Configuration
    API_TITLE: str = "Piper Alpha Training API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API for tracking Piper Alpha VR training progress"
    
    # CORS Origins (for frontend)
    CORS_ORIGINS: list = ["http://localhost:8501", "http://127.0.0.1:8501"]
    
    class Config:
        env_file = "../.env"  # Look for .env in parent directory (project root)
        env_file_encoding = 'utf-8'
        case_sensitive = True
        # Railway will inject env vars directly, so .env is optional


# Application constants
VALID_CHAPTERS = [
    "Briefing Room",
    "Arrival on Piper Alpha",
    "Maintenance Area",
    "Precursor to Disaster",
    "Explosion Simulation",
    "Escape Aftermath",
    "Debrief"
]

VALID_STATUSES = ["Completed", "Pending", "Not Completed"]
VALID_ROLES = ["Trainee", "Admin"]

# Score range
MIN_SCORE = 0
MAX_SCORE = 10

# Initialize settings
settings = Settings()

