"""
WebSocket Module
Real-time communication system
"""

from .connection_manager import connection_manager
from .handlers import websocket_handlers

__all__ = [
    "connection_manager",
    "websocket_handlers"
]
