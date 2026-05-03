"""
Advanced Recommendation System
Explainable, prioritized financial recommendations
"""

from .advanced_engine import AdvancedRecommendationEngine
from .priority_scorer import PriorityScorer
from .explanation_generator import ExplanationGenerator
# from recommendations_legacy import generate_recommendations  # Disabled for JSON mode

__all__ = [
    "AdvancedRecommendationEngine",
    "PriorityScorer",
    "ExplanationGenerator",
]
