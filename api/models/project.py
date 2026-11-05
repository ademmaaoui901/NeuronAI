"""
AI Production Agent - Project Model
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..database import Base


class Project(Base):
    """Project model for storing user projects"""
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    
    # Project metadata
    name = Column(String(200), nullable=False)
    description = Column(Text)
    project_type = Column(String(50), default="code")  # code, web, mobile, 3d, etc.
    language = Column(String(50))  # python, javascript, java, etc.
    framework = Column(String(50))  # flask, django, react, etc.
    
    # Project structure
    structure = Column(JSONB, default={})
    files = Column(JSONB, default=[])
    
    # Status
    status = Column(String(50), default="draft")  # draft, in_progress, completed, published
    is_public = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="projects")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', type={self.project_type})>"
