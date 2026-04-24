"""
API Routes
FastAPI route handlers
"""

from .auth import router as auth_router
from .financial import router as financial_router
from .forecast import router as forecast_router
from .chat import router as chat_router
from .reports import router as reports_router

__all__ = [
    "auth_router",
    "financial_router",
    "forecast_router",
    "chat_router",
    "reports_router",
]
