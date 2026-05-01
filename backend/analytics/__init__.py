"""
Advanced Analytics Module
Pattern detection, insights, and behavior analysis
"""

from .pattern_detector import PatternDetector
from .insight_generator import InsightGenerator
from .behavior_analyzer import BehaviorAnalyzer
from .legacy_adapter import (
    extract_transactions,
    extract_net_worth,
    extract_credit_score,
    extract_financials_summary,
    compute_metrics,
    compute_expenses,
    compute_investments,
    compute_goals,
    compute_risk,
    compute_forecast,
    compute_simulation
)

__all__ = [
    "PatternDetector",
    "InsightGenerator",
    "BehaviorAnalyzer",
    "extract_transactions",
    "extract_net_worth",
    "extract_credit_score",
    "extract_financials_summary",
    "compute_metrics",
    "compute_expenses",
    "compute_investments",
    "compute_goals",
    "compute_risk",
    "compute_forecast",
    "compute_simulation"
]
