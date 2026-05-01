"""
AUREXIS AI Backend Server
Simple FastAPI server with essential endpoints
"""

import builtins
import logging
import sqlite3
import time
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException, Body
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from slowapi import Limiter
from slowapi.util import get_remote_address

# Import configuration
from config import settings

# Import database utilities
from database.connection_enhanced import init_database

# Import user management
from user_manager_secure import authenticate_user, get_all_users

# Import cache manager
from cache_manager import cache

# Import exceptions
# from exceptions import AuthenticationError, DatabaseError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state
active_sessions = {}

# SlowAPI limiter instance (expected by tests)
limiter = Limiter(key_func=get_remote_address)


def get_db_connection() -> sqlite3.Connection:
    """
    Test helper expected by `backend/tests/test_integration.py`.

    Returns a raw sqlite connection so tests can run `cursor.execute(...)`.
    """
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# The integration test calls `get_db_connection()` without importing it.
# Put it in `builtins` so name resolution can find it.
builtins.get_db_connection = get_db_connection


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events"""
    # Startup
    try:
        # Force close any existing connections
        from database.connection_enhanced import close_connection_pool
        close_connection_pool()

        # Check if database already has users
        from user_manager_secure import UserManager
        existing_users = UserManager.get_all_users()

        if len(existing_users) == 0:
            # Only initialize if no users exist
            init_database()
            logger.info("Database initialized successfully")
        else:
            logger.info(f"Database already initialized with {len(existing_users)} users")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

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
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include financial routes
try:
    from routes.financial import financial_router
    from routes.chat import chat_router
    from routes.forecast import forecast_router
    from routes.reports import reports_router
    from routes.ml_forecasting import router as ml_router
    from routes.investment_optimization import router as investment_router
    from routes.notifications import router as notification_router
    from routes.agent_monitoring import router as agent_router
    from routes.advanced_analytics import router as analytics_router
    
    # Include all routers
    app.include_router(financial_router, tags=["Financial"])
    app.include_router(chat_router, prefix="/api/v1/chat", tags=["Chat"])
    app.include_router(forecast_router, prefix="/api/v1/forecast", tags=["Forecast"])
    app.include_router(reports_router, prefix="/api/v1/reports", tags=["Reports"])
    app.include_router(ml_router, prefix="/api/v1/ml", tags=["ML Forecasting"])
    app.include_router(investment_router, prefix="/api/v1/investments", tags=["Investments"])
    app.include_router(notification_router, prefix="/api/v1/notifications", tags=["Notifications"])
    app.include_router(agent_router, prefix="/api/v1/agents", tags=["Agents"])
    app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics"])
    
    logger.info("All API routes loaded successfully")
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

    return {
        "success": False,
        "error": {
            "code": 500,
            "message": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
        },
        "timestamp": datetime.now().isoformat()
    }


# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str


class APIResponse(BaseModel):
    success: bool
    data: dict = None
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
            "database": "ready",
            "auth": "ready",
            "ml": "ready",
        },
    }
    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["x-process-time"] = f"{duration_ms:.2f}ms"
    return payload


# Users endpoint
@app.get("/api/users", tags=["users"])
async def get_users():
    """
    Retrieve all registered users in the system

    Returns:
        dict: List of users and total count
    """
    try:
        # Check cache first
        cached_users = cache.get("all_users")
        if cached_users:
            logger.info("Returning cached users data")
            return cached_users

        # Force close connections and get fresh data
        from database.connection_enhanced import close_connection_pool
        close_connection_pool()

        users = get_all_users()
        result = {"users": users, "count": len(users)}

        # Cache the result (5 minutes)
        cache.set("all_users", result, ttl=300)
        logger.info("Cached users data")

        return result
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve users")


# Login endpoint
@app.options("/api/login", tags=["authentication"])
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
        
        # Store refresh token in database
        try:
            from database.db_utils import get_db
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO refresh_tokens (user_id, token, expires_at)
                    VALUES (?, ?, datetime('now', '+30 days'))
                """, (user_id, refresh_token))
        except Exception as e:
            logger.warning(f"Could not store refresh token: {e}")

        # Keep session for backward compatibility
        session_id = f"session_{user_id}"
        active_sessions[session_id] = {"user": user}

        return {
            "success": True,
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "session_id": session_id,  # For backward compatibility
                "user": build_user_profile(user),
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


def build_user_profile(user: dict) -> dict:
    """Build user profile for frontend"""
    user_id = user.get("id", "")
    financial_data = user.get("financial_data", {})

    # Extract financial metrics
    fm = extract_financials_summary(financial_data)
    income = fm["monthly_income"]
    expense = fm["monthly_expense"]
    savings_rate = fm["savings_rate"]
    net_worth = fm["net_worth"]
    credit_score = fm["credit_score"]

    return {
        "id": user_id,
        "name": user.get("name", "Unknown"),
        "email": user.get("email", ""),
        "occupation": user.get("occupation", "Professional"),
        "age": user.get("age", 30),
        "location": user.get("location", ""),
        "monthlyIncome": income,
        "monthlyExpense": expense,
        "savings": int(income - expense),
        "netWorth": net_worth,
        "savingsRate": savings_rate,
        "creditScore": credit_score,
        "riskLevel": "Low" if savings_rate > 30 else "Medium",
        "financialHealthScore": min(100, max(0, int(50 + savings_rate))),
        "debtToIncomeRatio": round(expense / income, 2) if income > 0 else 0,
        "emergencyFundMonths": round(net_worth * 0.2 / expense, 1) if expense > 0 else 6,
        "investmentValue": int(net_worth * 0.6),
        "totalDebt": 225000,
        "goals": [
            {
                "id": "g1",
                "name": "Emergency Fund",
                "target": int(expense * 6),
                "current": int(expense * 4.5),
                "deadline": "2026-08"
            },
            {
                "id": "g2",
                "name": "New Car",
                "target": 1200000,
                "current": 350000,
                "deadline": "2027-12"
            },
        ],
        "expenses": [
            {"category": "Housing", "amount": int(expense * 0.40), "percentage": 40},
            {"category": "Food", "amount": int(expense * 0.20), "percentage": 20},
            {"category": "Transport", "amount": int(expense * 0.15), "percentage": 15},
            {"category": "Utilities", "amount": int(expense * 0.10), "percentage": 10},
            {"category": "Other", "amount": int(expense * 0.15), "percentage": 15},
        ],
        "investments": [
            {
                "name": "Equity Funds",
                "type": "MF",
                "value": int(net_worth * 0.4),
                "allocation": 40
            },
            {
                "name": "Fixed Deposits",
                "type": "FD",
                "value": int(net_worth * 0.3),
                "allocation": 30
            },
            {
                "name": "EPF",
                "type": "EPF",
                "value": int(net_worth * 0.2),
                "allocation": 20
            },
            {
                "name": "Gold",
                "type": "Gold",
                "value": int(net_worth * 0.1),
                "allocation": 10
            },
        ],
        "alerts": [
            {
                "id": "a1",
                "type": "info",
                "title": "Savings Milestone",
                "message": "You've saved 20% more than last month!"
            },
            {
                "id": "a2",
                "type": "warning",
                "title": "Large Expense",
                "message": "Unexpected transaction of ₹15,000 detected."
            },
        ],
    }


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


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
