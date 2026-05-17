"""
Chat Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import Dict, Optional
from datetime import datetime
from schemas.chat import ChatRequest, ChatResponse
from auth.dependencies import get_current_user
from chat_memory import chat_memory_manager
from user_manager_json import UserManagerJSON
from config import settings
import httpx
import logging

chat_router = APIRouter(tags=["Chat"])
logger = logging.getLogger(__name__)

# Use settings from config.py which loads from .env
OLLAMA_BASE_URL = settings.OLLAMA_BASE_URL
OLLAMA_MODEL = settings.OLLAMA_MODEL

# Debug logging
logger.info(f"🔧 Chat route loaded with OLLAMA_BASE_URL={OLLAMA_BASE_URL}, OLLAMA_MODEL={OLLAMA_MODEL}")


@chat_router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Send a message to the AI assistant"""
    try:
        user_id = current_user.get("sub")
        
        # Get user data
        user = UserManagerJSON.get_user_by_id(user_id) or {"name": "User"}
        financial_data = UserManagerJSON.get_all_user_data(user_id)
        
        # Generate session ID if not provided
        session_id = request.session_id or f"session_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
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
        
        # Get response from Ollama
        response = await call_ollama_chat(
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
        
        return ChatResponse(
            success=True,
            response=response,
            session_id=session_id,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )


@chat_router.get("/history")
async def get_chat_history(
    limit: int = Query(50, ge=1, le=200),
    session_id: Optional[str] = None,
    days: Optional[int] = None,
    current_user: Dict = Depends(get_current_user)
):
    """Get conversation history"""
    try:
        user_id = current_user.get("sub")
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch history: {str(e)}"
        )


@chat_router.get("/sessions")
async def get_chat_sessions(
    limit: int = Query(20, ge=1, le=100),
    current_user: Dict = Depends(get_current_user)
):
    """Get list of conversation sessions"""
    try:
        user_id = current_user.get("sub")
        sessions = chat_memory_manager.get_conversation_sessions(
            user_id=user_id,
            limit=limit
        )
        
        return {
            "user_id": user_id,
            "sessions": sessions,
            "count": len(sessions)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch sessions: {str(e)}"
        )


@chat_router.get("/stats")
async def get_chat_stats(current_user: Dict = Depends(get_current_user)):
    """Get conversation statistics"""
    try:
        user_id = current_user.get("sub")
        stats = chat_memory_manager.get_conversation_stats(user_id)
        
        return {
            "user_id": user_id,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch stats: {str(e)}"
        )


@chat_router.get("/preferences")
async def get_chat_preferences(current_user: Dict = Depends(get_current_user)):
    """Get user preferences from conversation history"""
    try:
        user_id = current_user.get("sub")
        preferences = chat_memory_manager.get_user_preferences(user_id)
        
        return {
            "user_id": user_id,
            "preferences": preferences
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch preferences: {str(e)}"
        )


@chat_router.post("/search")
async def search_chat_history(
    search_term: str = Body(..., embed=True),
    limit: int = Query(20, ge=1, le=100),
    current_user: Dict = Depends(get_current_user)
):
    """Search conversation history"""
    try:
        user_id = current_user.get("sub")
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@chat_router.delete("/clear")
async def clear_chat_history(
    session_id: Optional[str] = None,
    days: Optional[int] = None,
    current_user: Dict = Depends(get_current_user)
):
    """Clear conversation history"""
    try:
        user_id = current_user.get("sub")
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear history: {str(e)}"
        )


