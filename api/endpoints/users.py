"""
AI Production Agent - Users Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sql_update
from typing import List, Optional
import secrets
import hashlib

from ..database import get_db
from ..models.user import User
from ..schemas.user import (
    UserCreate, UserResponse, UserLogin, 
    UserUpdate, Token, TokenData
)
from config.settings import settings
from core.security import (
    create_access_token, 
    verify_password, 
    get_password_hash,
    get_current_user
)

router = APIRouter()
security = HTTPBearer()


# Helper functions
def generate_api_key() -> str:
    """Generate a random API key"""
    return secrets.token_urlsafe(32)


def hash_api_key(api_key: str) -> str:
    """Hash API key for storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()


# User endpoints
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    response_description="Create a new user account"
)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Register a new user"""
    
    # Check if username exists
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Generate API key
    api_key = generate_api_key()
    hashed_api_key = hash_api_key(api_key)
    
    # Create user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        api_key=hashed_api_key,
        is_active=True,
        is_verified=False
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Return user response with API key
    user_response = UserResponse.from_orm(new_user)
    user_response.api_key = api_key
    
    return user_response


@router.post(
    "/login",
    response_model=Token,
    summary="Login user",
    response_description="Authenticate user and get access token"
)
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
) -> Token:
    """Login user and return access token"""
    
    # Find user
    result = await db.execute(
        select(User).where(User.username == login_data.username)
    )
    user = result.scalars().first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.username, "user_id": str(user.id)}
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    response_description="Get information about the current user"
)
async def get_current_user_endpoint(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Get current user information"""
    return UserResponse.from_orm(current_user)


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List all users",
    response_description="List all registered users (Admin only)"
)
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[UserResponse]:
    """List all users"""
    
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can list all users"
        )
    
    result = await db.execute(select(User))
    users = result.scalars().all()
    
    return [UserResponse.from_orm(user) for user in users]


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user",
    response_description="Update current user information"
)
async def update_current_user(
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Update current user information"""
    
    update_data = user_data.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    if update_data:
        await db.execute(
            sql_update(User)
            .where(User.id == current_user.id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(current_user)
    
    return UserResponse.from_orm(current_user)


@router.post(
    "/refresh-api-key",
    response_model=UserResponse,
    summary="Refresh API key",
    response_description="Generate a new API key for the current user"
)
async def refresh_api_key(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Generate a new API key"""
    
    # Generate new API key
    api_key = generate_api_key()
    hashed_api_key = hash_api_key(api_key)
    
    # Update user
    await db.execute(
        sql_update(User)
        .where(User.id == current_user.id)
        .values(api_key=hashed_api_key)
    )
    await db.commit()
    await db.refresh(current_user)
    
    # Return user response with new API key
    user_response = UserResponse.from_orm(current_user)
    user_response.api_key = api_key
    
    return user_response
