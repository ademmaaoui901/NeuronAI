"""
AI Production Agent - Model Configuration
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """Configuration for AI models"""
    
    # LLM Models
    CODE_LLAMA: Dict[str, Any] = field(default_factory=lambda: {
        "model_name": "codellama/CodeLlama-7b-Instruct-hf",
        "model_type": "llama",
        "quantization": "4bit",
        "device": "auto",
        "max_new_tokens": 4096,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50
    })
    
    MISTRAL: Dict[str, Any] = field(default_factory=lambda: {
        "model_name": "mistralai/Mistral-7B-Instruct-v0.1",
        "model_type": "mistral",
        "quantization": "4bit",
        "device": "auto",
        "max_new_tokens": 4096,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50
    })
    
    # Vision Models
    SDXL: Dict[str, Any] = field(default_factory=lambda: {
        "model_name": "stabilityai/stable-diffusion-xl-base-1.0",
        "pipe_class": "StableDiffusionXLPipeline",
        "device": "auto",
        "width": 1024,
        "height": 1024,
        "num_inference_steps": 30,
        "guidance_scale": 7.5
    })
    
    # Audio Models
    WHISPER: Dict[str, Any] = field(default_factory=lambda: {
        "model_name": "openai/whisper-large-v2",
        "device": "auto",
        "language": "auto",
        "task": "transcribe"
    })
    
    XTTS: Dict[str, Any] = field(default_factory=lambda: {
        "model_name": "coqui/XTTS-v2",
        "device": "auto",
        "language": "auto",
        "speaker": "default"
    })
    
    # Default models for different tasks
    DEFAULT_MODELS: Dict[str, str] = field(default_factory=lambda: {
        "code": "codellama",
        "text": "mistral",
        "chat": "mistral",
        "image": "sdxl",
        "audio_stt": "whisper",
        "audio_tts": "xtts"
    })
    
    # Performance settings
    USE_GPU: bool = True
    USE_4BIT: bool = True
    USE_8BIT: bool = False
    OFFLOAD_TO_CPU: bool = True


# Singleton instance
model_config = ModelConfig()
