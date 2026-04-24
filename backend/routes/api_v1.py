"""
API Version 1 Router

Groups all v1 API routes together for versioning.
"""

from fastapi import APIRouter
from routes import (
    auth_router,
    financial_router,
    forecast_router,
    chat_router,
    reports_router
)
from routes.advanced_analytics import router as advanced_analytics_router
from routes.ml_forecasting import router as ml_forecasting_router
from routes.investment_optimization import router as investment_optimization_router
from routes.notifications import router as notifications_router
from routes.agent_monitoring import router as agent_monitoring_router

# Create v1 router
api_v1_router = APIRouter(prefix="/api/v1")

# Include all sub-routers
api_v1_router.include_router(auth_router, tags=["v1-auth"])
api_v1_router.include_router(financial_router, tags=["v1-financial"])
api_v1_router.include_router(forecast_router, tags=["v1-forecast"])
api_v1_router.include_router(chat_router, tags=["v1-chat"])
api_v1_router.include_router(reports_router, tags=["v1-reports"])
api_v1_router.include_router(advanced_analytics_router, tags=["v1-analytics"])
api_v1_router.include_router(ml_forecasting_router, tags=["v1-ml"])
api_v1_router.include_router(investment_optimization_router, tags=["v1-investments"])
api_v1_router.include_router(notifications_router, tags=["v1-notifications"])
api_v1_router.include_router(agent_monitoring_router, tags=["v1-agents"])
