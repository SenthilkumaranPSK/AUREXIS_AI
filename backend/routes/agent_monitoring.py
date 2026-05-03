"""
Agent Monitoring Routes
API endpoints for monitoring agent performance
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, Dict
from datetime import datetime

from auth.dependencies import get_current_user
from agents.agent_monitor import agent_monitor

router = APIRouter(tags=["Agent Monitoring"])


@router.get("/metrics")
async def get_all_agent_metrics(
    current_user: Dict = Depends(get_current_user)
):
    """
    Get metrics for all agents
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Metrics for all agents
    """
    try:
        metrics = agent_monitor.get_all_metrics()
        
        return {
            "success": True,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/{agent_name}")
async def get_agent_metrics(
    agent_name: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get metrics for a specific agent
    
    Args:
        agent_name: Agent name
        current_user: Authenticated user
        
    Returns:
        Agent metrics
    """
    try:
        metrics = agent_monitor.get_agent_metrics(agent_name)
        
        if not metrics:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
        
        return {
            "success": True,
            "agent_name": agent_name,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_execution_history(
    agent_name: Optional[str] = None,
    limit: int = 50,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get agent execution history
    
    Args:
        agent_name: Optional agent name to filter by
        limit: Maximum number of executions to return
        current_user: Authenticated user
        
    Returns:
        Execution history
    """
    try:
        history = agent_monitor.get_execution_history(
            agent_name=agent_name,
            limit=limit
        )
        
        return {
            "success": True,
            "history": history,
            "count": len(history),
            "agent_name": agent_name,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary")
async def get_performance_summary(
    current_user: Dict = Depends(get_current_user)
):
    """
    Get overall performance summary
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Performance summary
    """
    try:
        summary = agent_monitor.get_performance_summary()
        
        return {
            "success": True,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/leaderboard")
async def get_agent_leaderboard(
    current_user: Dict = Depends(get_current_user)
):
    """
    Get agent leaderboard by performance
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Agent leaderboard
    """
    try:
        leaderboard = agent_monitor.get_agent_leaderboard()
        
        return {
            "success": True,
            "leaderboard": leaderboard,
            "count": len(leaderboard),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/slow")
async def get_slow_agents(
    threshold: Optional[float] = None,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get agents with slow execution times
    
    Args:
        threshold: Optional custom threshold in seconds
        current_user: Authenticated user
        
    Returns:
        List of slow agents
    """
    try:
        slow_agents = agent_monitor.get_slow_agents(threshold=threshold)
        
        return {
            "success": True,
            "slow_agents": slow_agents,
            "count": len(slow_agents),
            "threshold": threshold or 30.0,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/errors")
async def get_error_prone_agents(
    threshold: Optional[float] = None,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get agents with high error rates
    
    Args:
        threshold: Optional custom error rate threshold (0-1)
        current_user: Authenticated user
        
    Returns:
        List of error-prone agents
    """
    try:
        error_prone = agent_monitor.get_error_prone_agents(threshold=threshold)
        
        return {
            "success": True,
            "error_prone_agents": error_prone,
            "count": len(error_prone),
            "threshold": threshold or 0.1,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history")
async def clear_history(
    older_than_days: Optional[int] = None,
    current_user: Dict = Depends(get_current_user)
):
    """
    Clear agent execution history
    
    Args:
        older_than_days: Clear only executions older than X days
        current_user: Authenticated user
        
    Returns:
        Success status
    """
    try:
        agent_monitor.clear_history(older_than_days=older_than_days)
        
        return {
            "success": True,
            "message": f"History cleared {'for executions older than ' + str(older_than_days) + ' days' if older_than_days else 'completely'}",
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def get_agent_health(
    current_user: Dict = Depends(get_current_user)
):
    """
    Get health status of all agents
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Agent health status
    """
    try:
        summary = agent_monitor.get_performance_summary()
        
        health_status = {
            "overall_health": "healthy" if summary["critical_agents"] == 0 else "degraded" if summary["degraded_agents"] > 0 else "critical",
            "healthy_agents": summary["healthy_agents"],
            "degraded_agents": summary["degraded_agents"],
            "critical_agents": summary["critical_agents"],
            "agent_health": summary["agent_health"],
            "total_agents": summary["total_agents"]
        }
        
        return {
            "success": True,
            "health": health_status,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
