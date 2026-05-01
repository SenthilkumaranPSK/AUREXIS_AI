"""
Enhanced WebSocket Functionality for AUREXIS AI
Real-time updates, notifications, and live collaboration
"""

import asyncio
import json
import uuid
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
import logging
from dataclasses import dataclass, asdict
from enum import Enum

from exceptions import ValidationError, NotFoundError
from async_operations import AsyncUserManager, AsyncFinancialOperations
from config_enhanced import settings

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """WebSocket message types"""
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    HEARTBEAT = "heartbeat"
    NOTIFICATION = "notification"
    FINANCIAL_UPDATE = "financial_update"
    CHAT_MESSAGE = "chat_message"
    CHAT_RESPONSE = "chat_response"
    GOAL_UPDATE = "goal_update"
    ALERT = "alert"
    ANALYTICS_UPDATE = "analytics_update"
    COLLABORATION = "collaboration"
    ERROR = "error"


class NotificationType(str, Enum):
    """Notification types"""
    BUDGET_ALERT = "budget_alert"
    GOAL_ACHIEVED = "goal_achieved"
    INVESTMENT_UPDATE = "investment_update"
    SECURITY_ALERT = "security_alert"
    SYSTEM_MAINTENANCE = "system_maintenance"
    NEW_FEATURE = "new_feature"


