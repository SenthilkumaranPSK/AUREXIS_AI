"""
FastAPI Backend Server for AUREXIS AI
Handles user authentication and Ollama LLM integration
"""

import json
import os
import httpx
from pathlib import Path
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from user_manager import (
    authenticate_user,
    get_all_users,
    get_user_by_name,
    get_user_by_id,
    get_all_user_data,
    load_user_data,
)
from analytics_legacy import (
    compute_metrics,
    compute_forecast,
    compute_expenses,
    compute_investments,
    compute_goals,
    compute_risk,
    compute_simulation,
    extract_financials_summary,
)
from recommendations_legacy import generate_recommendations
from alerts import generate_alerts, generate_emis
from health import compute_health
from forecasting import (
    compute_monthly_forecast,
    compute_net_worth_forecast,
    compute_goal_forecast,
    compute_expense_forecast,
    compute_savings_projection,
)
from report import generate_report
from ml_forecasting import compute_ml_forecast
from portfolio import compute_stocks, compute_mutual_funds
from budget_optimizer import budget_optimizer
from credit_score_predictor import credit_score_predictor
from tax_planner import tax_planner
from fraud_detector import fraud_detector
from realtime_alerts import realtime_alert_system
from multi_agent_system import multi_agent_coordinator
from explainable_recommendations import explainable_recommendation_engine
from chat_memory import chat_memory_manager
import uuid

# NEW: Import modular routes
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
from routes.websocket_routes import router as websocket_router
from routes.agent_monitoring import router as agent_monitoring_router
from database.connection import init_database
from middleware.logging_middleware import LoggingMiddleware
from middleware.validation_middleware import ValidationMiddleware
from middleware.caching_middleware import CachingMiddleware
from config import settings

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "deepseek-v3.1:671b-cloud")


# --- Pydantic Models ---

class LoginRequest(BaseModel):
    username: str
    password: str

class ChatMessage(BaseModel):
    user_id: str
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = None
    session_id: Optional[str] = None
    use_memory: bool = True


# --- Global state ---

active_sessions: Dict[str, Dict[str, Any]] = {}
conversation_history: Dict[str, List[Dict[str, str]]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"AUREXIS AI Backend starting — model: {OLLAMA_MODEL}")

    # Initialize database on startup
    try:
        init_database()
        logger.info("Database initialized")
    except Exception as e:
        logger.warning(f"Database initialization warning: {e}")

    yield
    logger.info("Server shutting down...")


# --- App ---

# Initialize rate limiter with stricter limits for auth endpoints
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

# Stricter rate limit for authentication endpoints (5 requests per minute)
AUTH_RATE_LIMIT = "5/minute"

app = FastAPI(
    title="AUREXIS AI Backend",
    description="AI-powered financial planning and analysis API",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# IMPORTANT: CORS middleware MUST be added FIRST to handle preflight requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Must be False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add other middlewares AFTER CORS
app.add_middleware(LoggingMiddleware)
app.add_middleware(ValidationMiddleware)
app.add_middleware(CachingMiddleware)


# ==================== NEW MODULAR ROUTES ====================
# Register new API routes with proper authentication and validation
app.include_router(auth_router)
app.include_router(financial_router)
app.include_router(forecast_router)
app.include_router(chat_router)
app.include_router(reports_router)

# Phase 3: Advanced Features Routes
app.include_router(advanced_analytics_router)
app.include_router(ml_forecasting_router)
app.include_router(investment_optimization_router)

# Phase 4: AI & Intelligence Routes
app.include_router(notifications_router)
app.include_router(websocket_router)
app.include_router(agent_monitoring_router)

logger.info("New API routes registered:")
logger.info("  - /api/auth (7 endpoints)")
logger.info("  - /api/financial (20+ endpoints)")
logger.info("  - /api/forecast (7 endpoints)")
logger.info("  - /api/chat (7 endpoints)")
logger.info("  - /api/reports (5 endpoints)")
logger.info("  - /api/analytics (9 endpoints) [Phase 3]")
logger.info("  - /api/ml (9 endpoints) [Phase 3]")
logger.info("  - /api/investments (10 endpoints) [Phase 3]")
logger.info("  - /api/notifications (12 endpoints) [Phase 4]")
logger.info("  - /ws (WebSocket + 3 endpoints) [Phase 4]")
logger.info("  - /api/agents (9 endpoints) [Phase 4]")
# ============================================================


# --- Endpoints ---

@app.get("/")
@limiter.limit("60/minute")
async def root(request: Request):
    return {"status": "online", "service": "AUREXIS AI Backend", "model": OLLAMA_MODEL}


@app.get("/health")
@limiter.limit("30/minute")
async def health_check(request: Request):
    """Health check endpoint for monitoring"""
    from datetime import datetime
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "AUREXIS AI Backend",
        "version": "2.0",
        "model": OLLAMA_MODEL,
        "components": {
            "api": "healthy",
            "database": "healthy"
        }
    }


