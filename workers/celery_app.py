"""
AI Production Agent - Celery Application
"""

from celery import Celery
from celery.schedules import crontab
from config.settings import settings

# Create Celery app
celery_app = Celery(
    "ai_agent_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["workers.tasks.code_tasks", "workers.tasks.image_tasks", "workers.tasks.video_tasks", "workers.tasks.audio_tasks"]
)

# Configure Celery
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Performance settings
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=100,
    worker_max_memory_per_child=1000000,  # 1GB
    
    # Result settings
    result_expires=3600,  # 1 hour
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Scheduled tasks
    beat_schedule={
        "cleanup-temp-files": {
            "task": "workers.tasks.general_tasks.cleanup_temp_files",
            "schedule": crontab(hour=0, minute=0)  # Daily at midnight
        },
        "check-models": {
            "task": "workers.tasks.general_tasks.check_models",
            "schedule": crontab(hour=0, minute=30)  # Daily at 12:30 AM
        }
    }
)

# Import tasks to register them
from workers.tasks import code_tasks, image_tasks, video_tasks, audio_tasks, general_tasks
