"""Alert Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent

class AlertAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Alert Agent",
            role="Detects anomalies and generates alerts",
            capabilities=["detect_anomalies", "generate_alerts", "monitor_thresholds"]
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        self._update_status("processing")
        from alerts import generate_alerts
        data = task.get("data", {})
        result = generate_alerts(data)
        self._update_status("completed")
        return {"alerts": result, "agent": self.name}
