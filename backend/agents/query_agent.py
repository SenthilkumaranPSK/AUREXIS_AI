"""
Query Understanding Agent
Analyzes user queries and determines intent
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class QueryUnderstandingAgent(BaseAgent):
    """Agent for understanding user queries and determining intent"""
    
    def __init__(self):
        super().__init__(
            name="Query Understanding Agent",
            role="Analyzes user queries to determine intent and extract key information",
            capabilities=[
                "intent_classification",
                "entity_extraction",
                "query_parsing",
                "context_understanding"
            ]
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute query understanding task"""
        self._update_status("processing")
        
        task_type = task.get("type")
        data = task.get("data", {})
        query = data.get("query", "")
        
        if task_type == "classify_intent":
            result = self._classify_intent(query)
        elif task_type == "extract_entities":
            result = self._extract_entities(query)
        else:
            result = self._parse_query(query)
        
        self._update_status("completed")
        return result
    
    def _classify_intent(self, query: str) -> Dict[str, Any]:
        """Classify user intent from query"""
        query_lower = query.lower()
        
        # Intent classification logic
        if any(word in query_lower for word in ["spend", "expense", "cost", "paid"]):
            intent = "expense_inquiry"
        elif any(word in query_lower for word in ["save", "saving", "savings"]):
            intent = "savings_inquiry"
        elif any(word in query_lower for word in ["goal", "target", "achieve"]):
            intent = "goal_inquiry"
        elif any(word in query_lower for word in ["invest", "investment", "portfolio"]):
            intent = "investment_inquiry"
        elif any(word in query_lower for word in ["risk", "danger", "safe"]):
            intent = "risk_inquiry"
        elif any(word in query_lower for word in ["forecast", "predict", "future"]):
            intent = "forecast_inquiry"
        elif any(word in query_lower for word in ["health", "score", "status"]):
            intent = "health_inquiry"
        else:
            intent = "general_inquiry"
        
        return {
            "intent": intent,
            "confidence": 0.85,
            "query": query
        }
    
    def _extract_entities(self, query: str) -> Dict[str, Any]:
        """Extract entities from query"""
        entities = {
            "amounts": [],
            "dates": [],
            "categories": [],
            "time_periods": []
        }
        
        # Simple entity extraction (in production, use NLP library)
        words = query.split()
        for word in words:
            if word.startswith("₹") or word.isdigit():
                entities["amounts"].append(word)
            elif any(month in word.lower() for month in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]):
                entities["dates"].append(word)
        
        return {
            "entities": entities,
            "query": query
        }
    
    def _parse_query(self, query: str) -> Dict[str, Any]:
        """Parse query and extract all information"""
        intent_result = self._classify_intent(query)
        entity_result = self._extract_entities(query)
        
        return {
            "intent": intent_result["intent"],
            "confidence": intent_result["confidence"],
            "entities": entity_result["entities"],
            "query": query,
            "parsed": True
        }


# Backward-compatible alias for older imports/tests
QueryAgent = QueryUnderstandingAgent
