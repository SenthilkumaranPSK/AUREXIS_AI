"""Chat Response Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent

class ChatResponseAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Chat Response Agent",
            role="Generates conversational responses to user queries",
            capabilities=["generate_response", "format_answer", "provide_context"]
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        self._update_status("processing")
        data = task.get("data", {})
        query = data.get("query", "")
        context = task.get("context", {})
        
        # Generate response based on context
        response = f"Based on your financial data: {query}"
        
        self._update_status("completed")
        return {"response": response, "context": context, "agent": self.name}
