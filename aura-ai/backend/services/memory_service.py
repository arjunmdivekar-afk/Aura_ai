"""
Memory Service - Handles conversation memory, sessions, and user settings
Supports long-term and short-term memory with semantic search
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class MemoryService:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.folders: Dict[str, Dict] = {}
        self.settings: Dict = {}
        self.storage_path = Path("./data/memory")
        self.semantic_index = None
        
    async def initialize(self):
        """Initialize memory service and load existing data"""
        self.storage_path.mkdir(parents=True, exist_ok=True)
        await self._load_sessions()
        await self._load_settings()
        
    async def cleanup(self):
        """Save all data before cleanup"""
        await self._save_sessions()
        await self._save_settings()
        
    async def _load_sessions(self):
        """Load sessions from disk"""
        sessions_file = self.storage_path / "sessions.json"
        if sessions_file.exists():
            with open(sessions_file, 'r') as f:
                self.sessions = json.load(f)
                
    async def _save_sessions(self):
        """Save sessions to disk"""
        sessions_file = self.storage_path / "sessions.json"
        with open(sessions_file, 'w') as f:
            json.dump(self.sessions, f, indent=2, default=str)
            
    async def _load_settings(self):
        """Load settings from disk"""
        settings_file = self.storage_path / "settings.json"
        if settings_file.exists():
            with open(settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = self._default_settings()
            
    async def _save_settings(self):
        """Save settings to disk"""
        settings_file = self.storage_path / "settings.json"
        with open(settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def _default_settings(self) -> Dict:
        return {
            "theme": "dark",
            "language": "en",
            "default_model": "ollama/llama2",
            "auto_save": True,
            "encryption_enabled": False,
            "local_only": False,
            "custom_css": None
        }
    
    # Session Management
    def get_all_sessions(self) -> List[Dict]:
        """Get all chat sessions"""
        return list(self.sessions.values())
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get a specific session"""
        return self.sessions.get(session_id)
    
    def create_session(self, session: Dict) -> Dict:
        """Create a new session"""
        session_id = session.get("id", str(uuid.uuid4()))
        session["created_at"] = datetime.now().isoformat()
        session["updated_at"] = datetime.now().isoformat()
        self.sessions[session_id] = session
        return session
    
    def update_session(self, session_id: str, session: Dict) -> Optional[Dict]:
        """Update an existing session"""
        if session_id in self.sessions:
            session["updated_at"] = datetime.now().isoformat()
            self.sessions[session_id] = session
            return session
        return None
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def add_message(self, session_id: str, message: Dict) -> Optional[Dict]:
        """Add a message to a session"""
        if session_id in self.sessions:
            if "messages" not in self.sessions[session_id]:
                self.sessions[session_id]["messages"] = []
            
            message["id"] = str(uuid.uuid4())
            message["timestamp"] = datetime.now().isoformat()
            self.sessions[session_id]["messages"].append(message)
            self.sessions[session_id]["updated_at"] = datetime.now().isoformat()
            
            # Auto-generate title if first message
            if len(self.sessions[session_id]["messages"]) == 1:
                self.sessions[session_id]["title"] = message["content"][:50] + "..."
            
            return message
        return None
    
    # Folder Management
    def get_all_folders(self) -> List[Dict]:
        """Get all folders"""
        return list(self.folders.values())
    
    def create_folder(self, folder: Dict) -> Dict:
        """Create a new folder"""
        folder_id = folder.get("id", str(uuid.uuid4()))
        folder["created_at"] = datetime.now().isoformat()
        self.folders[folder_id] = folder
        return folder
    
    def delete_folder(self, folder_id: str):
        """Delete a folder"""
        if folder_id in self.folders:
            del self.folders[folder_id]
    
    # Settings Management
    def get_settings(self) -> Dict:
        """Get user settings"""
        return self.settings
    
    def save_settings(self, settings: Dict) -> Dict:
        """Save user settings"""
        self.settings.update(settings)
        return self.settings
    
    # Search & Organization
    def search_sessions(self, query: str) -> List[Dict]:
        """Search sessions by content"""
        results = []
        query_lower = query.lower()
        
        for session in self.sessions.values():
            # Search in title
            if query_lower in session.get("title", "").lower():
                results.append(session)
                continue
            
            # Search in messages
            for message in session.get("messages", []):
                if query_lower in message.get("content", "").lower():
                    results.append(session)
                    break
        
        return results
    
    def get_pinned_sessions(self) -> List[Dict]:
        """Get all pinned sessions"""
        return [s for s in self.sessions.values() if s.get("is_pinned", False)]
    
    def get_sessions_by_folder(self, folder_id: str) -> List[Dict]:
        """Get sessions in a specific folder"""
        return [s for s in self.sessions.values() if s.get("folder_id") == folder_id]
    
    # Export/Import
    def export_chats(self, format: str = "json") -> Dict:
        """Export all chats"""
        if format == "json":
            return {
                "format": "json",
                "exported_at": datetime.now().isoformat(),
                "sessions": list(self.sessions.values())
            }
        elif format == "markdown":
            # Convert to markdown format
            markdown_content = "# Aura AI Chat Export\n\n"
            for session in self.sessions.values():
                markdown_content += f"## {session['title']}\n\n"
                for message in session.get("messages", []):
                    role = message.get("role", "unknown")
                    content = message.get("content", "")
                    markdown_content += f"**{role}**: {content}\n\n"
                markdown_content += "---\n\n"
            
            return {
                "format": "markdown",
                "content": markdown_content
            }
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def import_chats(self, file_data: Dict) -> int:
        """Import chats from file"""
        imported_count = 0
        sessions = file_data.get("sessions", [])
        
        for session in sessions:
            session_id = session.get("id", str(uuid.uuid4()))
            self.sessions[session_id] = session
            imported_count += 1
        
        return imported_count
    
    # Memory Intelligence
    def compress_context(self, session_id: str, max_messages: int = 20) -> Dict:
        """Compress conversation context for long conversations"""
        if session_id not in self.sessions:
            return {"error": "Session not found"}
        
        messages = self.sessions[session_id].get("messages", [])
        
        if len(messages) <= max_messages:
            return {"compressed": False, "messages": messages}
        
        # Keep most recent messages
        compressed_messages = messages[-max_messages:]
        
        # TODO: Summarize older messages
        summary = f"[Previous {len(messages) - max_messages} messages summarized]"
        
        return {
            "compressed": True,
            "summary": summary,
            "messages": compressed_messages
        }
    
    def score_memory_importance(self, session_id: str) -> float:
        """Score the importance of a memory/session"""
        if session_id not in self.sessions:
            return 0.0
        
        session = self.sessions[session_id]
        score = 0.0
        
        # Factors for scoring
        if session.get("is_pinned", False):
            score += 0.3
        
        message_count = len(session.get("messages", []))
        score += min(message_count * 0.01, 0.3)  # Max 0.3 for message count
        
        # Recent activity
        updated_at = session.get("updated_at", "")
        if updated_at:
            days_old = (datetime.now() - datetime.fromisoformat(updated_at)).days
            score += max(0, 0.4 - (days_old * 0.01))  # Decay over time
        
        return min(score, 1.0)
