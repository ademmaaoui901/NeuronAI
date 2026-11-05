"""
AI Production Agent - Task Model
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..database import Base
import enum


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskType(str, enum.Enum):
    CODE_GENERATION = "code_generation"
    CODE_FIX = "code_fix"
    CODE_EXPLAIN = "code_explain"
    IMAGE_GENERATION = "image_generation"
    IMAGE_EDIT = "image_edit"
    VIDEO_GENERATION = "video_generation"
    AUDIO_STT = "audio_stt"
    AUDIO_TTS = "audio_tts"
    CHAT = "chat"
    SUMMARIZE = "summarize"
    TRANSLATE = "translate"
    CUSTOM = "custom"


class Task(Base):
    """Task model for storing background tasks"""
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    
    # Task information
    task_type = Column(Enum(TaskType), nullable=False)
    title = Column(String(200))
    description = Column(Text)
    
    # Parameters and results
    parameters = Column(JSONB, default={})
    result = Column(JSONB, default={})
    error = Column(Text)
    
    # Status
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, index=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    progress = Column(Integer, default=0)
    
    # Celery task ID
    celery_task_id = Column(String(64), unique=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", backref="tasks")
    
    def __repr__(self):
        return f"<Task(id={self.id}, type={self.task_type}, status={self.status})>"
