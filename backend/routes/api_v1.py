"""
API Version 1 Router

Groups all v1 API routes together for versioning.
"""

from fastapi import APIRouter
from routes.auth import router as auth_router
from routes.financial import financial_router
from routes.forecast import forecast_router
from routes.chat import chat_router
from routes.reports import reports_router
from routes.advanced_analytics import router as advanced_analytics_router
from routes.ml_forecasting import router as ml_forecasting_router
from routes.investment_optimization import router as investment_optimization_router
from routes.notifications import router as notifications_router
from routes.agent_monitoring import router as agent_monitoring_router

# Create v1 router (no prefix here since main.py will handle it)
api_v1_router = APIRouter()

# Include all sub-routers with proper nesting
api_v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(financial_router, prefix="/financial", tags=["Financial"])
api_v1_router.include_router(forecast_router, prefix="/forecast", tags=["Forecast"])
api_v1_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
api_v1_router.include_router(reports_router, prefix="/reports", tags=["Reports"])
api_v1_router.include_router(advanced_analytics_router, prefix="/analytics", tags=["Advanced Analytics"])
api_v1_router.include_router(ml_forecasting_router, prefix="/ml", tags=["ML Forecasting"])
api_v1_router.include_router(investment_optimization_router, prefix="/investments", tags=["Investment Optimization"])
api_v1_router.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])
api_v1_router.include_router(agent_monitoring_router, prefix="/agents", tags=["Agent Monitoring"])
