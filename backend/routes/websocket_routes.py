"""
WebSocket Routes
Real-time communication endpoints
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from typing import Optional
import json
import logging

from auth.jwt_handler import decode_token
from websocket.connection_manager import connection_manager
from websocket.handlers import websocket_handlers

logger = logging.getLogger("aurexis")

router = APIRouter(tags=["WebSocket"])


async def get_user_from_token(token: str) -> Optional[str]:
    """Extract user ID from JWT token"""
    try:
        payload = decode_token(token)
        return payload.get("sub")
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        return None


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(..., description="JWT authentication token")
):
    """
    WebSocket endpoint for real-time communication
    
    Connection URL: ws://localhost:8000/ws?token=<jwt_token>
    
    Message Types:
    - ping: Keep-alive ping
    - subscribe: Subscribe to a channel
    - unsubscribe: Unsubscribe from a channel
    - get_subscriptions: Get current subscriptions
    - get_stats: Get connection statistics
    - echo: Echo message back (testing)
    
    Server Messages:
    - notification: New notification
    - update: Real-time update (transaction, goal, budget, etc.)
    - alert: Alert message
    - pong: Response to ping
    
    Example Messages:
    
    Subscribe to notifications:
    {
        "type": "subscribe",
        "channel": "notifications"
    }
    
    Ping:
    {
        "type": "ping"
    }
    """
    # Validate token
    user_id = await get_user_from_token(token)
    
    if not user_id:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    # Connect
    connection_id = await connection_manager.connect(
        websocket,
        user_id,
        client_info={
            "user_agent": websocket.headers.get("user-agent", "unknown")
        }
    )
    
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "connection_id": connection_id,
            "user_id": user_id,
            "message": "WebSocket connection established",
            "available_channels": [
                "notifications",
                "transactions",
                "goals",
                "alerts",
                "budget",
                "investments",
                "insights",
                "reports"
            ]
        })
        
        # Message loop
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                
                # Handle message
                response = await websocket_handlers.handle_message(
                    message,
                    user_id,
                    connection_manager
                )
                
                # Send response
                if response:
                    await websocket.send_json(response)
            
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "error": "Invalid JSON format"
                })
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                await websocket.send_json({
                    "type": "error",
                    "error": str(e)
                })
    
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id, websocket)
        logger.info(f"WebSocket disconnected: {connection_id}")
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        connection_manager.disconnect(user_id, websocket)


@router.get("/ws/stats")
async def get_websocket_stats():
    """
    Get WebSocket connection statistics
    
    Returns:
        Connection statistics
    """
    stats = connection_manager.get_stats()
    
    return {
        "success": True,
        "stats": stats
    }


@router.get("/ws/active-users")
async def get_active_users():
    """
    Get list of users with active WebSocket connections
    
    Returns:
        List of active user IDs
    """
    active_users = connection_manager.get_active_users()
    
    return {
        "success": True,
        "active_users": active_users,
        "count": len(active_users)
    }


@router.post("/ws/broadcast")
async def broadcast_message(
    message: dict,
    channel: Optional[str] = None
):
    """
    Broadcast message to connected clients (admin only)
    
    Args:
        message: Message to broadcast
        channel: Optional channel to broadcast to
        
    Returns:
        Success status
    """
    try:
        if channel:
            await connection_manager.broadcast_to_channel(message, channel)
        else:
            await connection_manager.broadcast(message)
        
        return {
            "success": True,
            "message": "Message broadcasted",
            "channel": channel
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
