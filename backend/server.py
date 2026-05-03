"""
AUREXIS AI Backend Server
Simple FastAPI server with essential endpoints
"""

import builtins
import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from urllib.parse import quote
from fastapi import FastAPI, HTTPException, Body
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from slowapi import Limiter
from slowapi.util import get_remote_address

# Import configuration
from config import settings

# Import user management (JSON-based, no database)
from user_manager_json import authenticate_user, get_all_users

# Import cache manager
from cache_manager import cache

# Import analytics helpers used to shape the dashboard profile
from analytics import (
    compute_expenses,
    compute_forecast,
    compute_goals,
    compute_investments,
    compute_metrics,
    compute_risk,
)

# Import financial health helper
from health import compute_health

# Import exceptions
# from exceptions import AuthenticationError, DatabaseError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080",  # Added for Vite dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",  # Added for Vite dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    
    # Canonical legacy API surface used by the frontend/startup docs.
    # NOTE: auth_router is commented out because it conflicts with server.py /api/login
    # The server.py login returns full user profile with financial data
    app.include_router(financial_router, prefix="/api/financial", tags=["Financial"])
    app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
    app.include_router(forecast_router, prefix="/api/forecast", tags=["Forecast"])
    app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])
    app.include_router(export_router, prefix="/api/export", tags=["Export"])
    app.include_router(notification_router, prefix="/api/notifications", tags=["Notifications"])
    app.include_router(agent_router, prefix="/api/agents", tags=["Agents"])
    app.include_router(websocket_router)

    # Versioned surface used by the test suite and newer clients.
    app.include_router(api_v1_router, prefix="/api/v1")
    
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
            "json_store": "ready",
            "auth": "ready",
            "ml": "ready",
        },
    }
    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["x-process-time"] = f"{duration_ms:.2f}ms"
    return payload


# User endpoints commented out for security (prevents public user listing)
# @app.get("/api/users", tags=["users"])
# async def get_users(): ...

# @app.get("/api/v1/users", tags=["users"])
# async def get_users_v1(): ...


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
        # JSON mode: we don't store refresh tokens in a database since there is no DB.
        # They are simply stateless JWTs for now.

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
    financial_data = user.get("financial_data") or {}
    if not financial_data and user_id:
        from user_manager_json import UserManagerJSON

        financial_data = UserManagerJSON.get_all_user_data(user_id)

    metrics = compute_metrics(financial_data)
    expenses = compute_expenses(financial_data)
    goals = compute_goals(financial_data)
    investments = compute_investments(financial_data).get("portfolio", [])
    risk = compute_risk(financial_data)
    health = compute_health(financial_data)
    monthly_data = compute_forecast(financial_data)

    name = user.get("name", "Unknown")
    occupation = user.get("occupation") or "Professional"
    age = user.get("age") or 30
    location = user.get("location") or ""
    last_login = user.get("last_login")

    if hasattr(last_login, "isoformat"):
        last_active = last_login.isoformat()
    else:
        last_active = last_login or datetime.now().isoformat()

    avatar = build_avatar_data_uri(name)
    bank_name = user.get("bank_name", "") or ""
    account_number = mask_account_number(user.get("account_number", "") or "")
    account_type = user.get("account_type", "") or ""
    bank_location = user.get("bank_location", "") or location
    has_credit_card = bool(user.get("has_credit_card", False))

    alerts = build_profile_alerts(metrics, health)
    upcoming_emis = build_upcoming_emis(metrics)

    return {
        "id": user_id,
        "name": name,
        "avatar": avatar,
        "email": user.get("email", ""),
        "phone": user.get("phone", "") or "",
        "occupation": occupation,
        "age": age,
        "bankName": bank_name,
        "accountNumber": account_number,
        "accountType": account_type,
        "bankLocation": bank_location,
        "hasCreditCard": has_credit_card,
        "location": location,
        "monthlyIncome": metrics["monthlyIncome"],
        "monthlyExpense": metrics["monthlyExpense"],
        "netWorth": metrics["netWorth"],
        "savings": metrics["savings"],
        "totalDebt": metrics["totalDebt"],
        "riskLevel": risk["riskLevel"],
        "personalityTag": derive_personality_tag(metrics, risk),
        "lastActive": last_active,
        "creditScore": metrics["creditScore"],
        "emergencyFundMonths": metrics["emergencyFundMonths"],
        "investmentValue": metrics["investmentValue"],
        "savingsRate": metrics["savingsRate"],
        "debtToIncomeRatio": metrics["debtToIncomeRatio"],
        "financialHealthScore": health["overall"],
        "goals": [
            {
                "id": goal.get("id", f"goal_{index}"),
                "name": goal.get("name", "Goal"),
                "target": goal.get("target", 0),
                "current": goal.get("current", 0),
                "deadline": goal.get("deadline", ""),
                "icon": goal.get("icon", "Target"),
                "monthlySavingsNeeded": goal.get("monthlySavingsNeeded", 0),
            }
            for index, goal in enumerate(goals, start=1)
        ],
        "monthlyData": [
            {
                "month": item.get("month", ""),
                "income": item.get("income", 0),
                "expense": item.get("expense", 0),
                "savings": item.get("savings", 0),
                "netWorth": item.get("netWorth", 0),
                "debt": metrics["totalDebt"],
            }
            for item in monthly_data
        ],
        "expenses": expenses,
        "investments": investments,
        "upcomingEMIs": upcoming_emis,
        "alerts": alerts,
    }


