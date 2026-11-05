"""
AI Production Agent - Code Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import os
import uuid

from ..database import get_db
from ..models.user import User
from ..schemas.code import CodeRequest, CodeResponse
from core.security import get_current_user
from core.agent import agent
from config.settings import settings

router = APIRouter()


@router.post(
    "/generate",
    response_model=CodeResponse,
    summary="Generate code",
    response_description="Generate code from a description"
)
async def generate_code(
    request: CodeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CodeResponse:
    """Generate code from a description"""
    
    # Execute code generation task
    response = await agent.execute(
        task_type="code_generate",
        parameters={
            "description": request.description,
            "language": request.language,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature
        }
    )
    
    if response.status == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response.error
        )
    
    # Save code to file if project name is provided
    file_path = None
    if request.project_name:
        file_ext = {
            "python": ".py",
            "javascript": ".js",
            "java": ".java",
            "c++": ".cpp",
            "c": ".c",
            "go": ".go",
            "rust": ".rs",
            "php": ".php",
            "ruby": ".rb",
            "swift": ".swift",
            "kotlin": ".kt"
        }.get(request.language.lower(), ".txt")
        
        project_dir = os.path.join(settings.PROJECTS_DIR, request.project_name)
        os.makedirs(project_dir, exist_ok=True)
        
        file_path = os.path.join(project_dir, f"main{file_ext}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(response.content)
    
    return CodeResponse(
        code=response.content,
        language=request.language,
        action=request.action,
        file_path=file_path,
        model=response.model,
        usage=response.usage
    )


@router.post(
    "/fix",
    response_model=CodeResponse,
    summary="Fix code",
    response_description="Fix errors in code"
)
async def fix_code(
    request: CodeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CodeResponse:
    """Fix errors in code"""
    
    if not request.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code is required for fixing"
        )
    
    # Execute code fix task
    response = await agent.execute(
        task_type="code_fix",
        parameters={
            "code": request.code,
            "error": request.error or "",
            "language": request.language,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature
        }
    )
    
    if response.status == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response.error
        )
    
    return CodeResponse(
        code=response.content,
        language=request.language,
        action="fix",
        explanation=None,
        model=response.model,
        usage=response.usage
    )


@router.post(
    "/explain",
    response_model=CodeResponse,
    summary="Explain code",
    response_description="Explain what the code does"
)
async def explain_code(
    request: CodeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CodeResponse:
    """Explain what the code does"""
    
    if not request.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code is required for explanation"
        )
    
    # Execute code explain task
    response = await agent.execute(
        task_type="code_explain",
        parameters={
            "code": request.code,
            "language": request.language,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature
        }
    )
    
    if response.status == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response.error
        )
    
    return CodeResponse(
        code=request.code,
        language=request.language,
        action="explain",
        explanation=response.content,
        model=response.model,
        usage=response.usage
    )


@router.post(
    "/project",
    response_model=dict,
    summary="Create project",
    response_description="Create a complete project"
)
async def create_project(
    name: str,
    description: str,
    language: str = "python",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Create a complete project with multiple files"""
    
    # Create project directory
    project_dir = os.path.join(settings.PROJECTS_DIR, name)
    os.makedirs(project_dir, exist_ok=True)
    
    # Generate main code
    code_response = await agent.execute(
        task_type="code_generate",
        parameters={
            "description": f"Create a {language} project that: {description}",
            "language": language,
            "max_tokens": 4096
        }
    )
    
    if code_response.status == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=code_response.error
        )
    
    # Save main file
    file_ext = {
        "python": ".py",
        "javascript": ".js",
        "java": ".java",
        "c++": ".cpp",
        "c": ".c",
        "go": ".go",
        "rust": ".rs",
        "php": ".php",
        "ruby": ".rb",
        "swift": ".swift",
        "kotlin": ".kt"
    }.get(language.lower(), ".txt")
    
    main_file = os.path.join(project_dir, f"main{file_ext}")
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(code_response.content)
    
    # Generate README
    readme_response = await agent.execute(
        task_type="text_chat",
        parameters={
            "messages": [
                {
                    "role": "user",
                    "content": f"Create a comprehensive README.md file for a {language} project that: {description}"
                }
            ],
            "max_tokens": 2048
        }
    )
    
    readme_file = os.path.join(project_dir, "README.md")
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_response.content)
    
    # Generate requirements.txt for Python
    if language.lower() == "python":
        req_response = await agent.execute(
            task_type="text_chat",
            parameters={
                "messages": [
                    {
                        "role": "user",
                        "content": f"List all Python dependencies for a project that: {description}. Format as requirements.txt"
                    }
                ],
                "max_tokens": 512
            }
        )
        
        req_file = os.path.join(project_dir, "requirements.txt")
        with open(req_file, 'w', encoding='utf-8') as f:
            f.write(req_response.content)
    
    # Get project structure
    structure = {}
    for root, dirs, files in os.walk(project_dir):
        rel_path = os.path.relpath(root, project_dir)
        if rel_path == ".":
            rel_path = name
        structure[rel_path] = {
            "type": "directory",
            "contents": [{"type": "file", "name": f} for f in files]
        }
    
    return {
        "status": "success",
        "project_name": name,
        "project_dir": project_dir,
        "structure": structure,
        "files": [
            {"path": main_file, "type": "main"},
            {"path": readme_file, "type": "readme"}
        ]
    }


@router.post(
    "/apk",
    response_model=dict,
    summary="Create APK",
    response_description="Create an Android APK file (simulated)"
)
async def create_apk(
    project_name: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Create an Android APK file"""
    
    # This is a simulation - full APK generation requires Android SDK
    project_dir = os.path.join(settings.PROJECTS_DIR, project_name)
    
    if not os.path.exists(project_dir):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_name} not found"
        )
    
    # Simulate APK generation
    apk_path = os.path.join(project_dir, f"{project_name}.apk")
    
    # Create a dummy APK file (in reality, this would be built using Android Studio)
    with open(apk_path, 'w') as f:
        f.write("This is a simulated APK file")
    
    return {
        "status": "success",
        "message": "APK generation simulated",
        "apk_path": apk_path,
        "note": "For real APK generation, Android SDK and proper build tools are required"
    }
