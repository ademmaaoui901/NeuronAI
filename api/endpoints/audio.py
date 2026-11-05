"""
AI Production Agent - Audio Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import os
import uuid

from ..database import get_db
from ..models.user import User
from ..schemas.audio import AudioSTTRequest, AudioTTSRequest, AudioResponse
from core.security import get_current_user
from core.agent import agent
from config.settings import settings

router = APIRouter()


@router.post(
    "/stt",
    response_model=AudioResponse,
    summary="Speech to Text",
    response_description="Convert speech to text"
)
async def speech_to_text(
    request: AudioSTTRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> AudioResponse:
    """Convert speech to text using Whisper"""
    
    # Check if file exists
    if not os.path.exists(request.audio_file):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audio file not found: {request.audio_file}"
        )
    
    # Execute STT task
    response = await agent.execute(
        task_type="audio_stt",
        parameters={
            "audio_file": request.audio_file,
            "language": request.language,
            "model": request.model
        }
    )
    
    if response.status == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response.error
        )
    
    return AudioResponse(
        text=response.content,
        language=request.language,
        model=response.model
    )


@router.post(
    "/stt/upload",
    response_model=AudioResponse,
    summary="Speech to Text (Upload)",
    response_description="Upload audio file and convert to text"
)
async def speech_to_text_upload(
    audio_file: UploadFile = File(...),
    language: Optional[str] = "auto",
    model: Optional[str] = "whisper",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> AudioResponse:
    """Upload audio file and convert to text"""
    
    # Save uploaded file temporarily
    temp_path = os.path.join(settings.UPLOADS_DIR, f"{uuid.uuid4()}.wav")
    os.makedirs(settings.UPLOADS_DIR, exist_ok=True)
    
    try:
        # Save the uploaded file
        with open(temp_path, 'wb') as buffer:
            buffer.write(await audio_file.read())
        
        # Execute STT task
        response = await agent.execute(
            task_type="audio_stt",
            parameters={
                "audio_file": temp_path,
                "language": language,
                "model": model
            }
        )
        
        if response.status == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=response.error
            )
        
        return AudioResponse(
            text=response.content,
            language=language,
            model=response.model
        )
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.post(
    "/tts",
    response_model=AudioResponse,
    summary="Text to Speech",
    response_description="Convert text to speech"
)
async def text_to_speech(
    request: AudioTTSRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> AudioResponse:
    """Convert text to speech using XTTS"""
    
    # Execute TTS task
    response = await agent.execute(
        task_type="audio_tts",
        parameters={
            "text": request.text,
            "language": request.language,
            "speaker": request.speaker,
            "model": request.model
        }
    )
    
    if response.status == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response.error
        )
    
    audio_data = response.content
    
    return AudioResponse(
        audio_url=audio_data["audio_url"],
        audio_path=audio_data["audio_path"],
        sampling_rate=audio_data.get("sampling_rate"),
        model=response.model
    )
