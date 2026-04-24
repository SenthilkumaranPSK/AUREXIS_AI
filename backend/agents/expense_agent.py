"""Expense Analysis Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent

class ExpenseAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Expense Analysis Agent",
            role="Analyzes spending patterns and expense trends",
            capabilities=["analyze_expenses", "analyze_patterns", "detect_overspending"]
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        self._update_status("processing")
        from analytics import compute_expenses
        data = task.get("data", {})
        result = compute_expenses(data)
        self._update_status("completed")
        return {"expense_analysis": result, "agent": self.name}
