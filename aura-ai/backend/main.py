"""
Aura AI - Main Backend Server
Max level AI assistant with LM Studio & Ollama support
"""

import asyncio
import json
import os
import uuid
import base64
import hashlib
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Import service modules (to be implemented)
from services.llm_service import LLMService
from services.rag_service import RAGService
from services.file_service import FileService
from services.voice_service import VoiceService
from services.web_search_service import WebSearchService
from services.code_service import CodeService
from services.memory_service import MemoryService
from services.monitoring_service import MonitoringService

app = FastAPI(
    title="Aura AI",
    description="Max level AI assistant with LM Studio & Ollama support",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global services
llm_service = LLMService()
rag_service = RAGService()
file_service = FileService()
voice_service = VoiceService()
web_search_service = WebSearchService()
code_service = CodeService()
memory_service = MemoryService()
monitoring_service = MonitoringService()

# ==================== Models ====================

class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None

class ChatSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "New Chat"
    messages: List[ChatMessage] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    model: str = "default"
    folder_id: Optional[str] = None
    is_pinned: bool = False
    metadata: Optional[Dict[str, Any]] = None

class ModelConfig(BaseModel):
    provider: str  # "ollama" or "lmstudio"
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.9
    stream: bool = True

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    model_config: Optional[ModelConfig] = None
    system_prompt: Optional[str] = None
    web_search: bool = False
    thinking_mode: bool = False
    files: Optional[List[str]] = None

class Folder(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    parent_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class UserSettings(BaseModel):
    theme: str = "dark"
    language: str = "en"
    default_model: str = "ollama/llama2"
    auto_save: bool = True
    encryption_enabled: bool = False
    local_only: bool = False
    custom_css: Optional[str] = None

# ==================== WebSocket Manager ====================

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)

manager = ConnectionManager()

# ==================== API Routes ====================

@app.get("/")
async def root():
    return {"message": "Welcome to Aura AI", "version": "1.0.0"}

@app.get("/api/models")
async def get_available_models():
    """Get all available models from Ollama and LM Studio"""
    try:
        ollama_models = await llm_service.get_ollama_models()
        lmstudio_models = await llm_service.get_lmstudio_models()
        return {
            "ollama": ollama_models,
            "lmstudio": lmstudio_models
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Send a message and get a response"""
    try:
        response = await llm_service.chat(
            message=request.message,
            session_id=request.session_id,
            model_config=request.model_config,
            system_prompt=request.system_prompt,
            web_search=request.web_search,
            thinking_mode=request.thinking_mode,
            files=request.files
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/chat/{client_id}")
async def websocket_chat(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for streaming chat responses"""
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            
            # Process message
            request = ChatRequest(**data)
            
            # Stream response
            async for chunk in llm_service.stream_chat(
                message=request.message,
                session_id=request.session_id,
                model_config=request.model_config,
                system_prompt=request.system_prompt,
                web_search=request.web_search,
                thinking_mode=request.thinking_mode,
                files=request.files
            ):
                await manager.send_personal_message(chunk, client_id)
                
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        await manager.send_personal_message({"error": str(e)}, client_id)
        manager.disconnect(client_id)

# Session Management
@app.get("/api/sessions")
async def get_sessions():
    """Get all chat sessions"""
    return memory_service.get_all_sessions()

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get a specific chat session"""
    session = memory_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.post("/api/sessions")
async def create_session(session: ChatSession):
    """Create a new chat session"""
    return memory_service.create_session(session)

@app.put("/api/sessions/{session_id}")
async def update_session(session_id: str, session: ChatSession):
    """Update a chat session"""
    return memory_service.update_session(session_id, session)

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a chat session"""
    memory_service.delete_session(session_id)
    return {"message": "Session deleted"}

# Folder Management
@app.get("/api/folders")
async def get_folders():
    """Get all folders"""
    return memory_service.get_all_folders()

@app.post("/api/folders")
async def create_folder(folder: Folder):
    """Create a new folder"""
    return memory_service.create_folder(folder)

@app.delete("/api/folders/{folder_id}")
async def delete_folder(folder_id: str):
    """Delete a folder"""
    memory_service.delete_folder(folder_id)
    return {"message": "Folder deleted"}

# File Upload
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file for processing"""
    try:
        result = await file_service.process_file(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload/batch")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload multiple files"""
    results = []
    for file in files:
        try:
            result = await file_service.process_file(file)
            results.append(result)
        except Exception as e:
            results.append({"filename": file.filename, "error": str(e)})
    return results

# RAG Queries
@app.post("/api/rag/query")
async def rag_query(query: str, session_id: Optional[str] = None):
    """Query uploaded documents using RAG"""
    try:
        results = await rag_service.query(query, session_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Web Search
@app.get("/api/search/web")
async def web_search(query: str, engine: str = "duckduckgo"):
    """Perform web search"""
    try:
        results = await web_search_service.search(query, engine)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Code Execution
@app.post("/api/code/execute")
async def execute_code(code: str, language: str = "python"):
    """Execute code in sandbox"""
    try:
        result = await code_service.execute(code, language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/code/format")
async def format_code(code: str, language: str = "python"):
    """Format code"""
    try:
        result = await code_service.format(code, language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Voice Services
@app.post("/api/voice/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe audio to text"""
    try:
        result = await voice_service.transcribe(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/voice/synthesize")
async def synthesize_speech(text: str = Form(...), voice: Optional[str] = Form(None)):
    """Synthesize speech from text"""
    try:
        result = await voice_service.synthesize(text, voice)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Image Generation
@app.post("/api/image/generate")
async def generate_image(prompt: str, model: str = "stable-diffusion"):
    """Generate image from prompt"""
    try:
        result = await llm_service.generate_image(prompt, model)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# OCR
@app.post("/api/ocr")
async def perform_ocr(file: UploadFile = File(...)):
    """Perform OCR on image or PDF"""
    try:
        result = await file_service.ocr(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Monitoring & Stats
@app.get("/api/stats/system")
async def get_system_stats():
    """Get system monitoring stats"""
    return monitoring_service.get_system_stats()

@app.get("/api/stats/model")
async def get_model_stats(model_name: str):
    """Get model-specific stats"""
    return monitoring_service.get_model_stats(model_name)

@app.get("/api/stats/benchmark")
async def benchmark_model(model_name: str, prompt: Optional[str] = None):
    """Benchmark a model"""
    return await monitoring_service.benchmark(model_name, prompt)

# Settings
@app.get("/api/settings")
async def get_settings():
    """Get user settings"""
    return memory_service.get_settings()

@app.put("/api/settings")
async def update_settings(settings: UserSettings):
    """Update user settings"""
    return memory_service.save_settings(settings)

# Export/Import
@app.get("/api/export/chats")
async def export_chats(format: str = "json"):
    """Export all chats"""
    return memory_service.export_chats(format)

@app.post("/api/import/chats")
async def import_chats(file: UploadFile = File(...)):
    """Import chats from file"""
    return memory_service.import_chats(file)

# GitHub Integration
@app.get("/api/github/repos/{repo_name}")
async def get_github_repo(repo_name: str):
    """Get GitHub repository info"""
    try:
        result = await code_service.get_repo_info(repo_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/github/analyze")
async def analyze_github_repo(repo_url: str):
    """Analyze GitHub repository"""
    try:
        result = await code_service.analyze_repo(repo_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== Startup/Shutdown Events ====================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🚀 Starting Aura AI...")
    await llm_service.initialize()
    await rag_service.initialize()
    await memory_service.initialize()
    print("✅ Aura AI ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Shutting down Aura AI...")
    await llm_service.cleanup()
    await rag_service.cleanup()
    await memory_service.cleanup()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
