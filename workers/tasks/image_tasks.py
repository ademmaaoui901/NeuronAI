"""
AI Production Agent - Image Celery Tasks
"""

from celery import shared_task
from typing import Dict, Any
import os
import uuid

from config.settings import settings
from core.agent import agent


@shared_task(bind=True, max_retries=3)
def generate_image_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Generate image in background"""
    try:
        response = agent.execute(
            task_type="image_generate",
            parameters=parameters
        )
        
        if response.status == "error":
            raise Exception(response.error)
        
        image_data = response.content
        
        return {
            "status": "success",
            "image_path": image_data["image_path"],
            "image_url": image_data["image_url"],
            "prompt": parameters.get("prompt"),
            "width": parameters.get("width"),
            "height": parameters.get("height"),
            "model": response.model,
            "usage": response.usage
        }
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def edit_image_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Edit image in background"""
    try:
        response = agent.execute(
            task_type="image_edit",
            parameters=parameters
        )
        
        if response.status == "error":
            raise Exception(response.error)
        
        image_data = response.content
        
        return {
            "status": "success",
            "image_path": image_data["image_path"],
            "image_url": image_data["image_url"],
            "prompt": parameters.get("prompt"),
            "model": response.model,
            "usage": response.usage
        }
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def generate_4k_image_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Generate 4K image in background"""
    try:
        # Set 4K resolution
        parameters["width"] = 2048
        parameters["height"] = 2048
        parameters["num_inference_steps"] = parameters.get("num_inference_steps", 50)
        
        response = agent.execute(
            task_type="image_generate",
            parameters=parameters
        )
        
        if response.status == "error":
            raise Exception(response.error)
        
        image_data = response.content
        
        return {
            "status": "success",
            "image_path": image_data["image_path"],
            "image_url": image_data["image_url"],
            "prompt": parameters.get("prompt"),
            "width": 2048,
            "height": 2048,
            "model": response.model,
            "usage": response.usage
        }
    except Exception as e:
        self.retry(exc=e, countdown=60)
