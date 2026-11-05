"""
AI Production Agent - Audio Celery Tasks
"""

from celery import shared_task
from typing import Dict, Any
import os

from config.settings import settings
from core.agent import agent


@shared_task(bind=True, max_retries=3)
def speech_to_text_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Convert speech to text in background"""
    try:
        response = agent.execute(
            task_type="audio_stt",
            parameters=parameters
        )
        
        if response.status == "error":
            raise Exception(response.error)
        
        return {
            "status": "success",
            "text": response.content,
            "language": parameters.get("language"),
            "model": response.model
        }
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def text_to_speech_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Convert text to speech in background"""
    try:
        response = agent.execute(
            task_type="audio_tts",
            parameters=parameters
        )
        
        if response.status == "error":
            raise Exception(response.error)
        
        audio_data = response.content
        
        return {
            "status": "success",
            "audio_path": audio_data["audio_path"],
            "audio_url": audio_data["audio_url"],
            "sampling_rate": audio_data.get("sampling_rate"),
            "model": response.model
        }
    except Exception as e:
        self.retry(exc=e, countdown=60)
