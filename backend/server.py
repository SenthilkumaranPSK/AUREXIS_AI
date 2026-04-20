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

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from user_manager import (
    authenticate_user,
    get_all_users,
    get_user_by_name,
    get_user_by_id,
    get_all_user_data,
    load_user_data,
)
from analytics import (
    compute_metrics,
    compute_forecast,
    compute_expenses,
    compute_investments,
    compute_goals,
    compute_risk,
    compute_simulation,
    extract_financials_summary,
)
from recommendations import generate_recommendations
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


# --- Global state ---

active_sessions: Dict[str, Dict[str, Any]] = {}
conversation_history: Dict[str, List[Dict[str, str]]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 AUREXIS AI Backend starting — model: {OLLAMA_MODEL}")
    yield
    print("👋 Server shutting down...")


# --- App ---

app = FastAPI(title="AUREXIS AI Backend", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Endpoints ---

@app.get("/")
async def root():
    return {"status": "online", "service": "AUREXIS AI Backend", "model": OLLAMA_MODEL}


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

    try:
        response = await call_ollama(request.message, user, financial_data)
        return {"success": True, "response": response, "user_id": user_id}
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


# --- Helpers ---

async def call_ollama(
    user_message: str,
    user_context: Dict[str, Any],
    financial_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Call Ollama REST API directly for dynamic, personalized responses."""
    user_id = user_context.get("number", "guest")
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

    system_prompt = f"""You are AUREXIS AI, an expert personal financial advisor for {name}.

=== USER FINANCIAL PROFILE ===
Name: {name} | Age: {age} | Occupation: {occ} | Location: {city}
Credit Score: {credit_score} | Risk Profile: {risk_level}

=== MONTHLY FINANCIALS (avg over {num_months} months) ===
Monthly Income:   ₹{monthly_income:,.0f}
Monthly Expenses: ₹{monthly_expense:,.0f}
Monthly Savings:  ₹{monthly_savings:,.0f}
Savings Rate:     {savings_rate}%
Expense Ratio:    {dti}%

=== WEALTH SNAPSHOT ===
Net Worth:        ₹{net_worth:,.0f}
EPF Balance:      ₹{epf_balance:,.0f}
MF Invested:      ₹{mf_value:,.0f}
Emergency Fund:   {emergency_months} months covered
Health Score:     {health_score}/100

=== YOUR ROLE ===
- Give specific, personalized advice using the EXACT numbers above
- Be direct and actionable (3-5 sentences)
- Always reference actual rupee amounts from the profile
- Highlight risks if any exist
- Use ₹ for all currency values
- Never say you don't have data — use the profile above"""

    # Maintain per-user conversation history
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append({"role": "user", "content": user_message})

    # Keep last 10 turns for context window
    recent = conversation_history[user_id][-10:]

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [{"role": "system", "content": system_prompt}, *recent],
                "stream": False,
            },
        )
        resp.raise_for_status()
        reply = resp.json().get("message", {}).get("content", "")

    conversation_history[user_id].append({"role": "assistant", "content": reply})

    return {
        "summary": "AUREXIS AI",
        "content": reply,
        "insights": [
            f"Savings rate: {savings_rate}%",
            f"Net worth: ₹{net_worth:,.0f}",
            f"Credit score: {credit_score}",
            f"Health score: {health_score}/100",
        ],
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
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
