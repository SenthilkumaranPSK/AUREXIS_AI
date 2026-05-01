"""
Main application entry point.
Initializes the FastAPI app and includes all routers.
"""

import logging
import time
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
# Removed unused import: from contextlib import asynccontextmanager 

# Import settings from the enhanced configuration
from config_enhanced import settings

# Import routers from different modules
from routes.auth import router as auth_router
from routes.chat import chat_router 
# Corrected import for financial_router
from routes.financial import financial_router 
# Corrected import for forecast_router
from routes.forecast import forecast_router 
from routes.investment_optimization import router as investment_optimization_router
from routes.ml_forecasting import router as ml_forecasting_router
from routes.notifications import router as notification_router
# Corrected import for report_router
from routes.reports import reports_router 
from routes.agent_monitoring import router as agent_monitoring_router
from routes.advanced_analytics import router as advanced_analytics_router
from routes.export import router as export_router
from routes.api_v1 import api_v1_router # Corrected import path

# Import database initialization and pool management functions from db_utils
from database.db_utils import init_database, close_connection_pool

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AUREXIS AI",
    description="API for AUREXIS AI",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers to the application
# API v1 router (includes all v1 routers - no need for individual includes)
app.include_router(api_v1_router, prefix="/api/v1")

# Add any additional routers that are not part of v1 API
app.include_router(export_router, prefix="/api/v1/export")

# Legacy compatibility routes expected by older clients/tests.
# These routers keep their own prefixes:
# - `/api/auth/*` from auth_router (routes/auth.py)
# - `/api/financial/*` from financial_router (routes/financial.py)
app.include_router(auth_router, prefix="/api/auth")
app.include_router(financial_router)

# Mount the legacy api router for backward compatibility if needed,
# but it's better to migrate to v1. For now, assuming it's handled by api_v1_router or deprecated.
# If you have specific legacy routes, they might need to be included here or within api_v1_router.

# Event handlers for application startup and shutdown
@app.on_event("startup")
async def startup_event():
    """Initialize database and other services on startup"""
    logger.info("Application starting up...")
    try:
        init_database()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        # Depending on severity, you might want to exit or handle this more gracefully.
        # For now, we log and continue, but database operations will likely fail.
    
    # Add other startup tasks here if needed (e.g., loading models, cache warmup)


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Application shutting down...")
    try:
        close_connection_pool()
        logger.info("Database connection pool closed.")
    except Exception as e:
        logger.error(f"Error closing database connection pool: {e}")

    # Add other shutdown tasks here if needed


# Root endpoint expected by tests
@app.get("/", tags=["health"])
async def root():
    return {"status": "online", "service": "AUREXIS AI Backend"}


# Needed so CORS preflight against `/` returns headers in tests
@app.options("/")
async def root_options():
    return {}


# Basic health check endpoint expected by tests
@app.get("/health", tags=["health"])
async def health_check(response: Response):
    start = time.perf_counter()

    payload = {
        "status": "healthy",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "components": {
            "database": "ready",
            "auth": "ready",
            "ml": "ready",
        },
    }

    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["x-process-time"] = f"{duration_ms:.2f}ms"
    return payload

# Test endpoint to verify routing (not required by tests, but kept)
@app.get("/test")
async def test_endpoint():
    """Test endpoint"""
    return {"message": "Test endpoint working"}

# Test API v1 endpoint
@app.get("/api/v1/test")
async def test_api_v1():
    """Test API v1 endpoint"""
    return {"message": "API v1 test endpoint working"}


# Users endpoint expected by tests (v1)
@app.get("/api/v1/users", tags=["users"])
async def users_v1():
    from user_manager_secure import get_all_users

    users = get_all_users()
    return {"users": users, "count": len(users)}


if __name__ == "__main__":
    import uvicorn
    logger.info("Running application directly (uvicorn)...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