# Helper function
async def call_ollama_chat(
    user_message: str,
    user_context: Dict,
    financial_data: Dict,
    user_id: str,
    use_memory: bool = True
) -> Dict:
    """Call Ollama for chat response with deep financial context"""
    from analytics.legacy_adapter import extract_financials_summary, compute_investments, compute_risk
    from multi_agent_system import multi_agent_coordinator
    
    name = user_context.get("name", "User")
    occ = user_context.get("occupation", "Professional")
    age = user_context.get("age", 30)
    city = user_context.get("location", "")
    
    # Extract deep financial metrics
    fm = extract_financials_summary(financial_data)
    inv = compute_investments(financial_data)
    risk = compute_risk(financial_data)
    
    monthly_income = fm["monthly_income"]
    monthly_expense = fm["monthly_expense"]
    monthly_savings = fm["monthly_savings"]
    savings_rate = fm["savings_rate"]
    net_worth = fm["net_worth"]
    credit_score = fm["credit_score"]
    
    health_score = min(100, max(0, int(50 + savings_rate)))
    risk_level = risk.get("riskLevel", "Medium")
    
    # Build portfolio summary
    portfolio_summary = "\n".join([
        f"- {p['name']}: ₹{p['value']:,.0f} ({p['allocation']}% allocation, {p['returns']}% returns)"
        for p in inv.get("portfolio", [])[:3]
    ])
    
    # Get agent status
    agent_status = multi_agent_coordinator.get_agent_status()
    agent_info = "\n".join([
        f"- {name.title()}: {info['role']} ({info['status']})"
        for name, info in agent_status.items()
    ])
    
    # Get preferences
    preferences_info = ""
    if use_memory:
        preferences = chat_memory_manager.get_user_preferences(user_id)
        if preferences.get("topics_of_interest"):
            preferences_info = f"\n\nUser Interests: {', '.join(preferences['topics_of_interest'][:5])}"
    
    system_prompt = f"""You are AUREXIS AI, a sophisticated institutional-grade financial advisor for {name}.
Your tone is professional, insightful, and proactive. You don't just answer questions; you analyze data.

=== USER BIOMETRICS ===
Name: {name} | Age: {age} | Role: {occ} | Location: {city}
Credit: {credit_score} | Risk Profile: {risk_level} | Health Score: {health_score}/100

=== CORE FINANCIALS (Monthly) ===
Income: ₹{monthly_income:,.0f} | Expenses: ₹{monthly_expense:,.0f} | Savings: ₹{monthly_savings:,.0f} ({savings_rate}%)
Net Worth: ₹{net_worth:,.0f} | Debt-to-Income: {risk.get('debtToIncomeRatio', 0)}

=== PORTFOLIO SNAPSHOT ===
{portfolio_summary}
Average Portfolio Returns: {inv.get('avgReturns', 0)}%

=== ACTIVE AI AGENTS ===
{agent_info}
{preferences_info}

GUIDELINES:
1. Always use the user's specific numbers in your advice.
2. If you see a high debt-to-income ratio or low savings rate (<10%), mention it as a priority.
3. Be concise (max 4 sentences) but extremely high-value.
4. If asked about investments, refer to their current Equity/FD/Gold allocation.
5. Address the user as {name} occasionally to maintain rapport."""
    
    # Get conversation context
    if use_memory:
        recent_context = chat_memory_manager.get_recent_context(user_id, num_messages=10)
    else:
        recent_context = []
    
    # Call Ollama
    try:
        logger.info(f"🔄 Calling Ollama at {OLLAMA_BASE_URL} with model {OLLAMA_MODEL}")
        async with httpx.AsyncClient(timeout=180.0) as client:
            resp = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": OLLAMA_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *recent_context,
                        {"role": "user", "content": user_message}
                    ],
                    "stream": False,
                },
            )
            logger.info(f"✅ Ollama response status: {resp.status_code}")
            resp.raise_for_status()
            reply = resp.json().get("message", {}).get("content", "")
            logger.info(f"✅ Got reply from Ollama: {reply[:100]}...")
    except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPStatusError) as e:
        logger.error(f"❌ Ollama error: {type(e).__name__}: {str(e)}")
        reply = _offline_response(
            user_message=user_message,
            name=name,
            monthly_income=monthly_income,
            monthly_expense=monthly_expense,
            monthly_savings=monthly_savings,
            savings_rate=savings_rate,
            net_worth=net_worth,
            credit_score=credit_score,
            health_score=health_score,
            risk_level=risk_level,
            inv=inv,
            risk=risk,
        )
    
    return {
        "summary": "AUREXIS AI Executive Insight",
        "content": reply,
        "insights": [
            f"Savings rate: {savings_rate}%",
            f"Net worth: ₹{net_worth:,.0f}",
            f"Health score: {health_score}/100"
        ],
        "confidence": 0.95
    }


