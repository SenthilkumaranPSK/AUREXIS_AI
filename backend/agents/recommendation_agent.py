"""Recommendation Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent

class RecommendationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Recommendation Agent",
            role="Generates personalized financial recommendations",
            capabilities=["generate_recommendations", "goal_recommendations", "health_recommendations", "risk_mitigation", "investment_recommendations"]
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        self._update_status("processing")
        from recommendations import generate_recommendations
        data = task.get("data", {})
        result = generate_recommendations(data)
        self._update_status("completed")
        return {"recommendations": result, "agent": self.name}
