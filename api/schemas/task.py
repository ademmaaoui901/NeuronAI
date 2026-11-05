"""
AI Production Agent - Task Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.task import TaskStatus, TaskType, TaskPriority


class TaskBase(BaseModel):
    task_type: TaskType
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    user_id: int
    status: TaskStatus
    progress: int
    result: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    celery_task_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    progress: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class TaskStatusResponse(BaseModel):
    task_id: int
    status: TaskStatus
    progress: int
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