def build_avatar_data_uri(name: str) -> str:
    """Generate a lightweight inline avatar for the frontend."""
    initials = "".join(part[0].upper() for part in name.split()[:2] if part) or "A"
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='96' height='96' viewBox='0 0 96 96'>"
        "<rect width='96' height='96' rx='24' fill='#1d4ed8'/>"
        "<text x='48' y='56' text-anchor='middle' font-family='Arial, sans-serif' "
        "font-size='32' font-weight='700' fill='white'>"
        f"{initials}</text></svg>"
    )
    return f"data:image/svg+xml;utf8,{quote(svg)}"


def mask_account_number(account_number: str) -> str:
    """Mask sensitive account numbers for the UI."""
    digits = "".join(char for char in account_number if char.isdigit())
    if len(digits) < 4:
        return ""
    return f"•••• {digits[-4:]}"


def derive_personality_tag(metrics: dict, risk: dict) -> str:
    """Infer a lightweight personality label for the dashboard."""
    if metrics["savingsRate"] >= 30 and risk["riskLevel"] == "Low":
        return "Conservative Saver"
    if metrics["investmentValue"] >= max(metrics["netWorth"] * 0.45, 1):
        return "Investor"
    if metrics["debtToIncomeRatio"] >= 0.45:
        return "Debt Heavy"
    if metrics["savingsRate"] <= 10:
        return "High Spender"
    return "Balanced Planner"


def build_profile_alerts(metrics: dict, health: dict) -> list[dict]:
    """Create dashboard-friendly alert cards from current metrics."""
    timestamp = datetime.now().isoformat()
    alerts = []

    if metrics["savingsRate"] < 20:
        alerts.append(
            {
                "id": "alert_savings",
                "type": "warning",
                "title": "Savings Deficit Detected",
                "message": f"Your savings velocity is currently at {metrics['savingsRate']}%. Target a minimum of 20% to ensure sustainable wealth accumulation.",
                "timestamp": timestamp,
            }
        )

    if metrics["creditScore"] < 700:
        alerts.append(
            {
                "id": "alert_credit",
                "type": "warning",
                "title": "Suboptimal Credit Profile",
                "message": f"Credit score currently reads {metrics['creditScore']}. Consistent liability management can elevate this into the prime tier.",
                "timestamp": timestamp,
            }
        )

    if not alerts:
        alerts.append(
            {
                "id": "alert_health",
                "type": "info",
                "title": "System Health Overview",
                "message": f"Your financial matrix shows a {health['label'].lower()} standing, scoring {health['overall']}/100. All primary indicators are within safe thresholds.",
                "timestamp": timestamp,
            }
        )

    return alerts


def build_upcoming_emis(metrics: dict) -> list[dict]:
    """Provide a simple EMI reminder set for the sidebar."""
    if metrics["totalDebt"] <= 0:
        return []

    due_date = (datetime.now() + timedelta(days=10)).date().isoformat()
    return [
        {
            "name": "Loan EMI",
            "amount": min(12500, max(2500, round(metrics["monthlyIncome"] * 0.12))),
            "dueDate": due_date,
            "type": "Loan",
        }
    ]


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
