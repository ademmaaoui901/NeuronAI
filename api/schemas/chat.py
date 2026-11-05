"""
AI Production Agent - Chat Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class Message(BaseModel):
    role: str = Field(..., description="Role of the message: system, user, assistant, tool")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    messages: List[Message] = Field(default_factory=list)
    model: Optional[str] = Field(default="mistral", description="Model to use")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=4096, ge=1, le=8192)
    stream: Optional[bool] = Field(default=False, description="Whether to stream the response")


class ChatResponse(BaseModel):
    message: Message
    model: str
    finish_reason: Optional[str] = None
    usage: Dict[str, int] = Field(default_factory=dict)


class ChatStreamResponse(BaseModel):
    chunk: str
    model: str
    finish_reason: Optional[str] = None
