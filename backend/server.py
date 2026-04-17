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
)

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
    user_id = request.user_id
    user = get_user_by_id(user_id) or get_user_by_name(user_id) or {"number": user_id, "name": "User"}
    financial_data = get_all_user_data(user.get("number", user_id))

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


# --- Helpers ---

def _extract_financials(financial_data: Dict[str, Any]):
    """Extract key financial metrics from raw data."""
    net_worth_data = financial_data.get("fetch_net_worth", {})
    total_net_worth = 0.0
    if "netWorthResponse" in net_worth_data:
        try:
            total_net_worth = float(
                net_worth_data["netWorthResponse"].get("totalNetWorthValue", {}).get("units", 0) or 0
            )
        except (ValueError, TypeError):
            pass

    monthly_income = 0.0
    monthly_expense = 0.0
    for bank in financial_data.get("fetch_bank_transactions", {}).get("bankTransactions", []):
        for txn in bank.get("txns", []):
            if len(txn) >= 4:
                try:
                    amount = float(txn[0]) if str(txn[0]).replace(".", "").replace("-", "").isdigit() else 0.0
                except:
                    amount = 0.0
                if txn[3] == 1:
                    monthly_income += amount
                elif txn[3] == 2:
                    monthly_expense += amount

    credit_score = 750
    for report in financial_data.get("fetch_credit_report", {}).get("creditReports", []):
        score = report.get("creditReportData", {}).get("score", {}).get("bureauScore")
        if score:
            try:
                credit_score = int(float(score))
            except:
                pass
            break

    savings_rate = round((monthly_income - monthly_expense) / monthly_income * 100, 1) if monthly_income > 0 else 0.0
    return total_net_worth, monthly_income, monthly_expense, savings_rate, credit_score


async def call_ollama(
    user_message: str,
    user_context: Dict[str, Any],
    financial_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Call Ollama REST API directly for dynamic, personalized responses."""
    user_id = user_context.get("number", "guest")
    name = user_context.get("name", "User")
    net_worth, income, expense, savings_rate, credit_score = _extract_financials(financial_data)

    system_prompt = f"""You are AUREXIS AI, a personal financial advisor for {name}.

User's financial profile:
- Net Worth: ₹{net_worth:,.0f}
- Monthly Income: ₹{income:,.0f}
- Monthly Expenses: ₹{expense:,.0f}
- Savings Rate: {savings_rate}%
- Credit Score: {credit_score}
- Bank: {user_context.get("bank_name", "N/A")} ({user_context.get("account_type", "Savings")})
- Location: {user_context.get("location", "N/A")}
- Credit Card: {user_context.get("credit_card", "No")}

Guidelines:
- Give personalized advice using the user's actual numbers above
- Be concise and actionable (2-4 sentences unless asked for more)
- Use ₹ for all currency values
- Focus on practical steps the user can take"""

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
        ],
        "recommendations": [],
        "confidence": 0.85,
    }


def build_user_profile(user: Dict[str, Any]) -> Dict[str, Any]:
    """Build the full user profile object for the frontend."""
    user_id = user.get("number", "")
    financial_data = user.get("financial_data", {})
    net_worth, income, expense, savings_rate, credit_score = _extract_financials(financial_data)

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
