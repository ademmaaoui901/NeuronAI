"""
AI Production Agent - Code Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class CodeRequest(BaseModel):
    description: str = Field(..., description="Description of the code to generate")
    language: str = Field(default="python", description="Programming language")
    action: str = Field(default="generate", description="Action: generate, fix, explain")
    code: Optional[str] = Field(default=None, description="Code to fix or explain")
    error: Optional[str] = Field(default=None, description="Error message for fixing")
    project_name: Optional[str] = Field(default=None, description="Project name for saving")
    max_tokens: Optional[int] = Field(default=4096, ge=1, le=8192)
    temperature: Optional[float] = Field(default=0.5, ge=0, le=2)


class CodeResponse(BaseModel):
    code: str
    language: str
    action: str
    file_path: Optional[str] = None
    explanation: Optional[str] = None
    error: Optional[str] = None
    model: str
    usage: Dict[str, int] = Field(default_factory=dict)
