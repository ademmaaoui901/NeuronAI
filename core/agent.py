"""
AI Production Agent - Main Agent Class
"""

from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
import logging
import asyncio
import json
import os
from datetime import datetime

from config.settings import settings
from config.model_config import model_config

logger = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    """Standard response format for the agent"""
    content: Any
    model: str
    task_type: str
    status: str = "success"
    error: Optional[str] = None
    usage: Dict[str, int] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AgentConfig:
    """Configuration for the AI Agent"""
    model: str = "mistral"
    temperature: float = 0.7
    max_tokens: int = 4096
    use_gpu: bool = True
    use_4bit: bool = True
    offload_to_cpu: bool = True


class AIAgent:
    """
    Main AI Agent class that orchestrates all AI capabilities.
    This is a singleton class that manages all AI models and tools.
    """
    
    _instance = None
    _models_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIAgent, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.config = AgentConfig()
        self.models = {}
        self.tools = {}
        self._load_tools()
        
        logger.info("AI Agent initialized")
    
    def _load_tools(self):
        """Load all available tools"""
        # These will be loaded on demand
        self.tools = {
            "code": {
                "generate": self._generate_code_tool,
                "fix": self._fix_code_tool,
                "explain": self._explain_code_tool
            },
            "image": {
                "generate": self._generate_image_tool,
                "edit": self._edit_image_tool
            },
            "video": {
                "generate": self._generate_video_tool
            },
            "audio": {
                "stt": self._speech_to_text_tool,
                "tts": self._text_to_speech_tool
            },
            "text": {
                "chat": self._chat_tool,
                "summarize": self._summarize_tool,
                "translate": self._translate_tool
            }
        }
        
        logger.info("AI Agent tools loaded")
    
    def _load_models(self):
        """Load AI models (lazy loading)"""
        if self._models_loaded:
            return
        
        logger.info("Loading AI models...")
        
        # Load models based on configuration
        try:
            # Load LLM models
            if model_config.CODE_LLAMA.get("model_name"):
                self._load_llm_model("codellama", model_config.CODE_LLAMA)
            
            if model_config.MISTRAL.get("model_name"):
                self._load_llm_model("mistral", model_config.MISTRAL)
            
            # Load vision models
            if model_config.SDXL.get("model_name"):
                self._load_vision_model("sdxl", model_config.SDXL)
            
            # Load audio models
            if model_config.WHISPER.get("model_name"):
                self._load_audio_model("whisper", model_config.WHISPER)
            
            if model_config.XTTS.get("model_name"):
                self._load_audio_model("xtts", model_config.XTTS)
            
            self._models_loaded = True
            logger.info("All AI models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def _load_llm_model(self, model_name: str, config: Dict[str, Any]):
        """Load a language model"""
        logger.info(f"Loading LLM model: {model_name}")
        
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
            import torch
            
            # Check if GPU is available
            device = "cuda" if torch.cuda.is_available() and config.get("device") == "auto" else "cpu"
            
            # Load model with 4-bit quantization if enabled
            if config.get("quantization") == "4bit" and config.get("use_4bit", True):
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True
                )
                model = AutoModelForCausalLM.from_pretrained(
                    config["model_name"],
                    quantization_config=quantization_config,
                    device_map="auto" if device == "cuda" else None
                )
            else:
                model = AutoModelForCausalLM.from_pretrained(
                    config["model_name"],
                    device_map="auto" if device == "cuda" else None
                )
            
            tokenizer = AutoTokenizer.from_pretrained(config["model_name"])
            
            self.models[model_name] = {
                "model": model,
                "tokenizer": tokenizer,
                "config": config
            }
            
            logger.info(f"Loaded {model_name} model successfully")
        except Exception as e:
            logger.error(f"Error loading {model_name} model: {e}")
            raise
    
    def _load_vision_model(self, model_name: str, config: Dict[str, Any]):
        """Load a vision model"""
        logger.info(f"Loading vision model: {model_name}")
        
        try:
            from diffusers import StableDiffusionXLPipeline
            import torch
            
            device = "cuda" if torch.cuda.is_available() and config.get("device") == "auto" else "cpu"
            
            if model_name == "sdxl":
                pipe = StableDiffusionXLPipeline.from_pretrained(
                    config["model_name"],
                    torch_dtype=torch.float16 if device == "cuda" else torch.float32
                ).to(device)
            else:
                raise ValueError(f"Unknown vision model: {model_name}")
            
            self.models[model_name] = {
                "pipeline": pipe,
                "config": config
            }
            
            logger.info(f"Loaded {model_name} model successfully")
        except Exception as e:
            logger.error(f"Error loading {model_name} model: {e}")
            raise
    
    def _load_audio_model(self, model_name: str, config: Dict[str, Any]):
        """Load an audio model"""
        logger.info(f"Loading audio model: {model_name}")
        
        try:
            from transformers import pipeline
            
            if model_name == "whisper":
                pipe = pipeline(
                    "automatic-speech-recognition",
                    model=config["model_name"],
                    device=0 if config.get("device") == "auto" else -1
                )
            elif model_name == "xtts":
                pipe = pipeline(
                    "text-to-speech",
                    model=config["model_name"],
                    device=0 if config.get("device") == "auto" else -1
                )
            else:
                raise ValueError(f"Unknown audio model: {model_name}")
            
            self.models[model_name] = {
                "pipeline": pipe,
                "config": config
            }
            
            logger.info(f"Loaded {model_name} model successfully")
        except Exception as e:
            logger.error(f"Error loading {model_name} model: {e}")
            raise
    
    def _get_model(self, model_name: str):
        """Get a model, loading it if necessary"""
        if not self._models_loaded:
            self._load_models()
        
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not loaded")
        
        return self.models[model_name]
    
    # ========== CODE TOOLS ==========
    
    def _generate_code_tool(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Generate code from description"""
        model_name = model_config.DEFAULT_MODELS.get("code", "codellama")
        model_data = self._get_model(model_name)
        
        prompt = f"""
        You are an expert {parameters.get('language', 'python')} developer.
        Write code that: {parameters.get('description', '')}
        
        Provide only the code without any explanation or comments.
        Use proper formatting and syntax.
        """
        
        inputs = model_data["tokenizer"](
            prompt,
            return_tensors="pt"
        ).to(model_data["model"].device)
        
        outputs = model_data["model"].generate(
            **inputs,
            max_new_tokens=parameters.get("max_tokens", 4096),
            temperature=parameters.get("temperature", 0.5),
            do_sample=True
        )
        
        code = model_data["tokenizer"].decode(outputs[0], skip_special_tokens=True)
        
        return AgentResponse(
            content=code,
            model=model_name,
            task_type="code_generation",
            usage={"tokens": len(outputs[0])}
        )
    
    def _fix_code_tool(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Fix code errors"""
        model_name = model_config.DEFAULT_MODELS.get("code", "codellama")
        model_data = self._get_model(model_name)
        
        prompt = f"""
        You are an expert {parameters.get('language', 'python')} developer.
        Fix the following code:
        
        Code:
        {parameters.get('code', '')}
        
        Error (if any):
        {parameters.get('error', '')}
        
        Provide only the fixed code without any explanation.
        """
        
        inputs = model_data["tokenizer"](
            prompt,
            return_tensors="pt"
        ).to(model_data["model"].device)
        
        outputs = model_data["model"].generate(
            **inputs,
            max_new_tokens=parameters.get("max_tokens", 4096),
            temperature=parameters.get("temperature", 0.3),
            do_sample=True
        )
        
        code = model_data["tokenizer"].decode(outputs[0], skip_special_tokens=True)
        
        return AgentResponse(
            content=code,
            model=model_name,
            task_type="code_fix",
            usage={"tokens": len(outputs[0])}
        )
    
    def _explain_code_tool(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Explain code"""
        model_name = model_config.DEFAULT_MODELS.get("text", "mistral")
        model_data = self._get_model(model_name)
        
        prompt = f"""
        Explain the following {parameters.get('language', 'python')} code in detail:
        
        {parameters.get('code', '')}
        
        Provide:
        1. What the code does
        2. How it works
        3. Key functions/variables
        4. Time/space complexity (if applicable)
        """
        
        inputs = model_data["tokenizer"](
            prompt,
            return_tensors="pt"
        ).to(model_data["model"].device)
        
        outputs = model_data["model"].generate(
            **inputs,
            max_new_tokens=parameters.get("max_tokens", 4096),
            temperature=parameters.get("temperature", 0.7),
            do_sample=True
        )
        
        explanation = model_data["tokenizer"].decode(outputs[0], skip_special_tokens=True)
        
        return AgentResponse(
            content=explanation,
            model=model_name,
            task_type="code_explain",
            usage={"tokens": len(outputs[0])}
        )
    
    # ========== IMAGE TOOLS ==========
    
    def _generate_image_tool(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Generate image from text"""
        model_name = model_config.DEFAULT_MODELS.get("image", "sdxl")
        model_data = self._get_model(model_name)
        
        pipe = model_data["pipeline"]
        config = model_data["config"]
        
        image = pipe(
            prompt=parameters.get("prompt", ""),
            negative_prompt=parameters.get("negative_prompt", ""),
            width=parameters.get("width", config["width"]),
            height=parameters.get("height", config["height"]),
            num_inference_steps=parameters.get("num_inference_steps", config["num_inference_steps"]),
            guidance_scale=parameters.get("guidance_scale", config["guidance_scale"])
        ).images[0]
        
        # Save image
        import uuid
        from PIL import Image
        image_path = os.path.join(settings.OUTPUTS_DIR, f"{uuid.uuid4()}.png")
        image.save(image_path)
        
        return AgentResponse(
            content={
                "image_path": image_path,
                "image_url": f"/static/{os.path.basename(image_path)}"
            },
            model=model_name,
            task_type="image_generation",
            usage={"inference_steps": parameters.get("num_inference_steps", 30)}
        )
    
    def _edit_image_tool(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Edit an existing image"""
        # For now, we'll just regenerate with the prompt
        # In a full implementation, we'd use inpainting
        return self._generate_image_tool(parameters)
    
    # ========== AUDIO TOOLS ==========
    
    def _speech_to_text_tool(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Convert speech to text"""
        model_name = model_config.DEFAULT_MODELS.get("audio_stt", "whisper")
        model_data = self._get_model(model_name)
        
        pipe = model_data["pipeline"]
        
        # Load audio file
        audio_path = parameters.get("audio_file")
        if not audio_path or not os.path.exists(audio_path):
            raise ValueError(f"Audio file not found: {audio_path}")
        
        result = pipe(
            audio_path,
            language=parameters.get("language", "auto")
        )
        
        return AgentResponse(
            content=result["text"],
            model=model_name,
            task_type="audio_stt",
            usage={"duration": result.get("duration", 0)}
        )
    
    def _text_to_speech_tool(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Convert text to speech"""
        model_name = model_config.DEFAULT_MODELS.get("audio_tts", "xtts")
        model_data = self._get_model(model_name)
        
        pipe = model_data["pipeline"]
        
        result = pipe(
            text=parameters.get("text", ""),
            language=parameters.get("language", "auto")
        )
        
        # Save audio
        import uuid
        audio_path = os.path.join(settings.OUTPUTS_DIR, f"{uuid.uuid4()}.wav")
        import soundfile as sf
        sf.write(audio_path, result["audio"], samplerate=result["sampling_rate"])
        
        return AgentResponse(
            content={
                "audio_path": audio_path,
                "audio_url": f"/static/{os.path.basename(audio_path)}",
                "sampling_rate": result["sampling_rate"]
            },
            model=model_name,
            task_type="audio_tts",
            usage={"duration": len(result["audio"]) / result["sampling_rate"]}
        )
    
    # ========== TEXT TOOLS ==========
    
    def _chat_tool(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Chat with the AI"""
        model_name = model_config.DEFAULT_MODELS.get("chat", "mistral")
        model_data = self._get_model(model_name)
        
        messages = parameters.get("messages", [])
        
        # Format messages for the model
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                prompt += f"System: {content}\n"
            elif role == "user":
                prompt += f"User: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
        
        prompt += "Assistant:"
        
        inputs = model_data["tokenizer"](
            prompt,
            return_tensors="pt"
        ).to(model_data["model"].device)
        
        outputs = model_data["model"].generate(
            **inputs,
            max_new_tokens=parameters.get("max_tokens", 4096),
            temperature=parameters.get("temperature", 0.7),
            do_sample=True
        )
        
        response = model_data["tokenizer"].decode(outputs[0], skip_special_tokens=True)
        
        return AgentResponse(
            content=response,
            model=model_name,
            task_type="chat",
            usage={"tokens": len(outputs[0])}
        )
    
    def _summarize_tool(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Summarize text"""
        model_name = model_config.DEFAULT_MODELS.get("text", "mistral")
        model_data = self._get_model(model_name)
        
        prompt = f"""
        Please provide a concise summary (3-5 sentences) of the following text:
        
        {parameters.get('text', '')}
        
        Summary:
        """
        
        inputs = model_data["tokenizer"](
            prompt,
            return_tensors="pt"
        ).to(model_data["model"].device)
        
        outputs = model_data["model"].generate(
            **inputs,
            max_new_tokens=parameters.get("max_tokens", 512),
            temperature=parameters.get("temperature", 0.5),
            do_sample=True
        )
        
        summary = model_data["tokenizer"].decode(outputs[0], skip_special_tokens=True)
        
        return AgentResponse(
            content=summary,
            model=model_name,
            task_type="summarize",
            usage={"tokens": len(outputs[0])}
        )
    
    def _translate_tool(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Translate text"""
        model_name = model_config.DEFAULT_MODELS.get("text", "mistral")
        model_data = self._get_model(model_name)
        
        prompt = f"""
        Translate the following text from {parameters.get('from_language', 'auto')} to {parameters.get('to_language', 'en')}:
        
        {parameters.get('text', '')}
        
        Translation:
        """
        
        inputs = model_data["tokenizer"](
            prompt,
            return_tensors="pt"
        ).to(model_data["model"].device)
        
        outputs = model_data["model"].generate(
            **inputs,
            max_new_tokens=parameters.get("max_tokens", 2048),
            temperature=parameters.get("temperature", 0.3),
            do_sample=True
        )
        
        translation = model_data["tokenizer"].decode(outputs[0], skip_special_tokens=True)
        
        return AgentResponse(
            content=translation,
            model=model_name,
            task_type="translate",
            usage={"tokens": len(outputs[0])}
        )
    
    # ========== VIDEO TOOLS ==========
    
    def _generate_video_tool(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Generate video from images or text"""
        # This is a placeholder - full implementation requires more setup
        # For now, we'll return a message
        return AgentResponse(
            content="Video generation is not yet fully implemented. This feature requires Stable Video Diffusion model.",
            model="svd",
            task_type="video_generation",
            status="warning"
        )
    
    # ========== MAIN EXECUTE METHOD ==========
    
    async def execute(self, task_type: str, parameters: Dict[str, Any]) -> AgentResponse:
        """
        Execute a task using the appropriate tool.
        This is the main entry point for the agent.
        """
        try:
            # Determine which tool to use
            tool_path = task_type.split("_")
            tool_category = tool_path[0]
            tool_action = tool_path[1] if len(tool_path) > 1 else "execute"
            
            if tool_category in self.tools:
                if tool_action in self.tools[tool_category]:
                    tool = self.tools[tool_category][tool_action]
                    return tool(parameters)
                else:
                    raise ValueError(f"Unknown action: {tool_action} for category: {tool_category}")
            else:
                raise ValueError(f"Unknown task type: {task_type}")
        except Exception as e:
            logger.error(f"Error executing task {task_type}: {e}")
            return AgentResponse(
                content=None,
                model="",
                task_type=task_type,
                status="error",
                error=str(e)
            )


# Singleton instance
agent = AIAgent()
