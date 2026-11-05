"""
AI Production Agent - Image Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import os
import uuid

from ..database import get_db
from ..models.user import User
from ..schemas.image import ImageRequest, ImageResponse
from core.security import get_current_user
from core.agent import agent
from config.settings import settings
from PIL import Image

router = APIRouter()


@router.post(
    "/generate",
    response_model=ImageResponse,
    summary="Generate image",
    response_description="Generate an image from a text prompt"
)
async def generate_image(
    request: ImageRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ImageResponse:
    """Generate an image from a text prompt"""
    
    # Execute image generation task
    response = await agent.execute(
        task_type="image_generate",
        parameters={
            "prompt": request.prompt,
            "negative_prompt": request.negative_prompt,
            "width": request.width,
            "height": request.height,
            "num_inference_steps": request.num_inference_steps,
            "guidance_scale": request.guidance_scale,
            "model": request.model
        }
    )
    
    if response.status == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response.error
        )
    
    image_data = response.content
    
    return ImageResponse(
        image_url=image_data["image_url"],
        image_path=image_data["image_path"],
        prompt=request.prompt,
        width=request.width,
        height=request.height,
        model=response.model,
        usage=response.usage
    )


@router.post(
    "/edit",
    response_model=ImageResponse,
    summary="Edit image",
    response_description="Edit an existing image"
)
async def edit_image(
    prompt: str,
    image_file: UploadFile = File(...),
    negative_prompt: Optional[str] = "",
    width: Optional[int] = 1024,
    height: Optional[int] = 1024,
    num_inference_steps: Optional[int] = 30,
    guidance_scale: Optional[float] = 7.5,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ImageResponse:
    """Edit an existing image"""
    
    # Save uploaded image temporarily
    temp_path = os.path.join(settings.UPLOADS_DIR, f"{uuid.uuid4()}.png")
    os.makedirs(settings.UPLOADS_DIR, exist_ok=True)
    
    try:
        # Save the uploaded file
        with open(temp_path, 'wb') as buffer:
            buffer.write(await image_file.read())
        
        # Execute image edit task
        response = await agent.execute(
            task_type="image_edit",
            parameters={
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "width": width,
                "height": height,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "image_path": temp_path
            }
        )
        
        if response.status == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=response.error
            )
        
        image_data = response.content
        
        return ImageResponse(
            image_url=image_data["image_url"],
            image_path=image_data["image_path"],
            prompt=prompt,
            width=width,
            height=height,
            model=response.model,
            usage=response.usage
        )
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.post(
    "/4k",
    response_model=ImageResponse,
    summary="Generate 4K image",
    response_description="Generate a high-quality 4K image"
)
async def generate_4k_image(
    prompt: str,
    negative_prompt: Optional[str] = "",
    num_inference_steps: Optional[int] = 50,
    guidance_scale: Optional[float] = 7.5,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ImageResponse:
    """Generate a 4K (2048x2048 or higher) image"""
    
    # Execute image generation with 4K settings
    response = await agent.execute(
        task_type="image_generate",
        parameters={
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": 2048,
            "height": 2048,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "model": "sdxl"
        }
    )
    
    if response.status == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response.error
        )
    
    image_data = response.content
    
    return ImageResponse(
        image_url=image_data["image_url"],
        image_path=image_data["image_path"],
        prompt=prompt,
        width=2048,
        height=2048,
        model=response.model,
        usage=response.usage
    )
