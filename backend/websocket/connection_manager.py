"""
WebSocket Connection Manager
Manages WebSocket connections and message broadcasting
"""

from typing import Dict, List, Set, Optional, Any
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import json
import asyncio
import logging

logger = logging.getLogger("aurexis")


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        # Active connections: user_id -> list of WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}
        
        # Connection metadata: connection_id -> metadata
        self.connection_metadata: Dict[str, Dict] = {}
        
        # Subscriptions: user_id -> set of channels
        self.subscriptions: Dict[str, Set[str]] = {}
        
        # Connection counter for unique IDs
        self.connection_counter = 0
    
    async def connect(
        self,
        websocket: WebSocket,
        user_id: str,
        client_info: Optional[Dict] = None
    ) -> str:
        """
        Accept and register a new WebSocket connection
        
        Args:
            websocket: WebSocket connection
            user_id: User ID
            client_info: Optional client information
            
        Returns:
            Connection ID
        """
        await websocket.accept()
        
        # Generate connection ID
        self.connection_counter += 1
        connection_id = f"conn_{user_id}_{self.connection_counter}"
        
        # Add to active connections
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        
        # Store metadata
        self.connection_metadata[connection_id] = {
            "user_id": user_id,
            "websocket": websocket,
            "connected_at": datetime.now().isoformat(),
            "client_info": client_info or {},
            "last_activity": datetime.now().isoformat()
        }
        
        # Initialize subscriptions
        if user_id not in self.subscriptions:
            self.subscriptions[user_id] = set()
        
        logger.info(f"WebSocket connected: {connection_id} for user {user_id}")
        
        return connection_id
    
    def disconnect(self, user_id: str, websocket: WebSocket):
        """
        Remove a WebSocket connection
        
        Args:
            user_id: User ID
            websocket: WebSocket connection to remove
        """
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            
            # Clean up if no more connections
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                if user_id in self.subscriptions:
                    del self.subscriptions[user_id]
        
        # Clean up metadata
        connection_id = self._find_connection_id(user_id, websocket)
        if connection_id and connection_id in self.connection_metadata:
            del self.connection_metadata[connection_id]
        
        logger.info(f"WebSocket disconnected for user {user_id}")
    
    async def send_personal_message(
        self,
        message: Dict[str, Any],
        user_id: str
    ):
        """
        Send message to a specific user (all their connections)
        
        Args:
            message: Message to send
            user_id: Target user ID
        """
        if user_id not in self.active_connections:
            logger.warning(f"No active connections for user {user_id}")
            return
        
        # Add timestamp
        message["timestamp"] = datetime.now().isoformat()
        
        # Send to all user's connections
        disconnected = []
        for websocket in self.active_connections[user_id]:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to {user_id}: {e}")
                disconnected.append(websocket)
        
        # Clean up disconnected connections
        for ws in disconnected:
            self.disconnect(user_id, ws)
    
    async def broadcast(
        self,
        message: Dict[str, Any],
        exclude_user: Optional[str] = None
    ):
        """
        Broadcast message to all connected users
        
        Args:
            message: Message to broadcast
            exclude_user: Optional user ID to exclude
        """
        message["timestamp"] = datetime.now().isoformat()
        
        for user_id in list(self.active_connections.keys()):
            if exclude_user and user_id == exclude_user:
                continue
            
            await self.send_personal_message(message, user_id)
    
    async def broadcast_to_channel(
        self,
        message: Dict[str, Any],
        channel: str
    ):
        """
        Broadcast message to all users subscribed to a channel
        
        Args:
            message: Message to broadcast
            channel: Channel name
        """
        message["timestamp"] = datetime.now().isoformat()
        message["channel"] = channel
        
        for user_id, channels in self.subscriptions.items():
            if channel in channels:
                await self.send_personal_message(message, user_id)
    
    def subscribe(self, user_id: str, channel: str):
        """
        Subscribe user to a channel
        
        Args:
            user_id: User ID
            channel: Channel name
        """
        if user_id not in self.subscriptions:
            self.subscriptions[user_id] = set()
        
        self.subscriptions[user_id].add(channel)
        logger.info(f"User {user_id} subscribed to channel {channel}")
    
    def unsubscribe(self, user_id: str, channel: str):
        """
        Unsubscribe user from a channel
        
        Args:
            user_id: User ID
            channel: Channel name
        """
        if user_id in self.subscriptions:
            self.subscriptions[user_id].discard(channel)
            logger.info(f"User {user_id} unsubscribed from channel {channel}")
    
    def get_user_subscriptions(self, user_id: str) -> List[str]:
        """Get list of channels user is subscribed to"""
        return list(self.subscriptions.get(user_id, set()))
    
    def get_active_users(self) -> List[str]:
        """Get list of users with active connections"""
        return list(self.active_connections.keys())
    
    def get_connection_count(self, user_id: Optional[str] = None) -> int:
        """
        Get connection count
        
        Args:
            user_id: Optional user ID to get count for specific user
            
        Returns:
            Number of connections
        """
        if user_id:
            return len(self.active_connections.get(user_id, []))
        
        return sum(len(conns) for conns in self.active_connections.values())
    
    def get_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        return {
            "total_connections": self.get_connection_count(),
            "active_users": len(self.active_connections),
            "total_subscriptions": sum(len(subs) for subs in self.subscriptions.values()),
            "channels": list(set(
                channel
                for subs in self.subscriptions.values()
                for channel in subs
            ))
        }
    
    def _find_connection_id(self, user_id: str, websocket: WebSocket) -> Optional[str]:
        """Find connection ID for a websocket"""
        for conn_id, metadata in self.connection_metadata.items():
            if metadata["user_id"] == user_id and metadata["websocket"] == websocket:
                return conn_id
        return None
    
    async def send_notification(
        self,
        user_id: str,
        notification: Dict[str, Any]
    ):
        """
        Send notification via WebSocket
        
        Args:
            user_id: Target user ID
            notification: Notification data
        """
        message = {
            "type": "notification",
            "data": notification
        }
        await self.send_personal_message(message, user_id)
    
    async def send_update(
        self,
        user_id: str,
        update_type: str,
        data: Dict[str, Any]
    ):
        """
        Send real-time update
        
        Args:
            user_id: Target user ID
            update_type: Type of update (e.g., 'transaction', 'goal', 'budget')
            data: Update data
        """
        message = {
            "type": "update",
            "update_type": update_type,
            "data": data
        }
        await self.send_personal_message(message, user_id)
    
    async def send_alert(
        self,
        user_id: str,
        alert: Dict[str, Any]
    ):
        """
        Send alert via WebSocket
        
        Args:
            user_id: Target user ID
            alert: Alert data
        """
        message = {
            "type": "alert",
            "data": alert
        }
        await self.send_personal_message(message, user_id)
    
    async def ping_all(self):
        """Send ping to all connections to keep them alive"""
        ping_message = {
            "type": "ping",
            "timestamp": datetime.now().isoformat()
        }
        
        for user_id in list(self.active_connections.keys()):
            disconnected = []
            for websocket in self.active_connections[user_id]:
                try:
                    await websocket.send_json(ping_message)
                except Exception:
                    disconnected.append(websocket)
            
            # Clean up disconnected
            for ws in disconnected:
                self.disconnect(user_id, ws)
    
    async def start_ping_task(self, interval: int = 30):
        """
        Start background task to ping connections
        
        Args:
            interval: Ping interval in seconds
        """
        while True:
            await asyncio.sleep(interval)
            await self.ping_all()


# Global instance
connection_manager = ConnectionManager()
