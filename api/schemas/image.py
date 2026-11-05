"""
AI Production Agent - Image Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional


class ImageRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt for image generation")
    negative_prompt: Optional[str] = Field(default="", description="Negative prompt")
    width: int = Field(default=1024, ge=256, le=2048)
    height: int = Field(default=1024, ge=256, le=2048)
    num_inference_steps: int = Field(default=30, ge=10, le=100)
    guidance_scale: float = Field(default=7.5, ge=1, le=20)
    model: Optional[str] = Field(default="sdxl", description="Model to use")


class ImageResponse(BaseModel):
    image_url: str
    image_path: str
    prompt: str
    width: int
    height: int
    model: str
    usage: dict = Field(default_factory=dict)
