"""
AI Production Agent - Tasks Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sql_update
from typing import List, Optional
import uuid

from ..database import get_db
from ..models.user import User
from ..models.task import Task, TaskStatus, TaskType, TaskPriority
from ..schemas.task import TaskCreate, TaskResponse, TaskStatusResponse, TaskUpdate
from core.security import get_current_user
from core.agent import agent

router = APIRouter()


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create task",
    response_description="Create a new background task"
)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
) -> TaskResponse:
    """Create a new background task"""
    
    # Create task in database
    new_task = Task(
        user_id=current_user.id,
        task_type=task_data.task_type,
        title=task_data.title,
        description=task_data.description,
        parameters=task_data.parameters,
        priority=task_data.priority,
        status=TaskStatus.PENDING,
        celery_task_id=str(uuid.uuid4())
    )
    
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    
    # Execute task in background
    background_tasks.add_task(
        _execute_task_in_background,
        task_id=new_task.id,
        task_type=str(new_task.task_type),
        parameters=new_task.parameters,
        db=db
    )
    
    return TaskResponse.from_orm(new_task)


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="List tasks",
    response_description="List all tasks for the current user"
)
async def list_tasks(
    status_filter: Optional[TaskStatus] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[TaskResponse]:
    """List all tasks for the current user"""
    
    query = select(Task).where(Task.user_id == current_user.id)
    
    if status_filter:
        query = query.where(Task.status == status_filter)
    
    query = query.order_by(Task.created_at.desc()).limit(limit).offset(offset)
    
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    return [TaskResponse.from_orm(task) for task in tasks]


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task",
    response_description="Get a specific task by ID"
)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> TaskResponse:
    """Get a specific task by ID"""
    
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return TaskResponse.from_orm(task)


@router.get(
    "/{task_id}/status",
    response_model=TaskStatusResponse,
    summary="Get task status",
    response_description="Get the status of a specific task"
)
async def get_task_status(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> TaskStatusResponse:
    """Get the status of a specific task"""
    
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return TaskStatusResponse(
        task_id=task.id,
        status=task.status,
        progress=task.progress,
        result=task.result,
        error=task.error
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update task",
    response_description="Update a task"
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> TaskResponse:
    """Update a task"""
    
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Update task
    update_data = task_data.dict(exclude_unset=True)
    await db.execute(
        sql_update(Task)
        .where(Task.id == task_id)
        .values(**update_data)
    )
    await db.commit()
    await db.refresh(task)
    
    return TaskResponse.from_orm(task)


@router.delete(
    "/{task_id}",
    response_model=dict,
    summary="Delete task",
    response_description="Delete a task"
)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Delete a task"""
    
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    await db.delete(task)
    await db.commit()
    
    return {"status": "success", "message": "Task deleted"}


async def _execute_task_in_background(
    task_id: int,
    task_type: str,
    parameters: dict,
    db: AsyncSession
):
    """Execute a task in the background"""
    
    # Get task from database
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    
    if not task:
        return
    
    try:
        # Update task status to processing
        await db.execute(
            sql_update(Task)
            .where(Task.id == task_id)
            .values(status=TaskStatus.PROCESSING, progress=0)
        )
        await db.commit()
        
        # Execute the task
        response = await agent.execute(task_type=task_type, parameters=parameters)
        
        # Update task with results
        await db.execute(
            sql_update(Task)
            .where(Task.id == task_id)
            .values(
                status=TaskStatus.COMPLETED if response.status == "success" else TaskStatus.FAILED,
                result=response.content if response.status == "success" else {},
                error=response.error if response.status == "error" else None,
                progress=100,
                completed_at=func.now()
            )
        )
        await db.commit()
        
    except Exception as e:
        # Update task with error
        await db.execute(
            sql_update(Task)
            .where(Task.id == task_id)
            .values(
                status=TaskStatus.FAILED,
                error=str(e),
                progress=0
            )
        )
        await db.commit()