@app.get("/api/users")
async def get_users():
    users = get_all_users()
    return {"users": users, "count": len(users)}


@app.post("/api/login")
async def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials. Username and password must match.")

    session_id = f"session_{user['id']}"
    active_sessions[session_id] = {"user": user}

    return {
        "success": True,
        "session_id": session_id,
        "user": build_user_profile(user),
    }


@app.post("/api/logout")
async def logout(session_id: str = Body(..., embed=True)):
    if session_id in active_sessions:
        del active_sessions[session_id]
        # Clear conversation history on logout
        user_id = session_id.replace("session_", "")
        conversation_history.pop(user_id, None)
        return {"success": True}
    return {"success": False, "message": "Session not found"}


@app.get("/api/user/{user_id}/data/{data_type}")
async def get_user_data(user_id: str, data_type: str):
    data = load_user_data(user_id, data_type)
    if data is None:
        raise HTTPException(status_code=404, detail=f"'{data_type}' not found for user {user_id}")
    return {"user_id": user_id, "data_type": data_type, "data": data}


@app.get("/api/user/{user_id}/data")
async def get_all_user_data_endpoint(user_id: str):
    return {"user_id": user_id, "data": get_all_user_data(user_id)}


@app.post("/api/chat")
async def chat(request: ChatMessage):
    # Use the proper identifier (user_number) to fetch user data
    user_id = request.user_id
    # Try to locate the user by numeric ID first, then by name
    user = get_user_by_id(user_id) or get_user_by_name(user_id)
    if not user:
        # Fallback to a minimal placeholder – this will result in empty data
        user = {"number": user_id, "name": "User"}
    # The user dict contains the key "user_number" (or "number" after login). Use it to load data.
    user_number = user.get("user_number") or user.get("number") or user_id
    financial_data = get_all_user_data(user_number)
    
    # Generate session ID if not provided
    session_id = request.session_id or f"session_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    try:
        # Save user message to memory if enabled
        if request.use_memory:
            chat_memory_manager.save_message(
                user_id=user_id,
                role="user",
                message=request.message,
                session_id=session_id,
                metadata={
                    "timestamp": datetime.now().isoformat(),
                    "has_financial_data": bool(financial_data)
                }
            )
        
        # Get response from Ollama with memory context
        response = await call_ollama(
            request.message, 
            user, 
            financial_data,
            user_id=user_id,
            use_memory=request.use_memory
        )
        
        # Save assistant response to memory if enabled
        if request.use_memory:
            chat_memory_manager.save_message(
                user_id=user_id,
                role="assistant",
                message=response.get("content", ""),
                session_id=session_id,
                metadata={
                    "timestamp": datetime.now().isoformat(),
                    "confidence": response.get("confidence", 0)
                }
            )
        
        return {
            "success": True, 
            "response": response, 
            "user_id": user_id,
            "session_id": session_id
        }
    except Exception as e:
        print(f"Ollama Error: {e}")
        import traceback; traceback.print_exc()
        return {
            "success": False,
            "response": {
                "summary": "Service Unavailable",
                "content": "Could not reach Ollama. Make sure it is running with: ollama serve",
                "insights": [], "recommendations": [], "confidence": 0,
            },
            "user_id": user_id,
            "session_id": session_id
        }


# --- Analytics Endpoints ---

@app.get("/api/user/{user_id}/metrics")
async def get_metrics(user_id: str):
    """Key financial metrics computed from raw data."""
    data = get_all_user_data(user_id)
    return compute_metrics(data)


@app.get("/api/user/{user_id}/forecast")
async def get_forecast(user_id: str):
    """12-month historical + 6-month projected forecast."""
    data = get_all_user_data(user_id)
    return {"forecast": compute_forecast(data)}


@app.get("/api/user/{user_id}/expenses")
async def get_expenses(user_id: str):
    """Expense breakdown by category."""
    data = get_all_user_data(user_id)
    return {"expenses": compute_expenses(data)}


@app.get("/api/user/{user_id}/investments")
async def get_investments(user_id: str):
    """Investment portfolio breakdown."""
    data = get_all_user_data(user_id)
    return compute_investments(data)


