"""Goal Planning Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent

class GoalPlanningAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Goal Planning Agent",
            role="Creates and tracks financial goal plans",
            capabilities=["create_goal_plan", "track_goals", "calculate_timeline"]
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        self._update_status("processing")
        from analytics import compute_goals
        data = task.get("data", {})
        result = compute_goals(data)
        self._update_status("completed")
        return {"goal_plan": result, "agent": self.name}
