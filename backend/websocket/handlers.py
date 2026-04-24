"""
WebSocket Message Handlers
Handle different types of WebSocket messages
"""

from typing import Dict, Any, Callable
from datetime import datetime
import logging

logger = logging.getLogger("aurexis")


class WebSocketHandlers:
    """Handle WebSocket messages"""
    
    def __init__(self):
        self.handlers: Dict[str, Callable] = {
            "ping": self.handle_ping,
            "subscribe": self.handle_subscribe,
            "unsubscribe": self.handle_unsubscribe,
            "get_subscriptions": self.handle_get_subscriptions,
            "get_stats": self.handle_get_stats,
            "echo": self.handle_echo
        }
    
    async def handle_message(
        self,
        message: Dict[str, Any],
        user_id: str,
        connection_manager
    ) -> Dict[str, Any]:
        """
        Route message to appropriate handler
        
        Args:
            message: Incoming message
            user_id: User ID
            connection_manager: Connection manager instance
            
        Returns:
            Response message
        """
        message_type = message.get("type", "unknown")
        
        handler = self.handlers.get(message_type)
        
        if handler:
            try:
                return await handler(message, user_id, connection_manager)
            except Exception as e:
                logger.error(f"Error handling message type {message_type}: {e}")
                return {
                    "type": "error",
                    "error": str(e),
                    "original_type": message_type
                }
        else:
            return {
                "type": "error",
                "error": f"Unknown message type: {message_type}",
                "supported_types": list(self.handlers.keys())
            }
    
    async def handle_ping(
        self,
        message: Dict[str, Any],
        user_id: str,
        connection_manager
    ) -> Dict[str, Any]:
        """Handle ping message"""
        return {
            "type": "pong",
            "timestamp": datetime.now().isoformat()
        }
    
    async def handle_subscribe(
        self,
        message: Dict[str, Any],
        user_id: str,
        connection_manager
    ) -> Dict[str, Any]:
        """
        Handle channel subscription
        
        Message format:
        {
            "type": "subscribe",
            "channel": "notifications" | "transactions" | "goals" | "alerts"
        }
        """
        channel = message.get("channel")
        
        if not channel:
            return {
                "type": "error",
                "error": "Channel name required"
            }
        
        # Validate channel
        valid_channels = [
            "notifications",
            "transactions",
            "goals",
            "alerts",
            "budget",
            "investments",
            "insights",
            "reports"
        ]
        
        if channel not in valid_channels:
            return {
                "type": "error",
                "error": f"Invalid channel. Valid channels: {valid_channels}"
            }
        
        connection_manager.subscribe(user_id, channel)
        
        return {
            "type": "subscribed",
            "channel": channel,
            "subscriptions": connection_manager.get_user_subscriptions(user_id)
        }
    
    async def handle_unsubscribe(
        self,
        message: Dict[str, Any],
        user_id: str,
        connection_manager
    ) -> Dict[str, Any]:
        """
        Handle channel unsubscription
        
        Message format:
        {
            "type": "unsubscribe",
            "channel": "notifications"
        }
        """
        channel = message.get("channel")
        
        if not channel:
            return {
                "type": "error",
                "error": "Channel name required"
            }
        
        connection_manager.unsubscribe(user_id, channel)
        
        return {
            "type": "unsubscribed",
            "channel": channel,
            "subscriptions": connection_manager.get_user_subscriptions(user_id)
        }
    
    async def handle_get_subscriptions(
        self,
        message: Dict[str, Any],
        user_id: str,
        connection_manager
    ) -> Dict[str, Any]:
        """Get user's current subscriptions"""
        return {
            "type": "subscriptions",
            "subscriptions": connection_manager.get_user_subscriptions(user_id)
        }
    
    async def handle_get_stats(
        self,
        message: Dict[str, Any],
        user_id: str,
        connection_manager
    ) -> Dict[str, Any]:
        """Get connection statistics"""
        stats = connection_manager.get_stats()
        
        return {
            "type": "stats",
            "data": stats
        }
    
    async def handle_echo(
        self,
        message: Dict[str, Any],
        user_id: str,
        connection_manager
    ) -> Dict[str, Any]:
        """Echo message back (for testing)"""
        return {
            "type": "echo",
            "original_message": message,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }


# Global instance
websocket_handlers = WebSocketHandlers()
