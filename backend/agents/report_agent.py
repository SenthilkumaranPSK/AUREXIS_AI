"""Report Generation Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent

class ReportGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Report Generation Agent",
            role="Generates comprehensive financial reports",
            capabilities=["generate_report", "create_summary", "export_data"]
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        self._update_status("processing")
        from report import generate_report
        data = task.get("data", {})
        user = data.get("user_profile", {"name": "User"})
        result = generate_report(user, data)
        self._update_status("completed")
        return {"report": result, "agent": self.name}
