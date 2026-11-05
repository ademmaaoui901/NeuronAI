"""
AI Production Agent - User Model
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from ..database import Base


class User(Base):
    """User model for storing user information"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    
    # API Key for authentication
    api_key = Column(String(64), unique=True, index=True)
    api_key_name = Column(String(50))
    
    # Preferences
    preferences = Column(JSONB, default={})
    
    # Quota and Usage
    max_tokens = Column(Integer, default=100000)
    used_tokens = Column(Integer, default=0)
    max_images = Column(Integer, default=1000)
    used_images = Column(Integer, default=0)
    max_videos = Column(Integer, default=100)
    used_videos = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
