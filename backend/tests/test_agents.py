"""AI agent smoke tests for current async agent interfaces."""

import asyncio
from agents.orchestrator import AgentOrchestrator
from agents.query_agent import QueryUnderstandingAgent


def test_query_agent_async_execution():
    agent = QueryUnderstandingAgent()
    result = asyncio.run(agent.execute({"type": "classify_intent", "data": {"query": "How much did I spend?"}}))
    assert "intent" in result
    assert "confidence" in result


def test_orchestrator_goal_planning_workflow():
    orchestrator = AgentOrchestrator()
    data = {
        "transactions": [],
        "user_profile": {"name": "Test User"},
        "monthly_income": 50000,
        "monthly_expense": 30000,
        "net_worth": 500000,
    }
    result = asyncio.run(orchestrator.execute_workflow("goal_planning", data))
    assert result["workflow"] == "goal_planning"
    assert "results" in result
