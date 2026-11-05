"""
AI Production Agent - Conversation Model
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..database import Base
import enum


class MessageType(str, enum.Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Conversation(Base):
    """Conversation model for storing chat history"""
    
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    
    # Conversation metadata
    title = Column(String(200))
    model = Column(String(50), default="mistral")
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=4096)
    
    # Messages
    messages = Column(JSONB, default=[])
    
    # Context
    context = Column(JSONB, default={})
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="conversations")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, title='{self.title}')>"
