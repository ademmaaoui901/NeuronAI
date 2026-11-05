"""
AI Production Agent - Code Celery Tasks
"""

from celery import shared_task
from typing import Dict, Any
import os
import uuid

from config.settings import settings
from core.agent import agent


@shared_task(bind=True, max_retries=3)
def generate_code_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Generate code in background"""
    try:
        response = agent.execute(
            task_type="code_generate",
            parameters=parameters
        )
        
        if response.status == "error":
            raise Exception(response.error)
        
        # Save code to file if project name is provided
        file_path = None
        if parameters.get("project_name"):
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
            }.get(parameters.get("language", "python").lower(), ".txt")
            
            project_dir = os.path.join(settings.PROJECTS_DIR, parameters["project_name"])
            os.makedirs(project_dir, exist_ok=True)
            
            file_path = os.path.join(project_dir, f"main{file_ext}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(response.content)
        
        return {
            "status": "success",
            "code": response.content,
            "file_path": file_path,
            "model": response.model,
            "usage": response.usage
        }
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def fix_code_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Fix code in background"""
    try:
        response = agent.execute(
            task_type="code_fix",
            parameters=parameters
        )
        
        if response.status == "error":
            raise Exception(response.error)
        
        return {
            "status": "success",
            "code": response.content,
            "model": response.model,
            "usage": response.usage
        }
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def explain_code_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Explain code in background"""
    try:
        response = agent.execute(
            task_type="code_explain",
            parameters=parameters
        )
        
        if response.status == "error":
            raise Exception(response.error)
        
        return {
            "status": "success",
            "explanation": response.content,
            "model": response.model,
            "usage": response.usage
        }
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def create_project_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Create a complete project in background"""
    try:
        # Create project directory
        project_dir = os.path.join(settings.PROJECTS_DIR, parameters["name"])
        os.makedirs(project_dir, exist_ok=True)
        
        # Generate main code
        code_response = agent.execute(
            task_type="code_generate",
            parameters={
                "description": f"Create a {parameters.get('language', 'python')} project that: {parameters.get('description', '')}",
                "language": parameters.get("language", "python"),
                "max_tokens": 4096
            }
        )
        
        if code_response.status == "error":
            raise Exception(code_response.error)
        
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
        }.get(parameters.get("language", "python").lower(), ".txt")
        
        main_file = os.path.join(project_dir, f"main{file_ext}")
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(code_response.content)
        
        # Generate README
        readme_response = agent.execute(
            task_type="text_chat",
            parameters={
                "messages": [
                    {
                        "role": "user",
                        "content": f"Create a comprehensive README.md file for a {parameters.get('language', 'python')} project that: {parameters.get('description', '')}"
                    }
                ],
                "max_tokens": 2048
            }
        )
        
        if readme_response.status == "error":
            raise Exception(readme_response.error)
        
        readme_file = os.path.join(project_dir, "README.md")
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_response.content)
        
        # Get project structure
        structure = {}
        for root, dirs, files in os.walk(project_dir):
            rel_path = os.path.relpath(root, project_dir)
            if rel_path == ".":
                rel_path = parameters["name"]
            structure[rel_path] = {
                "type": "directory",
                "contents": [{"type": "file", "name": f} for f in files]
            }
        
        return {
            "status": "success",
            "project_name": parameters["name"],
            "project_dir": project_dir,
            "structure": structure,
            "files": [
                {"path": main_file, "type": "main"},
                {"path": readme_file, "type": "readme"}
            ]
        }
    except Exception as e:
        self.retry(exc=e, countdown=60)
