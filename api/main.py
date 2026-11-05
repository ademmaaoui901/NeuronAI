"""
AI Production Agent - Main API Application
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

from config.settings import settings
from .database import init_db, close_db
from .endpoints import (
    users, chat, code, image, 
    video, audio, tasks, health
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Add file handler
file_handler = RotatingFileHandler(
    'logs/ai_agent.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting AI Production Agent API...")
    await init_db()
    logger.info("Database initialized successfully")
    
    # Create directories if they don't exist
    os.makedirs(settings.MODELS_DIR, exist_ok=True)
    os.makedirs(settings.UPLOADS_DIR, exist_ok=True)
    os.makedirs(settings.OUTPUTS_DIR, exist_ok=True)
    os.makedirs(settings.CACHE_DIR, exist_ok=True)
    
    logger.info(f"Directories created: {settings.MODELS_DIR}, {settings.UPLOADS_DIR}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Production Agent API...")
    await close_db()
    logger.info("Database connection closed")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Advanced AI Agent API with Code, Image, Video, Audio capabilities",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


# Mount static files
app.mount("/static", StaticFiles(directory=settings.OUTPUTS_DIR), name="static")

# Include routers
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(code.router, prefix="/api/v1/code", tags=["code"])
app.include_router(image.router, prefix="/api/v1/image", tags=["image"])
app.include_router(video.router, prefix="/api/v1/video", tags=["video"])
app.include_router(audio.router, prefix="/api/v1/audio", tags=["audio"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health"
    }


# 404 handler
@app.get("/404", include_in_schema=False)
async def not_found():
    return JSONResponse(
        status_code=404,
        content={"message": "Not found"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )
