"""
AUREXIS AI — Chat Memory System
Persistent conversation storage and context management
JSON-based version (no database)
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
import json
import logging

logger = logging.getLogger("aurexis")


class ChatMemoryManager:
    """Manages conversation history and context (in-memory for JSON mode)"""
    
    def __init__(self):
        self.max_context_messages = 20  # Maximum messages to keep in context
        self.max_history_days = 90  # Keep history for 90 days
        self.context_window = 10  # Number of recent messages for context
        self._memory = {}  # In-memory storage: {user_id: [messages]}
    
    def save_message(
        self,
        user_id: str,
        role: str,
        message: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """Save a message to memory"""
        if user_id not in self._memory:
            self._memory[user_id] = []
        
        self._memory[user_id].append({
            "user_id": user_id,
            "session_id": session_id,
            "role": role,
            "message": message,
            "metadata": metadata or {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        # Keep only recent messages
        if len(self._memory[user_id]) > 100:
            self._memory[user_id] = self._memory[user_id][-100:]
        
        return True
    
    def get_conversation_history(
        self,
        user_id: str,
        limit: int = 50,
        session_id: Optional[str] = None,
        days: Optional[int] = None
    ) -> List[Dict]:
        """Get conversation history for a user"""
        if user_id not in self._memory:
            return []
        
        messages = self._memory[user_id]
        
        # Filter by session if provided
        if session_id:
            messages = [m for m in messages if m.get("session_id") == session_id]
        
        # Filter by days if provided
        if days:
            cutoff = datetime.now(timezone.utc) - timedelta(days=days)
            messages = [
                m for m in messages
                if datetime.fromisoformat(m["timestamp"]) > cutoff
            ]
        
        # Return most recent messages
        return messages[-limit:]
    
    def get_recent_context(
        self,
        user_id: str,
        num_messages: int = 10
    ) -> List[Dict]:
        """Get recent messages for context"""
        if user_id not in self._memory:
            return []
        
        messages = self._memory[user_id][-num_messages:]
        return [
            {"role": m["role"], "content": m["message"]}
            for m in messages
        ]
    
    def get_conversation_sessions(
        self,
        user_id: str,
        limit: int = 20
    ) -> List[Dict]:
        """Get list of conversation sessions"""
        if user_id not in self._memory:
            return []
        
        sessions = {}
        for msg in self._memory[user_id]:
            sid = msg.get("session_id")
            if sid and sid not in sessions:
                sessions[sid] = {
                    "session_id": sid,
                    "first_message": msg["timestamp"],
                    "last_message": msg["timestamp"],
                    "message_count": 0
                }
            if sid:
                sessions[sid]["last_message"] = msg["timestamp"]
                sessions[sid]["message_count"] += 1
        
        return list(sessions.values())[-limit:]
    
    def get_conversation_stats(self, user_id: str) -> Dict:
        """Get conversation statistics"""
        if user_id not in self._memory:
            return {
                "total_messages": 0,
                "total_sessions": 0,
                "first_conversation": None,
                "last_conversation": None
            }
        
        messages = self._memory[user_id]
        sessions = set(m.get("session_id") for m in messages if m.get("session_id"))
        
        return {
            "total_messages": len(messages),
            "total_sessions": len(sessions),
            "first_conversation": messages[0]["timestamp"] if messages else None,
            "last_conversation": messages[-1]["timestamp"] if messages else None
        }
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Extract user preferences from conversation history"""
        # Simplified version - return empty preferences
        return {
            "topics_of_interest": [],
            "communication_style": "professional",
            "preferred_language": "en"
        }
    
    def search_conversations(
        self,
        user_id: str,
        search_term: str,
        limit: int = 20
    ) -> List[Dict]:
        """Search conversation history"""
        if user_id not in self._memory:
            return []
        
        search_lower = search_term.lower()
        results = [
            m for m in self._memory[user_id]
            if search_lower in m["message"].lower()
        ]
        
        return results[-limit:]
    
    def clear_user_history(
        self,
        user_id: str,
        session_id: Optional[str] = None,
        days: Optional[int] = None
    ) -> int:
        """Clear conversation history"""
        if user_id not in self._memory:
            return 0
        
        if session_id:
            # Clear specific session
            original_count = len(self._memory[user_id])
            self._memory[user_id] = [
                m for m in self._memory[user_id]
                if m.get("session_id") != session_id
            ]
            return original_count - len(self._memory[user_id])
        elif days:
            # Clear messages older than days
            cutoff = datetime.now(timezone.utc) - timedelta(days=days)
            original_count = len(self._memory[user_id])
            self._memory[user_id] = [
                m for m in self._memory[user_id]
                if datetime.fromisoformat(m["timestamp"]) > cutoff
            ]
            return original_count - len(self._memory[user_id])
        else:
            # Clear all
            count = len(self._memory[user_id])
            self._memory[user_id] = []
            return count


# Global instance
chat_memory_manager = ChatMemoryManager()
