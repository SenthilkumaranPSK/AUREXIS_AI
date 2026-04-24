"""Savings Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent

class SavingsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Savings Agent",
            role="Analyzes savings patterns and provides savings strategies",
            capabilities=["analyze_savings", "calculate_savings_rate", "suggest_savings_plan"]
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        self._update_status("processing")
        from analytics import extract_financials_summary
        data = task.get("data", {})
        fm = extract_financials_summary(data)
        result = {
            "monthly_savings": fm["monthly_savings"],
            "savings_rate": fm["savings_rate"],
            "analysis": "Good" if fm["savings_rate"] > 20 else "Needs Improvement"
        }
        self._update_status("completed")
        return {"savings_analysis": result, "agent": self.name}
