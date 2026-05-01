"""
Chat Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import Dict, Optional
from datetime import datetime
from schemas.chat import ChatRequest, ChatResponse
from auth.dependencies import get_current_user
from chat_memory import chat_memory_manager
from user_manager_secure import UserManager
import httpx
import os

chat_router = APIRouter(prefix="/api/chat", tags=["Chat"])

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "deepseek-v3.1:671b-cloud")


@chat_router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Send a message to the AI assistant"""
    try:
        user_id = current_user.get("sub")
        
        # Get user data
        user = UserManager.get_user_by_id(user_id) or {"name": "User"}
        financial_data = UserManager.get_all_user_data(user_id)
        
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
    """Call Ollama for chat response"""
    from analytics import extract_financials_summary
    from multi_agent_system import multi_agent_coordinator
    
    name = user_context.get("name", "User")
    occ = user_context.get("occupation", "Professional")
    age = user_context.get("age", 30)
    city = user_context.get("location", "")
    
    # Extract financial summary
    fm = extract_financials_summary(financial_data)
    monthly_income = fm["monthly_income"]
    monthly_expense = fm["monthly_expense"]
    monthly_savings = fm["monthly_savings"]
    savings_rate = fm["savings_rate"]
    net_worth = fm["net_worth"]
    credit_score = fm["credit_score"]
    
    health_score = min(100, max(0, int(50 + savings_rate)))
    risk_level = "Low" if savings_rate > 30 else "Medium" if savings_rate > 10 else "High"
    
    # Get agent status
    agent_status = multi_agent_coordinator.get_agent_status()
    agent_info = "\n".join([
        f"- {name.title()}: {info['role']} ({info['status']})"
        for name, info in agent_status.items()
    ])
    
    # Get preferences if memory enabled
    preferences_info = ""
    if use_memory:
        preferences = chat_memory_manager.get_user_preferences(user_id)
        if preferences.get("topics_of_interest"):
            preferences_info = f"\n\nUser Interests: {', '.join(preferences['topics_of_interest'][:5])}"
    
    system_prompt = f"""You are AUREXIS AI, an expert personal financial advisor for {name}.

=== USER PROFILE ===
Name: {name} | Age: {age} | Occupation: {occ} | Location: {city}
Credit Score: {credit_score} | Risk Profile: {risk_level}

=== MONTHLY FINANCIALS ===
Income: ₹{monthly_income:,.0f} | Expenses: ₹{monthly_expense:,.0f} | Savings: ₹{monthly_savings:,.0f}
Savings Rate: {savings_rate}% | Net Worth: ₹{net_worth:,.0f} | Health Score: {health_score}/100

=== AI AGENTS ===
{agent_info}
{preferences_info}

Give specific, personalized advice using exact numbers. Be direct and actionable (3-5 sentences)."""
    
    # Get conversation context
    if use_memory:
        recent_context = chat_memory_manager.get_recent_context(user_id, num_messages=10)
    else:
        recent_context = []
    
    # Call Ollama
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
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
            resp.raise_for_status()
            reply = resp.json().get("message", {}).get("content", "")
    except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPStatusError):
        # Fallback for testing/unreachable Ollama
        reply = f"Hello {name}! I am currently operating in offline mode. Your monthly savings rate is {savings_rate}%, which is {risk_level.lower()} risk. How can I help you with your net worth of ₹{net_worth:,.0f} today?"
    
    return {
        "summary": "AUREXIS AI",
        "content": reply,
        "insights": [
            f"Savings rate: {savings_rate}%",
            f"Net worth: ₹{net_worth:,.0f}",
            f"Health score: {health_score}/100"
        ],
        "confidence": 0.85
    }
