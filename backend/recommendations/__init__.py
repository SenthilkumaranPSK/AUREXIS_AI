"""
Advanced Recommendation System
Explainable, prioritized financial recommendations
"""

from .advanced_engine import AdvancedRecommendationEngine
from .priority_scorer import PriorityScorer
from .explanation_generator import ExplanationGenerator

def generate_recommendations(financial_data: dict, user_profile: dict = None) -> list:
    """Helper function for backward compatibility"""
    engine = AdvancedRecommendationEngine()
    return engine.generate_recommendations(financial_data, user_profile or {})

__all__ = [
    "AdvancedRecommendationEngine",
    "PriorityScorer",
    "ExplanationGenerator",
    "generate_recommendations",
]
