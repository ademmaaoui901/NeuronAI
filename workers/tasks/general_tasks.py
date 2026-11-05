"""
AI Production Agent - General Celery Tasks
"""

from celery import shared_task
from celery.schedules import crontab
import os
import shutil
from datetime import datetime, timedelta

from config.settings import settings


@shared_task
ndef cleanup_temp_files():
    """Clean up temporary files"""
    try:
        # Clean up uploads older than 1 day
        uploads_dir = settings.UPLOADS_DIR
        if os.path.exists(uploads_dir):
            now = datetime.now()
            for filename in os.listdir(uploads_dir):
                file_path = os.path.join(uploads_dir, filename)
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if now - file_time > timedelta(days=1):
                        os.remove(file_path)
        
        # Clean up cache older than 1 hour
        cache_dir = settings.CACHE_DIR
        if os.path.exists(cache_dir):
            now = datetime.now()
            for filename in os.listdir(cache_dir):
                file_path = os.path.join(cache_dir, filename)
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if now - file_time > timedelta(hours=1):
                        os.remove(file_path)
        
        return {"status": "success", "message": "Temp files cleaned up"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@shared_task
ndef check_models():
    """Check if models are loaded and available"""
    try:
        from core.agent import agent
        
        # Check if models are loaded
        if not agent._models_loaded:
            agent._load_models()
        
        # Check each model
        model_status = {}
        for model_name, model_data in agent.models.items():
            model_status[model_name] = "loaded"
        
        return {
            "status": "success",
            "models": model_status,
            "total_models": len(agent.models)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
