"""
AI Production Agent - Endpoints Package
"""

from .health import router as health_router
from .users import router as users_router
from .chat import router as chat_router
from .code import router as code_router
from .image import router as image_router
from .video import router as video_router
from .audio import router as audio_router
from .tasks import router as tasks_router

__all__ = [
    "health_router", "users_router", "chat_router", 
    "code_router", "image_router", "video_router", 
    "audio_router", "tasks_router"
]
