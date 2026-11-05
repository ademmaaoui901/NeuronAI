"""
AI Production Agent - Health Check Endpoint
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Dict, Any
import psutil
import platform

router = APIRouter()


@router.get("/", summary="Health check", response_description="Check API health status")
async def health_check() -> Dict[str, Any]:
    """Check the health status of the API"""
    
    # System information
    system_info = {
        "system": platform.system(),
        "node_name": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }
    
    # CPU information
    cpu_info = {
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "usage": psutil.cpu_percent(interval=1)
    }
    
    # Memory information
    memory_info = psutil.virtual_memory()
    memory_data = {
        "total": memory_info.total,
        "available": memory_info.available,
        "used": memory_info.used,
        "percent": memory_info.percent
    }
    
    # Disk information
    disk_info = psutil.disk_usage('/')
    disk_data = {
        "total": disk_info.total,
        "used": disk_info.used,
        "free": disk_info.free,
        "percent": disk_info.percent
    }
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "system": system_info,
        "cpu": cpu_info,
        "memory": memory_data,
        "disk": disk_data,
        "message": "AI Production Agent API is running successfully"
    }


@router.get("/simple", summary="Simple health check", response_description="Simple health check endpoint")
async def simple_health_check() -> Dict[str, str]:
    """Simple health check"""
    return {
        "status": "healthy",
        "message": "AI Production Agent API is running"
    }