@app.get("/api/user/{user_id}/goals")
async def get_goals(user_id: str):
    """Financial goals with progress."""
    data = get_all_user_data(user_id)
    return {"goals": compute_goals(data)}


@app.get("/api/user/{user_id}/risk")
async def get_risk(user_id: str):
    """Detailed risk analysis."""
    data = get_all_user_data(user_id)
    return compute_risk(data)


class SimulationRequest(BaseModel):
    new_loan: float = 0
    salary_increase: float = 0
    job_loss: bool = False
    vacation_expense: float = 0
    house_purchase: bool = False
    car_purchase: bool = False
    investment_increase: float = 0


@app.post("/api/user/{user_id}/simulation")
async def run_simulation(user_id: str, params: SimulationRequest):
    """Run scenario simulation with given parameters."""
    data = get_all_user_data(user_id)
    return compute_simulation(
        data,
        new_loan=params.new_loan,
        salary_increase=params.salary_increase,
        job_loss=params.job_loss,
        vacation_expense=params.vacation_expense,
        house_purchase=params.house_purchase,
        car_purchase=params.car_purchase,
        investment_increase=params.investment_increase,
    )


@app.get("/api/user/{user_id}/health")
async def get_health(user_id: str):
    """Detailed financial health score with sub-scores."""
    data = get_all_user_data(user_id)
    return compute_health(data)


@app.get("/api/user/{user_id}/recommendations")
async def get_recommendations(user_id: str):
    """Personalized financial recommendations from real data."""
    data = get_all_user_data(user_id)
    return {"recommendations": generate_recommendations(data)}


@app.get("/api/user/{user_id}/alerts")
async def get_alerts(user_id: str):
    """Real-time financial alerts generated from data patterns."""
    data = get_all_user_data(user_id)
    return {
        "alerts": generate_alerts(data),
        "emis": generate_emis(data),
    }


# --- Forecasting Endpoints ---

@app.get("/api/user/{user_id}/forecast/monthly")
async def get_monthly_forecast(user_id: str, months: int = 6):
    """Historical + projected monthly income/expense/savings."""
    data = get_all_user_data(user_id)
    return {"forecast": compute_monthly_forecast(data, months)}


@app.get("/api/user/{user_id}/forecast/networth")
async def get_networth_forecast(user_id: str, years: int = 5):
    """Multi-year net worth projection."""
    data = get_all_user_data(user_id)
    return {"forecast": compute_net_worth_forecast(data, years)}


@app.get("/api/user/{user_id}/forecast/goals")
async def get_goal_forecast(user_id: str):
    """Goal completion timeline forecast."""
    data = get_all_user_data(user_id)
    return {"goals": compute_goal_forecast(data)}


@app.get("/api/user/{user_id}/forecast/expenses")
async def get_expense_forecast(user_id: str, months: int = 6):
    """Category-wise expense trend forecast."""
    data = get_all_user_data(user_id)
    return {"categories": compute_expense_forecast(data, months)}


@app.get("/api/user/{user_id}/forecast/savings")
async def get_savings_projection(user_id: str):
    """Savings projection at different contribution rates."""
    data = get_all_user_data(user_id)
    return compute_savings_projection(data)


# --- Report Endpoint ---

@app.get("/api/user/{user_id}/report")
async def get_report(user_id: str):
    """Generate complete financial report for a user."""
    user = get_user_by_id(user_id) or get_user_by_name(user_id) or {"name": "User", "number": user_id}
    data = get_all_user_data(user_id)
    return generate_report(user, data)


# --- Portfolio Endpoints ---

@app.get("/api/user/{user_id}/stocks")
async def get_stocks(user_id: str):
    """Stock portfolio with holdings, P&L, sector breakdown."""
    data = get_all_user_data(user_id)
    return compute_stocks(data)


@app.get("/api/user/{user_id}/mutual-funds")
async def get_mutual_funds(user_id: str):
    """Mutual fund portfolio with scheme-wise returns and XIRR."""
    data = get_all_user_data(user_id)
    return compute_mutual_funds(data)


# --- ML Forecasting Endpoint ---

@app.get("/api/user/{user_id}/forecast/ml")
async def get_ml_forecast(user_id: str, steps: int = 6):
    """ML-based forecast using ARIMA, LSTM, Random Forest, Gradient Boosting."""
    data = get_all_user_data(user_id)
    return compute_ml_forecast(data, steps)


# --- Budget Optimizer Endpoints ---

