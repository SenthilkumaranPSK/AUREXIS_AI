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
# Commented out - require database models (not available in JSON version)
# from routes.advanced_analytics import router as advanced_analytics_router
# from routes.ml_forecasting import router as ml_forecasting_router
# from routes.investment_optimization import router as investment_optimization_router
from routes.notifications import router as notifications_router
from routes.agent_monitoring import router as agent_monitoring_router
from routes.export import router as export_router

# Create v1 router (no prefix here since main.py will handle it)
api_v1_router = APIRouter()

# Include all sub-routers. Each router owns its resource prefix.
api_v1_router.include_router(auth_router, tags=["Authentication"])
api_v1_router.include_router(financial_router, tags=["Financial"])
api_v1_router.include_router(forecast_router, tags=["Forecast"])
api_v1_router.include_router(chat_router, tags=["Chat"])
api_v1_router.include_router(reports_router, tags=["Reports"])
# Commented out - require database models
# api_v1_router.include_router(advanced_analytics_router, tags=["Advanced Analytics"])
# api_v1_router.include_router(ml_forecasting_router, tags=["ML Forecasting"])
# api_v1_router.include_router(investment_optimization_router, tags=["Investment Optimization"])
api_v1_router.include_router(notifications_router, tags=["Notifications"])
api_v1_router.include_router(agent_monitoring_router, tags=["Agent Monitoring"])
api_v1_router.include_router(export_router, tags=["Export"])
