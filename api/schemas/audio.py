"""
AI Production Agent - Audio Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional


class AudioSTTRequest(BaseModel):
    audio_file: str = Field(..., description="Path to audio file")
    language: Optional[str] = Field(default="auto", description="Language of the audio")
    model: Optional[str] = Field(default="whisper", description="Model to use")


class AudioTTSRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    language: Optional[str] = Field(default="auto", description="Language of the text")
    speaker: Optional[str] = Field(default="default", description="Speaker voice")
    model: Optional[str] = Field(default="xtts", description="Model to use")


class AudioResponse(BaseModel):
    audio_url: str
    audio_path: str
    text: Optional[str] = None
    language: Optional[str] = None
    model: str
    duration: Optional[float] = None
