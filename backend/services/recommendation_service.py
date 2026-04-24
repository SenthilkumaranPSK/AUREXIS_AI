"""
Recommendation Service
Business logic for generating recommendations
"""

from typing import List, Dict, Optional
from user_manager import get_all_user_data, get_user_by_id
from recommendations_legacy import generate_recommendations
from explainable_recommendations import explainable_recommendation_engine
from models.financial import FinancialModel


class RecommendationService:
    """Recommendation generation business logic"""
    
    @staticmethod
    def generate_recommendations(user_id: str) -> List[Dict]:
        """Generate basic recommendations from data patterns"""
        data = get_all_user_data(user_id)
        recommendations = generate_recommendations(data)
        
        # Store recommendations in database
        for rec in recommendations:
            try:
                FinancialModel.create_recommendation(
                    user_id=user_id,
                    category=rec.get("category", "general"),
                    title=rec.get("title", "Recommendation"),
                    description=rec.get("description", ""),
                    priority=rec.get("priority", "medium"),
                    impact=rec.get("impact")
                )
            except Exception as e:
                print(f"Error storing recommendation: {e}")
        
        return recommendations
    
    @staticmethod
    def generate_explainable_recommendations(user_id: str) -> List[Dict]:
        """Generate recommendations with full explanations"""
        financial_data = get_all_user_data(user_id)
        user_profile = get_user_by_id(user_id) or {}
        
        recommendations = explainable_recommendation_engine.generate_recommendations(
            financial_data=financial_data,
            user_profile=user_profile
        )
        
        # Convert to dict format
        rec_dicts = [rec.to_dict() for rec in recommendations]
        
        # Store in database
        for rec_dict in rec_dicts:
            try:
                FinancialModel.create_recommendation(
                    user_id=user_id,
                    category=rec_dict.get("category", "general"),
                    title=rec_dict.get("title", "Recommendation"),
                    description=rec_dict.get("explanation", ""),
                    priority=rec_dict.get("priority", "medium"),
                    impact=rec_dict.get("expected_benefit")
                )
            except Exception as e:
                print(f"Error storing explainable recommendation: {e}")
        
        return rec_dicts
    
    @staticmethod
    def get_stored_recommendations(user_id: str, status: Optional[str] = None) -> List[Dict]:
        """Get recommendations from database"""
        return FinancialModel.get_user_recommendations(user_id, status)
    
    @staticmethod
    def update_recommendation_status(rec_id: int, status: str) -> bool:
        """Update recommendation status (pending/accepted/rejected)"""
        if status not in ["pending", "accepted", "rejected"]:
            raise ValueError("Invalid status. Must be: pending, accepted, or rejected")
        
        return FinancialModel.update_recommendation_status(rec_id, status)