# ─────────────────────────────────────────────────────────────────────────────
# INTELLIGENT OFFLINE RESPONSE ENGINE
# Analyses the user's message using keyword matching and returns a personalised,
# data-driven response using the user's actual financial figures.
# ─────────────────────────────────────────────────────────────────────────────

def _offline_response(
    user_message: str,
    name: str,
    monthly_income: float,
    monthly_expense: float,
    monthly_savings: float,
    savings_rate: float,
    net_worth: float,
    credit_score: int,
    health_score: int,
    risk_level: str,
    inv: dict,
    risk: dict,
) -> str:
    """
    Rule-based financial advisor that responds intelligently to user queries
    using their real financial data when Ollama is unavailable.
    """
    msg = user_message.lower().strip()

    # ── helpers ──────────────────────────────────────────────────────────────
    def fmt(n: float) -> str:
        """Format number as Indian currency string."""
        if n >= 1_00_00_000:
            return f"₹{n/1_00_00_000:.1f} Cr"
        if n >= 1_00_000:
            return f"₹{n/1_00_000:.1f} L"
        return f"₹{n:,.0f}"

    portfolio   = inv.get("portfolio", [])
    dti         = risk.get("debtToIncomeRatio", 0)
    total_debt  = risk.get("totalDebt", 0)
    emf_months  = risk.get("emergencyFundMonths", 0)
    invest_val  = sum(p.get("value", 0) for p in portfolio)
    top_holding = max(portfolio, key=lambda p: p.get("value", 0), default={})

    # ── keyword buckets ───────────────────────────────────────────────────────
    keywords = {
        "savings": ["sav", "save", "saving", "piggy", "deposit", "fd", "fixed deposit", "recurring"],
        "spending": ["spend", "spending", "expense", "expens", "cut", "reduc", "budget", "overspend", "cost"],
        "investment": ["invest", "stock", "equity", "mutual fund", "sip", "portfolio", "share", "nifty", "sensex", "etf", "gold", "bond"],
        "loan": ["loan", "emi", "debt", "borrow", "credit", "mortgage", "home loan", "car loan", "personal loan"],
        "health": ["health", "score", "financial health", "wellness", "status", "how am i", "how are my"],
        "networth": ["net worth", "networth", "wealth", "total asset", "asset", "worth"],
        "income": ["income", "salary", "earn", "pay", "wage", "revenue", "hike", "raise"],
        "goal": ["goal", "target", "plan", "retire", "retirement", "house", "car", "vacation", "dream", "future"],
        "risk": ["risk", "safe", "danger", "volatile", "volatility", "exposure", "hedge"],
        "credit": ["credit score", "cibil", "credit rating", "credit card", "creditworthiness"],
        "tax": ["tax", "itr", "income tax", "80c", "deduction", "tds", "gst", "tax saving"],
        "forecast": ["forecast", "predict", "future", "next month", "projection", "trend", "outlook"],
        "emergency": ["emergency", "emergency fund", "rainy day", "contingency", "backup"],
        "greeting": ["hi", "hello", "hey", "good morning", "good evening", "good afternoon", "namaste", "hola"],
    }

    def matches(bucket: str) -> bool:
        return any(kw in msg for kw in keywords[bucket])

    # ── response logic ────────────────────────────────────────────────────────

    if matches("greeting"):
        status_emoji = "🟢" if health_score >= 70 else "🟡" if health_score >= 50 else "🔴"
        return (
            f"Hello {name}! I'm AUREXIS AI running in offline mode — all your data is still fully accessible.\n\n"
            f"{status_emoji} Your financial snapshot:\n"
            f"• Net Worth: {fmt(net_worth)}\n"
            f"• Monthly Savings: {fmt(monthly_savings)} ({savings_rate:.1f}% rate)\n"
            f"• Health Score: {health_score}/100 ({risk_level} risk)\n\n"
            f"What would you like to explore today?"
        )

    if matches("savings"):
        ideal_savings = monthly_income * 0.20
        gap = ideal_savings - monthly_savings
        if savings_rate >= 30:
            tip = f"Excellent discipline! You're saving {fmt(monthly_savings)}/month. Consider moving surplus into ELSS or index funds for tax-efficient growth."
        elif savings_rate >= 20:
            tip = f"Good progress. You're {fmt(gap):.0f} away from the 30% benchmark. Automate a SIP of {fmt(gap)} to close this gap."
        else:
            tip = (
                f"Your savings rate of {savings_rate:.1f}% is below the recommended 20%. "
                f"You need to save an additional {fmt(ideal_savings - monthly_savings)} per month to reach the benchmark. "
                f"Start by reviewing your top 3 expense categories."
            )
        return (
            f"📊 Savings Analysis for {name}:\n\n"
            f"• Current savings: {fmt(monthly_savings)}/month ({savings_rate:.1f}%)\n"
            f"• Income: {fmt(monthly_income)} | Expenses: {fmt(monthly_expense)}\n"
            f"• Recommended minimum: {fmt(ideal_savings)}/month (20%)\n\n"
            f"💡 {tip}"
        )

    if matches("spending"):
        high_spend = monthly_expense / monthly_income > 0.7
        return (
            f"💸 Expense Breakdown for {name}:\n\n"
            f"• Monthly expenses: {fmt(monthly_expense)} ({(monthly_expense/monthly_income*100):.1f}% of income)\n"
            f"• Monthly income: {fmt(monthly_income)}\n"
            f"• Remaining after expenses: {fmt(monthly_savings)}\n\n"
            f"{'⚠️ Your expense ratio is high (>70%). ' if high_spend else '✅ Your expense ratio is healthy. '}"
            f"{'Focus on reducing discretionary spending — dining, subscriptions, and impulse purchases are common culprits. Aim to bring expenses below 70% of income.' if high_spend else 'Keep tracking category-wise to maintain this discipline. Consider the 50/30/20 rule: 50% needs, 30% wants, 20% savings.'}"
        )

    if matches("investment"):
        if portfolio:
            holdings_text = "\n".join([
                f"  • {p['name']}: {fmt(p['value'])} ({p.get('allocation', 0)}% | {p.get('returns', 0)}% returns)"
                for p in portfolio[:4]
            ])
            best = max(portfolio, key=lambda p: p.get("returns", 0), default={})
            return (
                f"📈 Investment Portfolio for {name}:\n\n"
                f"• Total portfolio value: {fmt(invest_val)}\n"
                f"• Holdings:\n{holdings_text}\n\n"
                f"💡 Best performer: {best.get('name', 'N/A')} at {best.get('returns', 0)}% returns. "
                f"{'Your equity allocation looks balanced. Consider rebalancing if any single asset exceeds 40%.' if invest_val > 0 else 'Start a SIP of at least ₹5,000/month in a diversified index fund to build long-term wealth.'}"
            )
        return (
            f"📈 Investment Advice for {name}:\n\n"
            f"With a monthly surplus of {fmt(monthly_savings)}, here's a suggested allocation:\n"
            f"• 40% Equity (Index funds / ELSS): {fmt(monthly_savings * 0.4)}/month\n"
            f"• 30% Debt (FD / Debt MF): {fmt(monthly_savings * 0.3)}/month\n"
            f"• 20% Gold / REITs: {fmt(monthly_savings * 0.2)}/month\n"
            f"• 10% Emergency top-up: {fmt(monthly_savings * 0.1)}/month\n\n"
            f"💡 Start with a Nifty 50 index fund SIP — low cost, diversified, and historically ~12% CAGR."
        )

    if matches("loan"):
        dti_pct = dti * 100
        status = "manageable" if dti < 0.36 else "elevated — consider prepayment"
        return (
            f"🏦 Debt Analysis for {name}:\n\n"
            f"• Total outstanding debt: {fmt(total_debt)}\n"
            f"• Debt-to-Income ratio: {dti_pct:.1f}% ({status})\n"
            f"• Monthly income: {fmt(monthly_income)}\n\n"
            f"💡 {'Your DTI is healthy (<36%). You can consider a new loan if needed, but keep total EMIs under 40% of income.' if dti < 0.36 else 'Your DTI exceeds 36%. Prioritise prepaying high-interest debt (credit cards first, then personal loans). Avoid new loans until DTI drops below 30%.'}"
        )

    if matches("health"):
        grade = "Excellent" if health_score >= 80 else "Good" if health_score >= 65 else "Fair" if health_score >= 50 else "Needs Attention"
        return (
            f"❤️ Financial Health Report for {name}:\n\n"
            f"• Health Score: {health_score}/100 — {grade}\n"
            f"• Risk Level: {risk_level}\n"
            f"• Savings Rate: {savings_rate:.1f}%\n"
            f"• Credit Score: {credit_score}\n"
            f"• Emergency Fund: {emf_months:.1f} months\n\n"
            f"💡 {'All indicators are strong. Focus on growing investments and optimising tax.' if health_score >= 70 else 'Key areas to improve: ' + (', '.join(filter(None, ['savings rate' if savings_rate < 20 else '', 'emergency fund' if emf_months < 6 else '', 'credit score' if credit_score < 700 else ''])) or 'review expense categories') + '.'}"
        )

    if matches("networth"):
        invest_pct = (invest_val / net_worth * 100) if net_worth > 0 else 0
        return (
            f"💰 Net Worth Breakdown for {name}:\n\n"
            f"• Total Net Worth: {fmt(net_worth)}\n"
            f"• Investment Assets: {fmt(invest_val)} ({invest_pct:.1f}%)\n"
            f"• Outstanding Debt: {fmt(total_debt)}\n"
            f"• Monthly Savings Contribution: {fmt(monthly_savings)}\n\n"
            f"💡 At your current savings rate, you'll add approximately {fmt(monthly_savings * 12)} to your net worth this year. "
            f"{'Great wealth-building momentum!' if savings_rate >= 20 else 'Increasing your savings rate by just 5% would add an extra ' + fmt(monthly_income * 0.05 * 12) + ' annually.'}"
        )

    if matches("income"):
        tax_estimate = monthly_income * 12 * 0.2
        return (
            f"💼 Income Analysis for {name}:\n\n"
            f"• Monthly Income: {fmt(monthly_income)}\n"
            f"• Annual Income: {fmt(monthly_income * 12)}\n"
            f"• Estimated Annual Tax: {fmt(tax_estimate)} (~20% effective rate)\n"
            f"• Take-home after expenses: {fmt(monthly_savings)}/month\n\n"
            f"💡 To maximise take-home, invest {fmt(150000)} in 80C instruments (ELSS, PPF, LIC) to save up to {fmt(46800)} in taxes annually."
        )

    if matches("goal"):
        years_to_1cr = (1_00_00_000 - net_worth) / (monthly_savings * 12) if monthly_savings > 0 else 99
        return (
            f"🎯 Goal Planning for {name}:\n\n"
            f"• Current Net Worth: {fmt(net_worth)}\n"
            f"• Monthly Savings: {fmt(monthly_savings)}\n"
            f"• At current pace, you'll reach ₹1 Crore in ~{max(0, years_to_1cr):.1f} years\n\n"
            f"💡 To accelerate: increase SIP by {fmt(monthly_income * 0.05)}/month (5% of income). "
            f"With 12% CAGR on investments, compounding will significantly shorten your timeline. "
            f"Define specific goals (retirement corpus, home down payment) for more precise planning."
        )

    if matches("risk"):
        return (
            f"⚠️ Risk Profile for {name}:\n\n"
            f"• Overall Risk Level: {risk_level}\n"
            f"• Debt-to-Income: {dti*100:.1f}%\n"
            f"• Emergency Fund: {emf_months:.1f} months {'✅' if emf_months >= 6 else '⚠️ (target: 6 months)'}\n"
            f"• Credit Score: {credit_score} {'✅' if credit_score >= 750 else '⚠️ (target: 750+)'}\n\n"
            f"💡 {'Your risk exposure is well-managed. Maintain your emergency fund and keep DTI below 36%.' if risk_level == 'Low' else 'To reduce risk: build emergency fund to 6 months of expenses (' + fmt(monthly_expense * 6) + '), and reduce high-interest debt first.'}"
        )

    if matches("credit"):
        grade = "Excellent" if credit_score >= 800 else "Good" if credit_score >= 750 else "Fair" if credit_score >= 700 else "Poor"
        return (
            f"💳 Credit Score Analysis for {name}:\n\n"
            f"• CIBIL Score: {credit_score} — {grade}\n\n"
            f"💡 {'Your credit score is excellent. You qualify for the best loan rates.' if credit_score >= 750 else 'To improve your score: pay all EMIs on time, keep credit utilisation below 30%, avoid multiple loan applications simultaneously, and check your CIBIL report for errors.'}"
        )

    if matches("tax"):
        annual_income = monthly_income * 12
        tax_80c_saving = min(150000, monthly_savings * 12) * 0.3
        return (
            f"📋 Tax Planning for {name}:\n\n"
            f"• Annual Income: {fmt(annual_income)}\n"
            f"• Max 80C Deduction: {fmt(150000)}\n"
            f"• Potential Tax Saving via 80C: {fmt(tax_80c_saving)}\n\n"
            f"💡 Key tax-saving instruments:\n"
            f"  • ELSS Mutual Funds (80C) — {fmt(150000)} limit, 3yr lock-in\n"
            f"  • PPF (80C) — Safe, 7.1% returns, 15yr tenure\n"
            f"  • NPS (80CCD) — Additional {fmt(50000)} deduction\n"
            f"  • Health Insurance (80D) — Up to {fmt(25000)} deduction"
        )

    if matches("forecast"):
        proj_3m = net_worth + (monthly_savings * 3)
        proj_1y = net_worth + (monthly_savings * 12 * 1.08)
        return (
            f"🔮 Financial Forecast for {name}:\n\n"
            f"• Current Net Worth: {fmt(net_worth)}\n"
            f"• Projected (3 months): {fmt(proj_3m)}\n"
            f"• Projected (1 year, 8% growth): {fmt(proj_1y)}\n"
            f"• Monthly savings contribution: {fmt(monthly_savings)}\n\n"
            f"💡 These projections assume consistent savings. Investing your surplus at 12% CAGR (equity) vs 7% (FD) would yield {fmt(monthly_savings * 12 * 0.05)} extra annually."
        )

    if matches("emergency"):
        target = monthly_expense * 6
        current = emf_months * monthly_expense
        gap = max(0, target - current)
        return (
            f"🛡️ Emergency Fund Status for {name}:\n\n"
            f"• Current emergency fund: {fmt(current)} ({emf_months:.1f} months)\n"
            f"• Recommended target: {fmt(target)} (6 months of expenses)\n"
            f"• Gap to fill: {fmt(gap)}\n\n"
            f"💡 {'Your emergency fund is fully funded. Keep it in a liquid instrument like a savings account or liquid mutual fund.' if emf_months >= 6 else f'You need {fmt(gap)} more to reach 6 months. Set aside {fmt(gap/6)}/month for the next 6 months to complete your safety net.'}"
        )

    # ── default: general financial summary ───────────────────────────────────
    return (
        f"Hi {name}! I'm AUREXIS AI in offline mode — here's your financial snapshot:\n\n"
        f"• 💰 Net Worth: {fmt(net_worth)}\n"
        f"• 📈 Monthly Income: {fmt(monthly_income)}\n"
        f"• 💸 Monthly Expenses: {fmt(monthly_expense)}\n"
        f"• 🏦 Monthly Savings: {fmt(monthly_savings)} ({savings_rate:.1f}%)\n"
        f"• ❤️ Health Score: {health_score}/100 ({risk_level} risk)\n"
        f"• 💳 Credit Score: {credit_score}\n\n"
        f"You can ask me about: savings, spending, investments, loans, goals, tax planning, risk, forecasting, or your credit score."
    )