@dataclass
class WebSocketMessage:
    """Standard WebSocket message format"""
    type: MessageType
    data: Dict[str, Any]
    timestamp: str
    message_id: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ConnectionManager:
    """Enhanced WebSocket connection manager"""
    
    def __init__(self):
        # Active connections by user_id
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # Connection metadata
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
        # Room-based connections for collaboration
        self.rooms: Dict[str, Set[WebSocket]] = {}
        # Message history for reconnection
        self.message_history: Dict[str, List[WebSocketMessage]] = {}
        # Rate limiting
        self.message_counts: Dict[WebSocket, Dict[str, Any]] = {}
        
    async def connect(self, websocket: WebSocket, user_id: str, session_id: str) -> str:
        """Connect a WebSocket client"""
        await websocket.accept()
        
        connection_id = str(uuid.uuid4())
        
        # Store connection
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        
        # Store metadata
        self.connection_metadata[websocket] = {
            "user_id": user_id,
            "session_id": session_id,
            "connection_id": connection_id,
            "connected_at": datetime.now().isoformat(),
            "last_heartbeat": datetime.now().isoformat(),
            "message_count": 0
        }
        
        # Initialize message counting
        self.message_counts[websocket] = {
            "count": 0,
            "window_start": datetime.now()
        }
        
        # Initialize message history
        if user_id not in self.message_history:
            self.message_history[user_id] = []
        
        # Send welcome message
        await self.send_personal_message(websocket, WebSocketMessage(
            type=MessageType.CONNECT,
            data={
                "connection_id": connection_id,
                "message": "Connected to AUREXIS AI real-time updates",
                "features": [
                    "Live financial updates",
                    "Real-time notifications",
                    "Chat with AI advisor",
                    "Goal tracking updates",
                    "Collaboration features"
                ]
            },
            timestamp=datetime.now().isoformat(),
            message_id=str(uuid.uuid4()),
            user_id=user_id
        ))
        
        logger.info(f"WebSocket connected: user_id={user_id}, connection_id={connection_id}")
        return connection_id
    
    async def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket client"""
        metadata = self.connection_metadata.get(websocket)
        if not metadata:
            return
        
        user_id = metadata["user_id"]
        connection_id = metadata["connection_id"]
        
        # Remove from active connections
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        # Remove from rooms
        for room_id, connections in self.rooms.items():
            connections.discard(websocket)
        
        # Clean up metadata
        self.connection_metadata.pop(websocket, None)
        self.message_counts.pop(websocket, None)
        
        logger.info(f"WebSocket disconnected: user_id={user_id}, connection_id={connection_id}")
    
    async def send_personal_message(self, websocket: WebSocket, message: WebSocketMessage):
        """Send message to specific WebSocket"""
        try:
            await websocket.send_text(json.dumps(message.to_dict()))
            
            # Update message count
            if websocket in self.message_counts:
                self.message_counts[websocket]["count"] += 1
            
            # Store in history
            user_id = message.user_id
            if user_id and user_id in self.message_history:
                self.message_history[user_id].append(message)
                # Keep only last 100 messages
                if len(self.message_history[user_id]) > 100:
                    self.message_history[user_id] = self.message_history[user_id][-100:]
                    
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            await self.disconnect(websocket)
    
    async def send_user_message(self, user_id: str, message: WebSocketMessage):
        """Send message to all connections for a user"""
        if user_id not in self.active_connections:
            return
        
        disconnected = set()
        for connection in self.active_connections[user_id]:
            try:
                await self.send_personal_message(connection, message)
            except Exception as e:
                logger.error(f"Error sending message to user {user_id}: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            await self.disconnect(connection)
    
    async def broadcast_to_room(self, room_id: str, message: WebSocketMessage):
        """Broadcast message to all connections in a room"""
        if room_id not in self.rooms:
            return
        
        disconnected = set()
        for connection in self.rooms[room_id]:
            try:
                await self.send_personal_message(connection, message)
            except Exception as e:
                logger.error(f"Error broadcasting to room {room_id}: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            await self.disconnect(connection)
    
    async def join_room(self, websocket: WebSocket, room_id: str):
        """Add connection to a room"""
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        self.rooms[room_id].add(websocket)
        
        # Update metadata
        if websocket in self.connection_metadata:
            if "rooms" not in self.connection_metadata[websocket]:
                self.connection_metadata[websocket]["rooms"] = set()
            self.connection_metadata[websocket]["rooms"].add(room_id)
    
    async def leave_room(self, websocket: WebSocket, room_id: str):
        """Remove connection from a room"""
        if room_id in self.rooms:
            self.rooms[room_id].discard(websocket)
        
        # Update metadata
        if websocket in self.connection_metadata:
            if "rooms" in self.connection_metadata[websocket]:
                self.connection_metadata[websocket]["rooms"].discard(room_id)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        total_connections = sum(len(conns) for conns in self.active_connections.values())
        total_rooms = len(self.rooms)
        
        return {
            "total_connections": total_connections,
            "active_users": len(self.active_connections),
            "total_rooms": total_rooms,
            "connections_per_user": {
                user_id: len(conns) 
                for user_id, conns in self.active_connections.items()
            }
        }


class RealTimeNotificationService:
    """Real-time notification service"""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
    
    async def send_budget_alert(self, user_id: str, alert_data: Dict[str, Any]):
        """Send budget alert to user"""
        message = WebSocketMessage(
            type=MessageType.NOTIFICATION,
            data={
                "notification_type": NotificationType.BUDGET_ALERT,
                "title": "Budget Alert",
                "message": alert_data.get("message", "Budget threshold exceeded"),
                "category": alert_data.get("category"),
                "spent": alert_data.get("spent"),
                "budget": alert_data.get("budget"),
                "percentage": alert_data.get("percentage"),
                "severity": alert_data.get("severity", "medium")
            },
            timestamp=datetime.now().isoformat(),
            message_id=str(uuid.uuid4()),
            user_id=user_id
        )
        
        await self.connection_manager.send_user_message(user_id, message)
    
    async def send_goal_achievement(self, user_id: str, goal_data: Dict[str, Any]):
        """Send goal achievement notification"""
        message = WebSocketMessage(
            type=MessageType.NOTIFICATION,
            data={
                "notification_type": NotificationType.GOAL_ACHIEVED,
                "title": "Goal Achieved! 🎉",
                "message": f"Congratulations! You've achieved your goal: {goal_data.get('name')}",
                "goal_name": goal_data.get("name"),
                "target_amount": goal_data.get("target_amount"),
                "achieved_amount": goal_data.get("current_amount"),
                "completion_date": datetime.now().isoformat()
            },
            timestamp=datetime.now().isoformat(),
            message_id=str(uuid.uuid4()),
            user_id=user_id
        )
        
        await self.connection_manager.send_user_message(user_id, message)
    
    async def send_financial_update(self, user_id: str, update_data: Dict[str, Any]):
        """Send financial data update"""
        message = WebSocketMessage(
            type=MessageType.FINANCIAL_UPDATE,
            data={
                "update_type": update_data.get("type", "general"),
                "metrics": update_data.get("metrics", {}),
                "changes": update_data.get("changes", {}),
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now().isoformat(),
            message_id=str(uuid.uuid4()),
            user_id=user_id
        )
        
        await self.connection_manager.send_user_message(user_id, message)
    
    async def send_analytics_update(self, user_id: str, analytics_data: Dict[str, Any]):
        """Send analytics update"""
        message = WebSocketMessage(
            type=MessageType.ANALYTICS_UPDATE,
            data={
                "metrics": analytics_data.get("metrics", {}),
                "trends": analytics_data.get("trends", {}),
                "insights": analytics_data.get("insights", []),
                "forecast": analytics_data.get("forecast", {})
            },
            timestamp=datetime.now().isoformat(),
            message_id=str(uuid.uuid4()),
            user_id=user_id
        )
        
        await self.connection_manager.send_user_message(user_id, message)


class WebSocketChatService:
    """WebSocket-based chat service with real-time AI responses"""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
    
    async def handle_chat_message(
        self, 
        websocket: WebSocket, 
        message_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle chat message with real-time AI response"""
        try:
            metadata = self.connection_manager.connection_metadata.get(websocket)
            if not metadata:
                raise ValidationError("Invalid connection")
            
            user_id = metadata["user_id"]
            message_content = message_data.get("message", "")
            
            # Send user message confirmation
            user_message = WebSocketMessage(
                type=MessageType.CHAT_MESSAGE,
                data={
                    "role": "user",
                    "content": message_content,
                    "timestamp": datetime.now().isoformat()
                },
                timestamp=datetime.now().isoformat(),
                message_id=str(uuid.uuid4()),
                user_id=user_id
            )
            
            await self.connection_manager.send_personal_message(websocket, user_message)
            
            # Get AI response asynchronously
            from async_operations import AsyncExternalServiceOperations
            
            # Get user context
            user_data = await AsyncUserManager.get_all_user_data_async(user_id)
            user_context = await AsyncUserManager.get_user_by_id_async(user_id) or {}
            
            # Get AI response
            ai_response = await AsyncExternalServiceOperations.call_ollama_async(
                message=message_content,
                user_context=user_context,
                financial_data=user_data
            )
            
            # Send AI response
            ai_message = WebSocketMessage(
                type=MessageType.CHAT_RESPONSE,
                data={
                    "role": "assistant",
                    "content": ai_response.get("content", ""),
                    "model": ai_response.get("model"),
                    "confidence": ai_response.get("confidence"),
                    "timestamp": datetime.now().isoformat()
                },
                timestamp=datetime.now().isoformat(),
                message_id=str(uuid.uuid4()),
                user_id=user_id
            )
            
            await self.connection_manager.send_personal_message(websocket, ai_message)
            
            return {
                "success": True,
                "user_message": user_message.to_dict(),
                "ai_response": ai_message.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error handling chat message: {e}")
            
            # Send error message
            error_message = WebSocketMessage(
                type=MessageType.ERROR,
                data={
                    "error": "Failed to process chat message",
                    "details": str(e)
                },
                timestamp=datetime.now().isoformat(),
                message_id=str(uuid.uuid4()),
                user_id=user_id if 'user_id' in locals() else None
            )
            
            await self.connection_manager.send_personal_message(websocket, error_message)
            
            return {"success": False, "error": str(e)}


class WebSocketCollaborationService:
    """Real-time collaboration features"""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    async def create_collaboration_session(
        self, 
        creator_id: str, 
        session_data: Dict[str, Any]
    ) -> str:
        """Create a collaboration session"""
        session_id = str(uuid.uuid4())
        
        self.active_sessions[session_id] = {
            "id": session_id,
            "creator_id": creator_id,
            "name": session_data.get("name", "Collaboration Session"),
            "type": session_data.get("type", "financial_planning"),
            "participants": {creator_id},
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "data": session_data.get("initial_data", {})
        }
        
        # Notify creator
        message = WebSocketMessage(
            type=MessageType.COLLABORATION,
            data={
                "action": "session_created",
                "session_id": session_id,
                "session_info": self.active_sessions[session_id]
            },
            timestamp=datetime.now().isoformat(),
            message_id=str(uuid.uuid4()),
            user_id=creator_id
        )
        
        await self.connection_manager.send_user_message(creator_id, message)
        
        return session_id
    
    async def join_collaboration_session(
        self, 
        user_id: str, 
        session_id: str
    ) -> bool:
        """Join a collaboration session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        session["participants"].add(user_id)
        
        # Notify all participants
        message = WebSocketMessage(
            type=MessageType.COLLABORATION,
            data={
                "action": "participant_joined",
                "session_id": session_id,
                "user_id": user_id,
                "participant_count": len(session["participants"])
            },
            timestamp=datetime.now().isoformat(),
            message_id=str(uuid.uuid4())
        )
        
        # Broadcast to all participants
        for participant_id in session["participants"]:
            message.user_id = participant_id
            await self.connection_manager.send_user_message(participant_id, message)
        
        return True
    
    async def update_session_data(
        self, 
        user_id: str, 
        session_id: str, 
        update_data: Dict[str, Any]
    ) -> bool:
        """Update collaboration session data"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        if user_id not in session["participants"]:
            return False
        
        # Update session data
        session["data"].update(update_data)
        session["updated_at"] = datetime.now().isoformat()
        
        # Notify all participants
        message = WebSocketMessage(
            type=MessageType.COLLABORATION,
            data={
                "action": "data_updated",
                "session_id": session_id,
                "updated_by": user_id,
                "changes": update_data,
                "full_data": session["data"]
            },
            timestamp=datetime.now().isoformat(),
            message_id=str(uuid.uuid4())
        )
        
        # Broadcast to all participants
        for participant_id in session["participants"]:
            message.user_id = participant_id
            await self.connection_manager.send_user_message(participant_id, message)
        
        return True


# Global instances
connection_manager = ConnectionManager()
notification_service = RealTimeNotificationService(connection_manager)
chat_service = WebSocketChatService(connection_manager)
collaboration_service = WebSocketCollaborationService(connection_manager)


async def handle_websocket_connection(
    websocket: WebSocket, 
    user_id: str, 
    session_id: str
):
    """Handle WebSocket connection lifecycle"""
    connection_id = None
    try:
        # Connect
        connection_id = await connection_manager.connect(websocket, user_id, session_id)
        
        # Start heartbeat
        heartbeat_task = asyncio.create_task(send_heartbeat(websocket))
        
        # Handle messages
        while True:
            try:
                # Receive message with timeout
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                message_data = json.loads(data)
                
                await handle_websocket_message(websocket, message_data)
                
            except asyncio.TimeoutError:
                # Send heartbeat if no message received
                await send_heartbeat_message(websocket)
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await send_error_message(websocket, "Invalid JSON format")
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")
                await send_error_message(websocket, f"Error processing message: {e}")
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for user {user_id}")
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        # Cleanup
        if connection_id:
            await connection_manager.disconnect(websocket)
        heartbeat_task.cancel()


async def handle_websocket_message(websocket: WebSocket, message_data: Dict[str, Any]):
    """Handle incoming WebSocket messages"""
    message_type = message_data.get("type")
    
    if message_type == "chat":
        await chat_service.handle_chat_message(websocket, message_data)
    
    elif message_type == "heartbeat":
        await handle_heartbeat_response(websocket, message_data)
    
    elif message_type == "join_room":
        room_id = message_data.get("room_id")
        if room_id:
            await connection_manager.join_room(websocket, room_id)
    
    elif message_type == "leave_room":
        room_id = message_data.get("room_id")
        if room_id:
            await connection_manager.leave_room(websocket, room_id)
    
    elif message_type == "collaboration":
        await handle_collaboration_message(websocket, message_data)
    
    else:
        await send_error_message(websocket, f"Unknown message type: {message_type}")


async def send_heartbeat(websocket: WebSocket):
    """Send periodic heartbeat messages"""
    while True:
        try:
            await asyncio.sleep(30)  # Send heartbeat every 30 seconds
            await send_heartbeat_message(websocket)
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")
            break


async def send_heartbeat_message(websocket: WebSocket):
    """Send heartbeat message"""
    message = WebSocketMessage(
        type=MessageType.HEARTBEAT,
        data={"timestamp": datetime.now().isoformat()},
        timestamp=datetime.now().isoformat(),
        message_id=str(uuid.uuid4())
    )
    
    await connection_manager.send_personal_message(websocket, message)


async def handle_heartbeat_response(websocket: WebSocket, message_data: Dict[str, Any]):
    """Handle heartbeat response"""
    metadata = connection_manager.connection_metadata.get(websocket)
    if metadata:
        metadata["last_heartbeat"] = datetime.now().isoformat()


async def send_error_message(websocket: WebSocket, error_message: str):
    """Send error message to client"""
    metadata = connection_manager.connection_metadata.get(websocket)
    user_id = metadata.get("user_id") if metadata else None
    
    message = WebSocketMessage(
        type=MessageType.ERROR,
        data={"error": error_message},
        timestamp=datetime.now().isoformat(),
        message_id=str(uuid.uuid4()),
        user_id=user_id
    )
    
    await connection_manager.send_personal_message(websocket, message)


async def handle_collaboration_message(websocket: WebSocket, message_data: Dict[str, Any]):
    """Handle collaboration messages"""
    action = message_data.get("action")
    metadata = connection_manager.connection_metadata.get(websocket)
    
    if not metadata:
        return
    
    user_id = metadata["user_id"]
    
    if action == "create_session":
        session_id = await collaboration_service.create_collaboration_session(
            user_id, message_data
        )
        await connection_manager.join_room(websocket, session_id)
    
    elif action == "join_session":
        session_id = message_data.get("session_id")
        if session_id:
            success = await collaboration_service.join_collaboration_session(
                user_id, session_id
            )
            if success:
                await connection_manager.join_room(websocket, session_id)
    
    elif action == "update_data":
        session_id = message_data.get("session_id")
        update_data = message_data.get("data", {})
        if session_id and update_data:
            await collaboration_service.update_session_data(
                user_id, session_id, update_data
            )
