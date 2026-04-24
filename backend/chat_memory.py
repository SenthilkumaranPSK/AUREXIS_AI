"""
AUREXIS AI — Chat Memory System
Persistent conversation storage and context management
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Index
from sqlalchemy.orm import Session
import json
import logging

from database_legacy import Base, SessionLocal

logger = logging.getLogger("aurexis")


class Conversation(Base):
    """Conversation history table"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=False, index=True)
    session_id = Column(String(100), nullable=True, index=True)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    message = Column(Text, nullable=False)
    message_metadata = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), index=True)
    
    # Indexes for faster queries
    __table_args__ = (
        Index('idx_user_timestamp', 'user_id', 'timestamp'),
        Index('idx_session_timestamp', 'session_id', 'timestamp'),
    )


class ChatMemoryManager:
    """Manages conversation history and context"""
    
    def __init__(self):
        self.max_context_messages = 20  # Maximum messages to keep in context
        self.max_history_days = 90  # Keep history for 90 days
        self.context_window = 10  # Number of recent messages for context
    
    def save_message(
        self,
        user_id: str,
        role: str,
        message: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Save a message to conversation history
        
        Args:
            user_id: User identifier
            role: 'user' or 'assistant'
            message: Message content
            session_id: Optional session identifier
            metadata: Optional metadata (sentiment, topics, etc.)
        
        Returns:
            Message ID
        """
        db = SessionLocal()
        try:
            conversation = Conversation(
                user_id=user_id,
                session_id=session_id,
                role=role,
                message=message,
                message_metadata=metadata or {}
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            
            logger.info(f"Saved {role} message for user {user_id}")
            return conversation.id
            
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            db.rollback()
            raise
        finally:
            db.close()
    
    def get_conversation_history(
        self,
        user_id: str,
        limit: int = 50,
        session_id: Optional[str] = None,
        days: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history for a user
        
        Args:
            user_id: User identifier
            limit: Maximum number of messages to return
            session_id: Optional session filter
            days: Optional filter for messages within last N days
        
        Returns:
            List of conversation messages
        """
        db = SessionLocal()
        try:
            query = db.query(Conversation).filter(Conversation.user_id == user_id)
            
            if session_id:
                query = query.filter(Conversation.session_id == session_id)
            
            if days:
                cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
                query = query.filter(Conversation.timestamp >= cutoff_date)
            
            conversations = query.order_by(
                Conversation.timestamp.desc()
            ).limit(limit).all()
            
            # Reverse to get chronological order
            conversations.reverse()
            
            return [
                {
                    "id": conv.id,
                    "role": conv.role,
                    "message": conv.message,
                    "timestamp": conv.timestamp.isoformat(),
                    "session_id": conv.session_id,
                    "metadata": conv.message_metadata or {}
                }
                for conv in conversations
            ]
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
        finally:
            db.close()
    
    def get_recent_context(
        self,
        user_id: str,
        num_messages: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        Get recent messages for context in chat
        
        Args:
            user_id: User identifier
            num_messages: Number of recent messages (default: context_window)
        
        Returns:
            List of messages in format for Ollama API
        """
        num_messages = num_messages or self.context_window
        
        history = self.get_conversation_history(
            user_id=user_id,
            limit=num_messages,
            days=7  # Only last 7 days for context
        )
        
        # Convert to Ollama format
        return [
            {
                "role": msg["role"],
                "content": msg["message"]
            }
            for msg in history
        ]
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """
        Extract user preferences from conversation history
        
        Args:
            user_id: User identifier
        
        Returns:
            Dictionary of user preferences
        """
        db = SessionLocal()
        try:
            # Get all conversations with metadata
            conversations = db.query(Conversation).filter(
                Conversation.user_id == user_id,
                Conversation.message_metadata.isnot(None)
            ).order_by(Conversation.timestamp.desc()).limit(100).all()
            
            preferences = {
                "topics_of_interest": [],
                "common_questions": [],
                "preferred_response_style": "detailed",
                "financial_goals": [],
                "concerns": []
            }
            
            # Analyze metadata to extract preferences
            for conv in conversations:
                metadata = conv.message_metadata or {}
                
                if "topics" in metadata:
                    preferences["topics_of_interest"].extend(metadata["topics"])
                
                if "question_type" in metadata:
                    preferences["common_questions"].append(metadata["question_type"])
                
                if "goals" in metadata:
                    preferences["financial_goals"].extend(metadata["goals"])
            
            # Remove duplicates and get top items
            preferences["topics_of_interest"] = list(set(preferences["topics_of_interest"]))[:10]
            preferences["common_questions"] = list(set(preferences["common_questions"]))[:10]
            preferences["financial_goals"] = list(set(preferences["financial_goals"]))[:5]
            
            return preferences
            
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return {}
        finally:
            db.close()
    
    def get_conversation_sessions(
        self,
        user_id: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get list of conversation sessions for a user
        
        Args:
            user_id: User identifier
            limit: Maximum number of sessions
        
        Returns:
            List of session summaries
        """
        db = SessionLocal()
        try:
            from sqlalchemy import func
            
            # Get distinct sessions with first and last message
            sessions = db.query(
                Conversation.session_id,
                func.min(Conversation.timestamp).label('start_time'),
                func.max(Conversation.timestamp).label('end_time'),
                func.count(Conversation.id).label('message_count')
            ).filter(
                Conversation.user_id == user_id,
                Conversation.session_id.isnot(None)
            ).group_by(
                Conversation.session_id
            ).order_by(
                func.max(Conversation.timestamp).desc()
            ).limit(limit).all()
            
            session_list = []
            for session in sessions:
                # Get first user message as session title
                first_message = db.query(Conversation).filter(
                    Conversation.user_id == user_id,
                    Conversation.session_id == session.session_id,
                    Conversation.role == 'user'
                ).order_by(Conversation.timestamp.asc()).first()
                
                title = first_message.message[:50] + "..." if first_message is not None and len(first_message.message) > 50 else (first_message.message if first_message is not None else "Conversation")
                
                session_list.append({
                    "session_id": session.session_id,
                    "title": title,
                    "start_time": session.start_time.isoformat(),
                    "end_time": session.end_time.isoformat(),
                    "message_count": session.message_count,
                    "duration_minutes": int((session.end_time - session.start_time).total_seconds() / 60)
                })
            
            return session_list
            
        except Exception as e:
            logger.error(f"Error getting conversation sessions: {e}")
            return []
        finally:
            db.close()
    
    def clear_user_history(
        self,
        user_id: str,
        session_id: Optional[str] = None,
        days: Optional[int] = None
    ) -> int:
        """
        Clear conversation history for a user
        
        Args:
            user_id: User identifier
            session_id: Optional session to clear (if None, clears all)
            days: Optional clear messages older than N days
        
        Returns:
            Number of messages deleted
        """
        db = SessionLocal()
        try:
            query = db.query(Conversation).filter(Conversation.user_id == user_id)
            
            if session_id:
                query = query.filter(Conversation.session_id == session_id)
            
            if days:
                cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
                query = query.filter(Conversation.timestamp < cutoff_date)
            
            count = query.count()
            query.delete()
            db.commit()
            
            logger.info(f"Cleared {count} messages for user {user_id}")
            return count
            
        except Exception as e:
            logger.error(f"Error clearing history: {e}")
            db.rollback()
            return 0
        finally:
            db.close()
    
    def search_conversations(
        self,
        user_id: str,
        search_term: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search conversation history for a term
        
        Args:
            user_id: User identifier
            search_term: Term to search for
            limit: Maximum results
        
        Returns:
            List of matching messages
        """
        db = SessionLocal()
        try:
            conversations = db.query(Conversation).filter(
                Conversation.user_id == user_id,
                Conversation.message.ilike(f"%{search_term}%")
            ).order_by(
                Conversation.timestamp.desc()
            ).limit(limit).all()
            
            return [
                {
                    "id": conv.id,
                    "role": conv.role,
                    "message": conv.message,
                    "timestamp": conv.timestamp.isoformat(),
                    "session_id": conv.session_id
                }
                for conv in conversations
            ]
            
        except Exception as e:
            logger.error(f"Error searching conversations: {e}")
            return []
        finally:
            db.close()
    
    def get_conversation_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Get statistics about user's conversation history
        
        Args:
            user_id: User identifier
        
        Returns:
            Dictionary of statistics
        """
        db = SessionLocal()
        try:
            total_messages = db.query(Conversation).filter(
                Conversation.user_id == user_id
            ).count()
            
            user_messages = db.query(Conversation).filter(
                Conversation.user_id == user_id,
                Conversation.role == 'user'
            ).count()
            
            assistant_messages = db.query(Conversation).filter(
                Conversation.user_id == user_id,
                Conversation.role == 'assistant'
            ).count()
            
            # Get first and last conversation
            first_conv = db.query(Conversation).filter(
                Conversation.user_id == user_id
            ).order_by(Conversation.timestamp.asc()).first()
            
            last_conv = db.query(Conversation).filter(
                Conversation.user_id == user_id
            ).order_by(Conversation.timestamp.desc()).first()
            
            # Get unique sessions
            session_count = db.query(Conversation.session_id).filter(
                Conversation.user_id == user_id,
                Conversation.session_id.isnot(None)
            ).distinct().count()
            
            stats = {
                "total_messages": total_messages,
                "user_messages": user_messages,
                "assistant_messages": assistant_messages,
                "session_count": session_count,
                "first_conversation": first_conv.timestamp.isoformat() if first_conv else None,
                "last_conversation": last_conv.timestamp.isoformat() if last_conv else None,
                "days_active": (last_conv.timestamp - first_conv.timestamp).days if first_conv and last_conv else 0
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting conversation stats: {e}")
            return {}
        finally:
            db.close()
    
    def cleanup_old_conversations(self, days: int = 90) -> int:
        """
        Clean up conversations older than specified days
        
        Args:
            days: Delete conversations older than this many days
        
        Returns:
            Number of conversations deleted
        """
        db = SessionLocal()
        try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            count = db.query(Conversation).filter(
                Conversation.timestamp < cutoff_date
            ).count()
            
            db.query(Conversation).filter(
                Conversation.timestamp < cutoff_date
            ).delete()
            
            db.commit()
            
            logger.info(f"Cleaned up {count} old conversations")
            return count
            
        except Exception as e:
            logger.error(f"Error cleaning up conversations: {e}")
            db.rollback()
            return 0
        finally:
            db.close()


# Singleton instance
chat_memory_manager = ChatMemoryManager()
