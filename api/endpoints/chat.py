"""
AI Production Agent - Chat Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..models.user import User
from ..schemas.chat import ChatRequest, ChatResponse, ChatStreamResponse
from core.security import get_current_user, get_current_user_from_api_key
from core.agent import agent

router = APIRouter()


@router.post(
    "/",
    response_model=ChatResponse,
    summary="Chat with AI",
    response_description="Send a message and get an AI response"
)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """Chat with the AI agent"""
    
    # Execute chat task
    response = await agent.execute(
        task_type="text_chat",
        parameters={
            "messages": request.messages,
            "model": request.model,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens
        }
    )
    
    if response.status == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response.error
        )
    
    # Create response
    return ChatResponse(
        message={
            "role": "assistant",
            "content": response.content
        },
        model=response.model,
        finish_reason="stop",
        usage=response.usage
    )


@router.post(
    "/stream",
    response_model=ChatStreamResponse,
    summary="Streaming chat",
    response_description="Stream AI responses in real-time"
)
async def chat_stream(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ChatStreamResponse:
    """Stream chat responses"""
    
    # For now, we'll return a simple response
    # Full streaming implementation requires more setup
    response = await agent.execute(
        task_type="text_chat",
        parameters={
            "messages": request.messages,
            "model": request.model,
            "temperature": request.temperature,
            "max_tokens": min(request.max_tokens, 100)  # Limit for streaming
        }
    )
    
    if response.status == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response.error
        )
    
    return ChatStreamResponse(
        chunk=response.content,
        model=response.model
    )
