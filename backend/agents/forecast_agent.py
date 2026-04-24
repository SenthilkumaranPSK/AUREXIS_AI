"""Forecasting Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent

class ForecastingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Forecasting Agent",
            role="Generates financial forecasts and predictions",
            capabilities=["forecast_monthly", "forecast_goals", "forecast_networth"]
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        self._update_status("processing")
        from forecasting import compute_monthly_forecast
        data = task.get("data", {})
        result = compute_monthly_forecast(data, 6)
        self._update_status("completed")
        return {"forecast": result, "agent": self.name}
