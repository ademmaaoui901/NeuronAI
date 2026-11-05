"""
AI Production Agent - Configuration Settings
"""

from pydantic import BaseSettings, Field
from typing import Optional, List
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI Production Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # Server
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/ai_agent",
        env="DATABASE_URL"
    )
    
    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    
    # Models Directory
    MODELS_DIR: str = Field(
        default="./models",
        env="MODELS_DIR"
    )
    
    # Storage Directory
    STORAGE_DIR: str = Field(
        default="./storage",
        env="STORAGE_DIR"
    )
    
    # Uploads Directory
    UPLOADS_DIR: str = Field(
        default="./storage/uploads",
        env="UPLOADS_DIR"
    )
    
    # Outputs Directory
    OUTPUTS_DIR: str = Field(
        default="./storage/outputs",
        env="OUTPUTS_DIR"
    )
    
    # Cache Directory
    CACHE_DIR: str = Field(
        default="./storage/cache",
        env="CACHE_DIR"
    )
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["*"],
        env="CORS_ORIGINS"
    )
    
    # AI Models Configuration
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton instance
settings = Settings()

# Create directories if they don't exist
os.makedirs(settings.MODELS_DIR, exist_ok=True)
os.makedirs(settings.STORAGE_DIR, exist_ok=True)
os.makedirs(settings.UPLOADS_DIR, exist_ok=True)
os.makedirs(settings.OUTPUTS_DIR, exist_ok=True)
os.makedirs(settings.CACHE_DIR, exist_ok=True)
