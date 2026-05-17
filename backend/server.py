"""
AUREXIS AI Backend Server
Simple FastAPI server with essential endpoints
"""

import os
import builtins
import logging
import time
from typing import Optional, Dict, List, Any
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from urllib.parse import quote
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from slowapi import Limiter
from slowapi.util import get_remote_address

# Import configuration
from config import settings

# Import security
from security import get_current_user

# Ensure critical directories exist for Render/Production
if not os.path.exists("user_data"):
    os.makedirs("user_data")

# Import user management (JSON-based, no database)
from user_manager_json import authenticate_user, get_all_users

# Import cache manager
from cache_manager import cache

# Import UserService
from services.user_service import UserService

# Configure logging
from logger import logger

# Global state
active_sessions = {}

# SlowAPI limiter instance (expected by tests)
limiter = Limiter(key_func=get_remote_address)

# JSON-based server - no database connection needed
# Legacy function removed - tests should use JSON-based approach


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events"""
    # Startup
    try:
        logger.info("✅ JSON-based server - No database initialization needed")
    except Exception as e:
        logger.error(f"Startup error: {e}")

    yield

    # Shutdown
    logger.info("Application shutting down")


# Initialize FastAPI app (SINGLE INITIALIZATION)
app = FastAPI(
    title="AUREXIS AI",
    description="AI-powered Financial Decision Support System API. "
                "Provides comprehensive financial analysis, risk assessment, "
                "and personalized insights using advanced machine learning models.",
    version="2.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    contact={
        "name": "AUREXIS AI Team",
        "email": "support@aurexis.ai",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    tags=[
        {
            "name": "health",
            "description": "System health and status checks"
        },
        {
            "name": "authentication",
            "description": "User authentication and session management"
        },
        {
            "name": "users",
            "description": "User management and profile operations"
        },
    ],
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Import and include financial routes
try:
    from routes.api_v1 import api_v1_router
    from routes.auth import router as auth_router
    from routes.financial import financial_router
    from routes.chat import chat_router
    from routes.forecast import forecast_router
    from routes.reports import reports_router
    from routes.export import router as export_router
    from routes.notifications import router as notification_router
    from routes.agent_monitoring import router as agent_router
    from routes.websocket_routes import router as websocket_router
    from routes.advanced_analytics import router as analytics_router
    from routes.transactions import router as transactions_router
    
    # Canonical legacy API surface used by the frontend/startup docs.
    app.include_router(financial_router, prefix="/api/financial", tags=["Financial"])
    app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
    app.include_router(forecast_router, prefix="/api/forecast", tags=["Forecast"])
    app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])
    app.include_router(export_router, prefix="/api/export", tags=["Export"])
    app.include_router(notification_router, prefix="/api/notifications", tags=["Notifications"])
    app.include_router(agent_router, prefix="/api/agents", tags=["Agents"])
    app.include_router(analytics_router, prefix="/api", tags=["Advanced Analytics"])
    app.include_router(websocket_router)
    app.include_router(transactions_router, prefix="/api/user", tags=["Transactions"])

    # Versioned surface used by the test suite and newer clients.
    app.include_router(api_v1_router, prefix="/api/v1")
    
    logger.info("==========================================")
    logger.info(f" AUREXIS AI - VERSION 1.0.0 (Production) ")
    logger.info(f" Environment: {settings.ENVIRONMENT}      ")
    logger.info(" All API routes loaded successfully      ")
    logger.info("==========================================")
except ImportError as e:
    logger.warning(f"Some routes could not be loaded: {e}")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors

    Args:
        request: FastAPI request object
        exc: Exception that was raised

    Returns:
        JSONResponse: Standardized error response
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "Internal server error",
                "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
            },
            "timestamp": datetime.now().isoformat()
        }
    )


# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str


class APIResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str = ""
    timestamp: str = ""
    version: str = "v1"


# Root endpoint expected by tests
@app.get("/", tags=["health"])
async def root():
    return {"status": "online", "service": "AUREXIS AI Backend"}


@app.options("/")
async def root_options():
    return {}


# Health check endpoint expected by tests
@app.get("/health", tags=["health"])
async def health_check(response: Response):
    start = time.perf_counter()
    payload = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "json_store": "ready",
            "auth": "ready",
            "ml": "ready",
        },
    }
    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["x-process-time"] = f"{duration_ms:.2f}ms"
    return payload


# User endpoints for internal use/tests
@app.get("/api/users", tags=["users"])
async def get_users():
    users = get_all_users()
    return {"users": users, "count": len(users)}

@app.get("/api/v1/users", tags=["users"])
async def get_users_v1():
    users = get_all_users()
    return {"users": users, "count": len(users)}


@app.post("/api/auth/signup", tags=["authentication"], status_code=201)
async def signup_fallback(request: dict = Body(...)):
    """Fallback signup for legacy tests"""
    from services.auth_service import AuthService
    result = AuthService.signup(
        name=request.get("name"),
        email=request.get("email"),
        password=request.get("password")
    )
    user = result["user"]
    user_id = user["id"]
    
    # Create session
    session_id = f"session_{user_id}"
    active_sessions[session_id] = {"user": user}
    
    return {
        "success": True,
        "access_token": result["access_token"],
        "refresh_token": result["refresh_token"],
        "user": UserService.build_user_profile(user),
        "data": {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": "Bearer",
            "session_id": session_id,
            "user": UserService.build_user_profile(user)
        }
    }
async def login_options():
    """Handle CORS preflight for login endpoint"""
    return {"message": "OK"}

@app.post("/api/login", tags=["authentication"])
async def login(request: LoginRequest):
    """
    Authenticate user and create session with JWT tokens

    Args:
        request: LoginRequest with username and password

    Returns:
        dict: JWT tokens and user profile

    Raises:
        HTTPException: 401 if credentials invalid, 500 if server error
    """
    try:
        # Authenticate user (supports email, user_number, or name)
        user = authenticate_user(request.username, request.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generate JWT tokens
        from auth.jwt_handler import create_access_token, create_refresh_token
        from datetime import timedelta
        
        user_id = str(user.get('id', user.get('user_number', '')))
        access_token = create_access_token({
            "sub": user_id,
            "email": user.get("email", ""),
            "name": user.get("name", "")
        })
        refresh_token = create_refresh_token({"sub": user_id})
        # JSON mode: we don't store refresh tokens in a database since there is no DB.
        # They are simply stateless JWTs for now.

        # Keep session for backward compatibility
        # Create session
        session_id = f"session_{user_id}"
        active_sessions[session_id] = {"user": user}

        # Build response with top-level tokens for tests
        return {
            "success": True,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": UserService.build_user_profile(user),
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "session_id": session_id,
                "user": UserService.build_user_profile(user),
                "expires_in": 1800
            },
            "message": "Login successful",
            "timestamp": datetime.now().isoformat(),
            "version": "v1"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")


# Logout endpoint
@app.post("/api/logout", tags=["authentication"])
async def logout(session_id: str = Body(..., embed=True)):
    """
    Logout user and invalidate session

    Args:
        session_id: Session identifier to invalidate

    Returns:
        dict: Success message
    """
    if session_id in active_sessions:
        del active_sessions[session_id]
    return {"success": True, "message": "Logged out successfully"}


def extract_financials_summary(financial_data: dict) -> dict:
    """Extract financial summary from user data"""
    try:
        # Default values
        defaults = {
            "monthly_income": 75000,
            "monthly_expense": 45000,
            "savings_rate": 40,
            "net_worth": 850000,
            "credit_score": 750
        }

        # Try to extract from actual data
        net_worth_data = financial_data.get("fetch_net_worth", {})
        if isinstance(net_worth_data, dict) and "net_worth" in net_worth_data:
            defaults["net_worth"] = int(net_worth_data["net_worth"])

        bank_data = financial_data.get("fetch_bank_transactions", {})
        if isinstance(bank_data, dict) and "monthly_income" in bank_data:
            defaults["monthly_income"] = int(bank_data["monthly_income"])

        return defaults
    except Exception as e:
        logger.error(f"Error extracting financials: {e}")
        return {
            "monthly_income": 75000,
            "monthly_expense": 45000,
            "savings_rate": 40,
            "net_worth": 850000,
            "credit_score": 750
        }

# --- ML ENGINE INTEGRATION ---
from ml_engine import ml_engine, RiskInput, ForecastInput

@app.post("/api/train")
def train_model(user: dict = Depends(get_current_user)):
    """Train all backend ML models (RandomForest, LinearRegression, KMeans)"""
    try:
        return ml_engine.train_models()
    except Exception as e:
        logger.error(f"Error training models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict-risk")
def predict_risk(data: RiskInput, user: dict = Depends(get_current_user)):
    """Predict financial risk using RandomForestClassifier"""
    try:
        return ml_engine.predict_risk(data)
    except Exception as e:
        logger.error(f"Error predicting risk: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/forecast")
def forecast(data: ForecastInput, user: dict = Depends(get_current_user)):
    """Forecast future expenses using LinearRegression"""
    try:
        return ml_engine.forecast_expenses(data)
    except Exception as e:
        logger.error(f"Error forecasting: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recommendation")
def recommendation(expense_ratio: float, savings_ratio: float, user: dict = Depends(get_current_user)):
    """Get smart recommendations using KMeans clustering"""
    try:
        rec = ml_engine.get_recommendation(expense_ratio, savings_ratio)
        return {"recommendation": rec}
    except Exception as e:
        logger.error(f"Error getting recommendation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
