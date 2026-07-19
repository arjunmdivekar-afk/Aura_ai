"""
LLM Service - Handles communication with Ollama and LM Studio
Supports streaming, model switching, and intelligent routing
"""

import asyncio
import json
import httpx
from typing import AsyncGenerator, Dict, List, Optional, Any
from datetime import datetime


class LLMService:
    def __init__(self):
        self.ollama_base_url = "http://localhost:11434"
        self.lmstudio_base_url = "http://localhost:1234"
        self.available_models = {"ollama": [], "lmstudio": []}
        self.model_cache = {}
        
    async def initialize(self):
        """Initialize and fetch available models"""
        await self.refresh_models()
        
    async def cleanup(self):
        """Cleanup resources"""
        self.model_cache.clear()
        
    async def refresh_models(self):
        """Refresh available models from both providers"""
        try:
            # Get Ollama models
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.ollama_base_url}/api/tags", timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    self.available_models["ollama"] = [
                        {"name": model["name"], "provider": "ollama"}
                        for model in data.get("models", [])
                    ]
        except Exception as e:
            print(f"Error fetching Ollama models: {e}")
            
        try:
            # Get LM Studio models
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.lmstudio_base_url}/v1/models", timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    self.available_models["lmstudio"] = [
                        {"name": model["id"], "provider": "lmstudio"}
                        for model in data.get("data", [])
                    ]
        except Exception as e:
            print(f"Error fetching LM Studio models: {e}")
    
    async def get_ollama_models(self) -> List[Dict]:
        """Get available Ollama models"""
        return self.available_models["ollama"]
    
    async def get_lmstudio_models(self) -> List[Dict]:
        """Get available LM Studio models"""
        return self.available_models["lmstudio"]
    
    def _select_best_model(self, query: str, has_images: bool = False, is_code: bool = False, is_math: bool = False) -> Dict:
        """Intelligently select the best model for the task"""
        # Simple heuristic-based model selection
        all_models = self.available_models["ollama"] + self.available_models["lmstudio"]
        
        if not all_models:
            return {"name": "llama2", "provider": "ollama"}
        
        # Vision tasks
        if has_images:
            vision_models = [m for m in all_models if any(x in m["name"].lower() for x in ["vision", "vl", "llava"])]
            if vision_models:
                return vision_models[0]
        
        # Code tasks
        if is_code:
            code_models = [m for m in all_models if any(x in m["name"].lower() for x in ["code", "deepseek", "starcoder"])]
            if code_models:
                return code_models[0]
        
        # Math/Reasoning tasks
        if is_math:
            reasoning_models = [m for m in all_models if any(x in m["name"].lower() for x in ["math", "reason"])]
            if reasoning_models:
                return reasoning_models[0]
        
        # Default to first available model
        return all_models[0]
    
    async def chat(
        self,
        message: str,
        session_id: Optional[str] = None,
        model_config: Optional[Dict] = None,
        system_prompt: Optional[str] = None,
        web_search: bool = False,
        thinking_mode: bool = False,
        files: Optional[List[str]] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """Send a chat message and get response"""
        
        # Auto-select model if not specified
        if not model_config:
            model_config = self._select_best_model(message)
        
        provider = model_config.get("provider", "ollama")
        model_name = model_config.get("model_name", "llama2")
        
        # Build messages array
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": message})
        
        # Route to appropriate provider
        if provider == "ollama":
            response = await self._ollama_chat(model_name, messages, model_config)
        elif provider == "lmstudio":
            response = await self._lmstudio_chat(model_name, messages, model_config)
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        return response
    
    async def stream_chat(
        self,
        message: str,
        session_id: Optional[str] = None,
        model_config: Optional[Dict] = None,
        system_prompt: Optional[str] = None,
        web_search: bool = False,
        thinking_mode: bool = False,
        files: Optional[List[str]] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> AsyncGenerator[Dict, None]:
        """Stream chat response token by token"""
        
        # Auto-select model if not specified
        if not model_config:
            model_config = self._select_best_model(message)
        
        provider = model_config.get("provider", "ollama")
        model_name = model_config.get("model_name", "llama2")
        
        # Build messages array
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": message})
        
        # Route to appropriate provider
        if provider == "ollama":
            async for chunk in self._ollama_stream(model_name, messages, model_config):
                yield chunk
        elif provider == "lmstudio":
            async for chunk in self._lmstudio_stream(model_name, messages, model_config):
                yield chunk
    
    async def _ollama_chat(self, model: str, messages: List[Dict], config: Dict) -> Dict:
        """Chat with Ollama"""
        async with httpx.AsyncClient() as client:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": config.get("temperature", 0.7),
                    "top_p": config.get("top_p", 0.9),
                    "num_predict": config.get("max_tokens", 2048)
                }
            }
            
            response = await client.post(
                f"{self.ollama_base_url}/api/chat",
                json=payload,
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "role": "assistant",
                "content": data["message"]["content"],
                "model": model,
                "provider": "ollama",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _ollama_stream(self, model: str, messages: List[Dict], config: Dict) -> AsyncGenerator[Dict, None]:
        """Stream chat with Ollama"""
        async with httpx.AsyncClient() as client:
            payload = {
                "model": model,
                "messages": messages,
                "stream": True,
                "options": {
                    "temperature": config.get("temperature", 0.7),
                    "top_p": config.get("top_p", 0.9),
                    "num_predict": config.get("max_tokens", 2048)
                }
            }
            
            async with client.stream(
                "POST",
                f"{self.ollama_base_url}/api/chat",
                json=payload,
                timeout=120.0
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if "message" in data:
                                yield {
                                    "type": "token",
                                    "content": data["message"].get("content", ""),
                                    "done": data.get("done", False)
                                }
                        except json.JSONDecodeError:
                            continue
    
    async def _lmstudio_chat(self, model: str, messages: List[Dict], config: Dict) -> Dict:
        """Chat with LM Studio"""
        async with httpx.AsyncClient() as client:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": config.get("temperature", 0.7),
                "max_tokens": config.get("max_tokens", 2048),
                "top_p": config.get("top_p", 0.9),
                "stream": False
            }
            
            response = await client.post(
                f"{self.lmstudio_base_url}/v1/chat/completions",
                json=payload,
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "role": "assistant",
                "content": data["choices"][0]["message"]["content"],
                "model": model,
                "provider": "lmstudio",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _lmstudio_stream(self, model: str, messages: List[Dict], config: Dict) -> AsyncGenerator[Dict, None]:
        """Stream chat with LM Studio"""
        async with httpx.AsyncClient() as client:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": config.get("temperature", 0.7),
                "max_tokens": config.get("max_tokens", 2048),
                "top_p": config.get("top_p", 0.9),
                "stream": True
            }
            
            async with client.stream(
                "POST",
                f"{self.lmstudio_base_url}/v1/chat/completions",
                json=payload,
                timeout=120.0
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data.strip() == "[DONE]":
                            yield {"type": "token", "content": "", "done": True}
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield {
                                    "type": "token",
                                    "content": content,
                                    "done": False
                                }
                        except json.JSONDecodeError:
                            continue
    
    async def generate_image(self, prompt: str, model: str = "stable-diffusion") -> Dict:
        """Generate image from prompt (placeholder for future implementation)"""
        # This would integrate with Stable Diffusion or FLUX
        return {
            "status": "not_implemented",
            "message": "Image generation will be implemented in future version"
        }
    
    async def analyze_code(self, code: str, language: str = "python") -> Dict:
        """Analyze code and provide suggestions"""
        # This would use a code-specialized model
        return {
            "analysis": "Code analysis placeholder",
            "suggestions": []
        }
