"""
API Routes
FastAPI route handlers
"""

from .auth import router as auth_router
from .financial import financial_router
from .forecast import forecast_router
from .chat import chat_router
from .reports import reports_router

__all__ = [
    "auth_router",
    "financial_router",
    "forecast_router",
    "chat_router",
    "reports_router",
]
