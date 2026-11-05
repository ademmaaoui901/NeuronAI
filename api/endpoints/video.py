"""
AI Production Agent - Video Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import os
import uuid

from ..database import get_db
from ..models.user import User
from core.security import get_current_user
from core.agent import agent
from config.settings import settings

router = APIRouter()


@router.post(
    "/generate",
    summary="Generate video",
    response_description="Generate a video from images or text"
)
async def generate_video(
    prompt: Optional[str] = None,
    images: Optional[List[UploadFile]] = None,
    duration: Optional[int] = 5,
    fps: Optional[int] = 24,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Generate a video from images or text"""
    
    temp_dir = os.path.join(settings.UPLOADS_DIR, f"video_{uuid.uuid4()}")
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Save uploaded images
        image_paths = []
        if images:
            for img in images:
                img_path = os.path.join(temp_dir, f"{uuid.uuid4()}.png")
                with open(img_path, 'wb') as buffer:
                    buffer.write(await img.read())
                image_paths.append(img_path)
        
        # Execute video generation task
        response = await agent.execute(
            task_type="video_generate",
            parameters={
                "prompt": prompt,
                "image_paths": image_paths,
                "duration": duration,
                "fps": fps
            }
        )
        
        if response.status == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=response.error
            )
        
        # For now, return a message
        # Full video generation requires Stable Video Diffusion
        return {
            "status": "success",
            "message": "Video generation is not yet fully implemented",
            "note": "This feature requires Stable Video Diffusion model which needs significant GPU resources"
        }
    finally:
        # Clean up temp directory
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
