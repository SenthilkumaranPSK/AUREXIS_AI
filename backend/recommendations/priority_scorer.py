"""
Priority Scorer
Calculate priority scores for recommendations
"""

from typing import Dict, Any


class PriorityScorer:
    """Calculate priority scores for recommendations"""
    
    def __init__(self):
        self.impact_weights = {
            "critical": 100,
            "high": 75,
            "medium": 50,
            "low": 25
        }
        
        self.difficulty_weights = {
            "low": 1.0,
            "medium": 0.8,
            "high": 0.6
        }
        
        self.timeframe_weights = {
            "immediate": 1.0,
            "1-3 months": 0.9,
            "3-6 months": 0.7,
            "6-12 months": 0.5,
            "long-term": 0.3
        }
    
    def calculate_score(
        self,
        recommendation: Dict[str, Any],
        financial_data: Dict[str, Any]
    ) -> float:
        """
        Calculate priority score for a recommendation
        
        Args:
            recommendation: Recommendation dictionary
            financial_data: User's financial data
            
        Returns:
            Priority score (0-100)
        """
        # Base score from impact
        impact = recommendation.get("impact", "medium")
        base_score = self.impact_weights.get(impact, 50)
        
        # Adjust for difficulty (easier = higher priority)
        difficulty = recommendation.get("difficulty", "medium")
        difficulty_multiplier = self.difficulty_weights.get(difficulty, 0.8)
        
        # Adjust for timeframe (sooner = higher priority)
        timeframe = recommendation.get("timeframe", "1-3 months")
        timeframe_multiplier = self.timeframe_weights.get(timeframe, 0.7)
        
        # Calculate urgency based on financial situation
        urgency_multiplier = self._calculate_urgency(recommendation, financial_data)
        
        # Calculate final score
        score = base_score * difficulty_multiplier * timeframe_multiplier * urgency_multiplier
        
        # Normalize to 0-100
        return min(100, max(0, score))
    
    def _calculate_urgency(
        self,
        recommendation: Dict[str, Any],
        financial_data: Dict[str, Any]
    ) -> float:
        """Calculate urgency multiplier based on financial situation"""
        category = recommendation.get("category", "")
        
        monthly_income = financial_data.get("monthly_income", 0)
        monthly_expense = financial_data.get("monthly_expense", 0)
        monthly_savings = monthly_income - monthly_expense
        savings_rate = (monthly_savings / monthly_income * 100) if monthly_income > 0 else 0
        
        # High urgency for critical financial situations
        if category == "debt" and monthly_expense > monthly_income * 0.9:
            return 1.5
        
        if category == "savings" and savings_rate < 5:
            return 1.4
        
        if category == "expenses" and monthly_expense > monthly_income:
            return 1.5
        
        # Medium urgency for improvement areas
        if category == "investment" and savings_rate > 20:
            return 1.2
        
        if category == "goals" and monthly_savings > 0:
            return 1.1
        
        # Normal urgency
        return 1.0


# Global instance
priority_scorer = PriorityScorer()
