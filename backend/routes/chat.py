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
        # Fallback for testing/unreachable Ollama
        logger.error(f"❌ Ollama error: {type(e).__name__}: {str(e)}")
        reply = f"Hello {name}, I am currently processing in standby mode. Based on your {savings_rate}% savings rate and ₹{net_worth:,.0f} net worth, I recommend focusing on liquidity. How can I assist with your portfolio today?"
    
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