@app.get("/api/user/{user_id}/budget/analyze")
async def analyze_spending_patterns(user_id: str):
    """Analyze spending patterns and provide insights."""
    data = get_all_user_data(user_id)
    transactions = data.get("fetch_bank_transactions", {}).get("transactions", [])
    
    analysis = budget_optimizer.analyze_spending_patterns(transactions)
    return {
        "user_id": user_id,
        "analysis": analysis,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/user/{user_id}/budget/predict")
async def predict_expenses(user_id: str, months_ahead: int = 3):
    """Predict future expenses using ML."""
    data = get_all_user_data(user_id)
    transactions = data.get("fetch_bank_transactions", {}).get("transactions", [])
    
    predictions = budget_optimizer.predict_future_expenses(transactions, months_ahead)
    return {
        "user_id": user_id,
        "predictions": predictions,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/user/{user_id}/budget/optimize")
async def optimize_budget(user_id: str):
    """Get optimal budget allocation recommendations."""
    data = get_all_user_data(user_id)
    
    # Extract income
    fm = extract_financials_summary(data)
    income = fm["monthly_income"]
    
    # Extract current spending by category
    transactions = data.get("fetch_bank_transactions", {}).get("transactions", [])
    current_spending = {}
    
    for txn in transactions:
        if txn.get("type") == "debit":
            category = txn.get("category", "Other")
            amount = abs(float(txn.get("amount", 0)))
            current_spending[category] = current_spending.get(category, 0) + amount
    
    # Normalize to monthly (assuming data is for multiple months)
    num_months = len(set(txn.get("date", "")[:7] for txn in transactions if txn.get("date")))
    if num_months > 0:
        current_spending = {k: v / num_months for k, v in current_spending.items()}
    
    # Get financial goals
    goals_data = compute_goals(data).get("goals", [])
    financial_goals = [
        {
            "target_amount": goal.get("target", 0) - goal.get("current", 0),
            "months_remaining": max(1, int((datetime.strptime(goal.get("deadline", "2026-12-31"), "%Y-%m-%d") - datetime.now()).days / 30))
        }
        for goal in goals_data
    ]
    
    optimization = budget_optimizer.suggest_optimal_budget(
        income=income,
        current_spending=current_spending,
        financial_goals=financial_goals if financial_goals else None
    )
    
    return {
        "user_id": user_id,
        "optimization": optimization,
        "timestamp": datetime.now().isoformat()
    }


class AutoCategorizeRequest(BaseModel):
    description: str
    amount: float


@app.post("/api/budget/categorize")
async def auto_categorize(request: AutoCategorizeRequest):
    """Auto-categorize a transaction using AI."""
    category = budget_optimizer.auto_categorize_transaction(
        request.description,
        request.amount
    )
    return {
        "description": request.description,
        "amount": request.amount,
        "suggested_category": category
    }


class SavingsPlanRequest(BaseModel):
    user_id: str
    target_amount: float
    months: int


@app.post("/api/budget/savings-plan")
async def create_savings_plan(request: SavingsPlanRequest):
    """Generate a personalized savings plan."""
    data = get_all_user_data(request.user_id)
    fm = extract_financials_summary(data)
    
    current_savings = fm["net_worth"] * 0.2  # Assume 20% is liquid savings
    current_monthly_savings = fm["monthly_savings"]
    
    plan = budget_optimizer.generate_savings_plan(
        current_savings=current_savings,
        target_amount=request.target_amount,
        months=request.months,
        current_monthly_savings=current_monthly_savings
    )
    
    return {
        "user_id": request.user_id,
        "plan": plan,
        "timestamp": datetime.now().isoformat()
    }


# --- Credit Score Predictor Endpoints ---

@app.get("/api/user/{user_id}/credit-score/predict")
async def predict_credit_score(user_id: str):
    """Predict future credit score and get improvement recommendations."""
    data = get_all_user_data(user_id)
    prediction = credit_score_predictor.predict_credit_score(data)
    
    return {
        "user_id": user_id,
        "prediction": prediction,
        "timestamp": datetime.now().isoformat()
    }


# --- Tax Planning Endpoints ---

class TaxCalculationRequest(BaseModel):
    annual_income: float
    regime: str = "new"
    deductions: Optional[Dict[str, float]] = None


@app.post("/api/tax/calculate")
async def calculate_tax(request: TaxCalculationRequest):
    """Calculate tax liability under new or old regime."""
    result = tax_planner.calculate_tax_liability(
        annual_income=request.annual_income,
        regime=request.regime,
        deductions=request.deductions
    )
    return result


@app.post("/api/tax/compare-regimes")
async def compare_tax_regimes(request: TaxCalculationRequest):
    """Compare tax liability between old and new regime."""
    result = tax_planner.compare_tax_regimes(
        annual_income=request.annual_income,
        potential_deductions=request.deductions or {}
    )
    return result


@app.get("/api/user/{user_id}/tax/analyze")
async def analyze_tax_efficiency(user_id: str):
    """Analyze overall tax efficiency and provide optimization suggestions."""
    data = get_all_user_data(user_id)
    analysis = tax_planner.analyze_tax_efficiency(data)
    
    return {
        "user_id": user_id,
        "analysis": analysis,
        "timestamp": datetime.now().isoformat()
    }


class TaxInvestmentRequest(BaseModel):
    annual_income: float
    current_investments: Dict[str, float]
    risk_profile: str = "moderate"


@app.post("/api/tax/investment-suggestions")
async def get_tax_investment_suggestions(request: TaxInvestmentRequest):
    """Get tax-saving investment suggestions."""
    suggestions = tax_planner.suggest_tax_saving_investments(
        annual_income=request.annual_income,
        current_investments=request.current_investments,
        risk_profile=request.risk_profile
    )
    return suggestions


@app.post("/api/tax/advance-tax")
async def calculate_advance_tax(request: TaxCalculationRequest):
    """Calculate advance tax payment schedule."""
    schedule = tax_planner.calculate_advance_tax(
        annual_income=request.annual_income,
        regime=request.regime
    )
    return schedule


# --- Fraud Detection Endpoints ---

class TransactionAnalysisRequest(BaseModel):
    user_id: str
    transaction: Dict[str, Any]


@app.post("/api/fraud/analyze-transaction")
async def analyze_transaction_fraud(request: TransactionAnalysisRequest):
    """Analyze a single transaction for fraud indicators."""
    data = get_all_user_data(request.user_id)
    transactions = data.get("fetch_bank_transactions", {}).get("transactions", [])
    user_profile = get_user_by_id(request.user_id) or {}
    
    analysis = fraud_detector.analyze_transaction(
        transaction=request.transaction,
        user_history=transactions,
        user_profile=user_profile
    )
    
    return {
        "user_id": request.user_id,
        "analysis": analysis,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/user/{user_id}/fraud/report")
async def get_fraud_report(user_id: str):
    """Generate comprehensive fraud analysis report."""
    data = get_all_user_data(user_id)
    transactions = data.get("fetch_bank_transactions", {}).get("transactions", [])
    user_profile = get_user_by_id(user_id) or {}
    
    report = fraud_detector.generate_fraud_report(transactions, user_profile)
    
    return {
        "user_id": user_id,
        "report": report,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/user/{user_id}/fraud/account-takeover")
async def check_account_takeover(user_id: str):
    """Check for potential account takeover attempts."""
    data = get_all_user_data(user_id)
    transactions = data.get("fetch_bank_transactions", {}).get("transactions", [])
    user_profile = get_user_by_id(user_id) or {}
    
    analysis = fraud_detector.detect_account_takeover(transactions[-20:], user_profile)
    
    return {
        "user_id": user_id,
        "analysis": analysis,
        "timestamp": datetime.now().isoformat()
    }


# --- Real-time Alerts Endpoints ---

@app.get("/api/user/{user_id}/alerts/realtime")
async def get_realtime_alerts(user_id: str):
    """Get real-time financial alerts."""
    data = get_all_user_data(user_id)
    user_profile = get_user_by_id(user_id) or {}
    
    alerts = realtime_alert_system.generate_realtime_alerts(data, user_profile)
    summary = realtime_alert_system.get_alert_summary(alerts)
    
    return {
        "user_id": user_id,
        "alerts": alerts,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }


# --- Multi-Agent System Endpoints ---

class WorkflowRequest(BaseModel):
    workflow_type: str
    data: Dict[str, Any]


@app.post("/api/multi-agent/workflow")
async def execute_workflow(user_id: str, request: WorkflowRequest):
    """Execute a multi-agent workflow."""
    # Get user data
    financial_data = get_all_user_data(user_id)
    user_profile = get_user_by_id(user_id) or {}
    
    # Merge with request data
    workflow_data = {
        **request.data,
        "transactions": financial_data.get("fetch_bank_transactions", {}).get("transactions", []),
        "user_profile": user_profile,
        "monthly_income": financial_data.get("monthly_income", 0),
        "monthly_expense": financial_data.get("monthly_expense", 0),
        "net_worth": financial_data.get("fetch_net_worth", {}).get("totalAssets", 0),
    }
    
    result = await multi_agent_coordinator.execute_workflow(
        workflow_type=request.workflow_type,
        data=workflow_data
    )
    
    return {
        "user_id": user_id,
        **result
    }


@app.get("/api/multi-agent/status")
async def get_agent_status():
    """Get status of all AI agents."""
    return multi_agent_coordinator.get_agent_status()


@app.get("/api/multi-agent/workflows")
async def list_workflows():
    """List available workflows."""
    return {
        "workflows": [
            {
                "type": "comprehensive_analysis",
                "description": "Complete financial analysis with spending, income, trends, recommendations, and risk assessment",
                "agents_involved": ["analyst", "advisor"],
                "estimated_time": "2-3 seconds"
            },
            {
                "type": "goal_planning",
                "description": "Create detailed plan to achieve financial goals with milestones and budget",
                "agents_involved": ["planner", "advisor"],
                "estimated_time": "1-2 seconds"
            },
            {
                "type": "financial_checkup",
                "description": "Complete health checkup with spending analysis, anomalies, risk assessment, and projections",
                "agents_involved": ["analyst", "advisor", "planner"],
                "estimated_time": "2-3 seconds"
            }
        ]
    }


# --- Explainable Recommendations Endpoints ---

@app.get("/api/user/{user_id}/recommendations/explainable")
async def get_explainable_recommendations(user_id: str):
    """Get recommendations with full explanations and reasoning."""
    financial_data = get_all_user_data(user_id)
    user_profile = get_user_by_id(user_id) or {}
    
    recommendations = explainable_recommendation_engine.generate_recommendations(
        financial_data=financial_data,
        user_profile=user_profile
    )
    
    return {
        "user_id": user_id,
        "recommendations": [rec.to_dict() for rec in recommendations],
        "total_count": len(recommendations),
        "timestamp": datetime.now().isoformat()
    }


# --- Chat Memory Endpoints ---

@app.get("/api/user/{user_id}/chat/history")
async def get_chat_history(
    user_id: str,
    limit: int = 50,
    session_id: Optional[str] = None,
    days: Optional[int] = None
):
    """Get conversation history for a user."""
    history = chat_memory_manager.get_conversation_history(
        user_id=user_id,
        limit=limit,
        session_id=session_id,
        days=days
    )
    
    return {
        "user_id": user_id,
        "history": history,
        "count": len(history),
        "session_id": session_id
    }


@app.get("/api/user/{user_id}/chat/sessions")
async def get_chat_sessions(user_id: str, limit: int = 20):
    """Get list of conversation sessions for a user."""
    sessions = chat_memory_manager.get_conversation_sessions(
        user_id=user_id,
        limit=limit
    )
    
    return {
        "user_id": user_id,
        "sessions": sessions,
        "count": len(sessions)
    }


@app.get("/api/user/{user_id}/chat/stats")
async def get_chat_stats(user_id: str):
    """Get conversation statistics for a user."""
    stats = chat_memory_manager.get_conversation_stats(user_id)
    
    return {
        "user_id": user_id,
        "stats": stats
    }


@app.get("/api/user/{user_id}/chat/preferences")
async def get_chat_preferences(user_id: str):
    """Get user preferences extracted from conversation history."""
    preferences = chat_memory_manager.get_user_preferences(user_id)
    
    return {
        "user_id": user_id,
        "preferences": preferences
    }


@app.post("/api/user/{user_id}/chat/search")
async def search_chat_history(
    user_id: str,
    search_term: str = Body(..., embed=True),
    limit: int = 20
):
    """Search conversation history for a term."""
    results = chat_memory_manager.search_conversations(
        user_id=user_id,
        search_term=search_term,
        limit=limit
    )
    
    return {
        "user_id": user_id,
        "search_term": search_term,
        "results": results,
        "count": len(results)
    }


@app.delete("/api/user/{user_id}/chat/clear")
async def clear_chat_history(
    user_id: str,
    session_id: Optional[str] = None,
    days: Optional[int] = None
):
    """Clear conversation history for a user."""
    count = chat_memory_manager.clear_user_history(
        user_id=user_id,
        session_id=session_id,
        days=days
    )
    
    return {
        "user_id": user_id,
        "deleted_count": count,
        "message": f"Cleared {count} messages"
    }


# --- Helpers ---

async def call_ollama(
    user_message: str,
    user_context: Dict[str, Any],
    financial_data: Dict[str, Any],
    user_id: Optional[str] = None,
    use_memory: bool = True
) -> Dict[str, Any]:
    """Call Ollama REST API directly for dynamic, personalized responses."""
    user_id = user_id or user_context.get("number", "guest")
    name    = user_context.get("name", "User")
    occ     = user_context.get("occupation", "Professional")
    age     = user_context.get("age", 30)
    city    = user_context.get("location", "")

    # Use the centralized extractor with monthly normalization
    fm = extract_financials_summary(financial_data)
    monthly_income  = fm["monthly_income"]
    monthly_expense = fm["monthly_expense"]
    monthly_savings = fm["monthly_savings"]
    savings_rate    = fm["savings_rate"]
    net_worth       = fm["net_worth"]
    credit_score    = fm["credit_score"]
    num_months      = fm["num_months"]

    dti              = round(monthly_expense / monthly_income * 100, 1) if monthly_income > 0 else 0
    emergency_months = round(net_worth * 0.2 / monthly_expense, 1) if monthly_expense > 0 else 0
    health_score     = min(100, max(0, int(50 + savings_rate)))
    risk_level       = "Low" if savings_rate > 30 else "Medium" if savings_rate > 10 else "High"

    # Get EPF balance
    epf_balance = 0
    epf = financial_data.get("fetch_epf_details", {}).get("epfDetails", {})
    if epf:
        epf_balance = epf.get("totalBalance", 0)

    # Get MF value
    mf_value = 0
    for scheme in financial_data.get("fetch_mf_transactions", {}).get("mfTransactions", []):
        for txn in scheme.get("txns", []):
            if len(txn) >= 5 and txn[0] == 1:
                mf_value += txn[4]

    # Get agent status
    agent_status = multi_agent_coordinator.get_agent_status()
    agent_info = "\n".join([
        f"- {name.title()}: {info['role']} ({info['status']}) - {len(info['capabilities'])} capabilities"
        for name, info in agent_status.items()
    ])
    
    # Get user preferences from memory if enabled
    preferences_info = ""
    if use_memory:
        preferences = chat_memory_manager.get_user_preferences(user_id)
        if preferences.get("topics_of_interest"):
            preferences_info = f"\n\n=== USER PREFERENCES (from conversation history) ===\n"
            preferences_info += f"Topics of Interest: {', '.join(preferences['topics_of_interest'][:5])}\n"
            if preferences.get("financial_goals"):
                preferences_info += f"Financial Goals: {', '.join(preferences['financial_goals'][:3])}\n"

    system_prompt = f"""You are AUREXIS AI, a personal financial advisor for {name}.

USER PROFILE:
Name: {name}, Age: {age}, Occupation: {occ}, Location: {city}
Monthly Income: ₹{monthly_income:,.0f}
Monthly Expenses: ₹{monthly_expense:,.0f}
Monthly Savings: ₹{monthly_savings:,.0f}
Savings Rate: {savings_rate}%
Net Worth: ₹{net_worth:,.0f}
Credit Score: {credit_score}
EPF Balance: ₹{epf_balance:,.0f}
MF Invested: ₹{mf_value:,.0f}
Emergency Fund: {emergency_months} months covered
{preferences_info}
INSTRUCTIONS:
- Write responses in simple, plain text without markdown formatting
- No bold text, no bullet points, no emojis, no special formatting
- Keep answers short and conversational (2-4 sentences)
- Use actual numbers from the profile above
- Write naturally like you're talking to a friend
- Use ₹ for currency values
- Never say you don't have data — use the profile above"""

    # Get conversation context from memory if enabled
    if use_memory:
        recent_context = chat_memory_manager.get_recent_context(user_id, num_messages=10)
    else:
        # Fallback to in-memory conversation history
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        conversation_history[user_id].append({"role": "user", "content": user_message})
        recent_context = conversation_history[user_id][-10:]

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [{"role": "system", "content": system_prompt}, *recent_context, {"role": "user", "content": user_message}],
                "stream": False,
            },
        )
        resp.raise_for_status()
        reply = resp.json().get("message", {}).get("content", "")

    # Update in-memory history if not using persistent memory
    if not use_memory:
        conversation_history[user_id].append({"role": "assistant", "content": reply})

    return {
        "summary": "AUREXIS AI",
        "content": reply,
        "insights": [],  # Removed metrics footer for cleaner output
        "recommendations": [],
        "confidence": 0.85,
    }


def build_user_profile(user: Dict[str, Any]) -> Dict[str, Any]:
    """Build the full user profile object for the frontend."""
    user_id      = user.get("number", "")
    financial_data = user.get("financial_data", {})

    fm = extract_financials_summary(financial_data)
    income       = fm["monthly_income"]
    expense      = fm["monthly_expense"]
    savings_rate = fm["savings_rate"]
    net_worth    = fm["net_worth"]
    credit_score = fm["credit_score"]

    expenses = [
        {"category": "Housing",   "amount": int(expense * 0.40), "percentage": 40, "trend": "stable", "color": "#3B82F6"},
        {"category": "Food",      "amount": int(expense * 0.20), "percentage": 20, "trend": "up",     "color": "#F59E0B"},
        {"category": "Transport", "amount": int(expense * 0.15), "percentage": 15, "trend": "down",   "color": "#10B981"},
        {"category": "Utilities", "amount": int(expense * 0.10), "percentage": 10, "trend": "stable", "color": "#EC4899"},
        {"category": "Other",     "amount": int(expense * 0.15), "percentage": 15, "trend": "stable", "color": "#6B7280"},
    ]
    investments = [
        {"name": "Equity Funds",   "type": "MF",  "value": int(net_worth * 0.4), "allocation": 40, "returns": 12.5, "risk": "High"},
        {"name": "Fixed Deposits", "type": "FD",  "value": int(net_worth * 0.3), "allocation": 30, "returns": 7.0,  "risk": "Low"},
        {"name": "EPF",            "type": "EPF", "value": int(net_worth * 0.2), "allocation": 20, "returns": 8.1,  "risk": "Safe"},
        {"name": "Gold",           "type": "Gold","value": int(net_worth * 0.1), "allocation": 10, "returns": 9.0,  "risk": "Medium"},
    ]
    monthly_data = [
        {"month": m, "income": int(income * fi), "expense": int(expense * fe),
         "savings": int(income * fi - expense * fe), "netWorth": int(net_worth * fn), "debt": d}
        for m, fi, fe, fn, d in [
            ("Oct", 0.90, 0.95, 0.92, 250000), ("Nov", 1.00, 1.00, 0.95, 245000),
            ("Dec", 1.10, 1.20, 0.97, 240000), ("Jan", 1.00, 0.90, 0.98, 235000),
            ("Feb", 0.95, 0.85, 0.99, 230000), ("Mar", 1.00, 1.00, 1.00, 225000),
        ]
    ]

    return {
        "id": user_id,
        "name": user.get("name", "Unknown"),
        "avatar": f"https://ui-avatars.com/api/?name={user.get('name','User')}&background=3B82F6&color=fff&size=128&bold=true",
        "occupation": user.get("occupation", "Professional"),
        "age": user.get("age", 30),
        "email": user.get("email", ""),
        "bankName": user.get("bank_name", ""),
        "accountNumber": user.get("account_number", ""),
        "accountType": user.get("account_type", "Savings"),
        "bankLocation": user.get("bank_location", ""),
        "hasCreditCard": user.get("credit_card", "No").lower() == "yes",
        "location": user.get("location", ""),
        "monthlyIncome": income,
        "monthlyExpense": expense,
        "savings": int(income - expense),
        "netWorth": net_worth,
        "savingsRate": savings_rate,
        "creditScore": credit_score,
        "riskLevel": "Low" if savings_rate > 30 else "Medium",
        "personalityTag": "Balanced Planner",
        "lastActive": "Now",
        "financialHealthScore": min(100, max(0, int(50 + savings_rate))),
        "debtToIncomeRatio": round(expense / income, 2) if income > 0 else 0,
        "emergencyFundMonths": round(net_worth * 0.2 / expense, 1) if expense > 0 else 6,
        "investmentValue": int(net_worth * 0.6),
        "totalDebt": 225000,
        "goals": [
            {"id": "g1", "name": "Emergency Fund", "target": int(expense * 6),   "current": int(expense * 4.5), "deadline": "2026-08", "icon": "🛡️", "monthlySavingsNeeded": 5000},
            {"id": "g2", "name": "New Car",         "target": 1200000,            "current": 350000,             "deadline": "2027-12", "icon": "🚗", "monthlySavingsNeeded": 15000},
        ],
        "expenses": expenses,
        "investments": investments,
        "monthlyData": monthly_data,
        "upcomingEMIs": [
            {"name": "Home Loan", "amount": 25000, "dueDate": "2026-05-05", "type": "Mortgage"},
            {"name": "Car Loan",  "amount": 12000, "dueDate": "2026-05-12", "type": "Auto"},
        ],
        "alerts": [
            {"id": "a1", "type": "info",    "title": "Savings Milestone", "message": "You've saved 20% more than last month!", "timestamp": "2026-04-15"},
            {"id": "a2", "type": "warning", "title": "Large Expense",     "message": "Unexpected transaction of ₹15,000 detected.", "timestamp": "2026-04-10"},
        ],
    }


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
