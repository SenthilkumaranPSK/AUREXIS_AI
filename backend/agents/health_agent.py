"""Financial Health Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent

class FinancialHealthAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Financial Health Agent",
            role="Calculates and monitors financial health score",
            capabilities=["calculate_health", "track_health_trends", "identify_health_issues"]
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        self._update_status("processing")
        from health import compute_health
        data = task.get("data", {})
        result = compute_health(data)
        self._update_status("completed")
        return {"health_score": result, "agent": self.name}
