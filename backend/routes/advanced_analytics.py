"""
Advanced Analytics Routes
API endpoints for pattern detection, insights, and behavior analysis
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from auth.dependencies import get_current_user
from user_manager_json import UserManagerJSON
from analytics.pattern_detector import pattern_detector
from analytics.insight_generator import insight_generator
from analytics.behavior_analyzer import behavior_analyzer
from analytics.legacy_adapter import extract_financials_summary, compute_forecast

router = APIRouter(prefix="/analytics", tags=["Advanced Analytics"])


@router.get("/patterns")
async def detect_patterns(
    days: int = 90,
    current_user: Dict = Depends(get_current_user)
):
    """
    Detect financial patterns
    """
    try:
        user_id = current_user.get("sub")
        financial_data = UserManagerJSON.get_all_user_data(user_id)
        
        if "error" in financial_data:
            raise HTTPException(status_code=404, detail=financial_data["error"])
            
        # Detect patterns
        patterns = pattern_detector.detect_patterns(financial_data=financial_data)
        
        return {
            "success": True,
            "patterns": patterns,
            "analysis_period_days": days,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights")
async def generate_insights(
    include_patterns: bool = True,
    current_user: Dict = Depends(get_current_user)
):
    """
    Generate financial insights
    """
    try:
        user_id = current_user.get("sub")
        financial_data = UserManagerJSON.get_all_user_data(user_id)
        
        if "error" in financial_data:
            raise HTTPException(status_code=404, detail=financial_data["error"])
            
        # Get historical data (mocked from compute_forecast)
        historical_data = compute_forecast(financial_data)
        
        # Get patterns if requested
        patterns = None
        if include_patterns:
            patterns = pattern_detector.detect_patterns(financial_data=financial_data)
        
        # Generate insights
        summary = extract_financials_summary(financial_data)
        # Normalize summary for insight generator
        norm_data = {
            "total_income": summary["monthly_income"],
            "total_expenses": summary["monthly_expense"],
            "net_worth": summary["net_worth"],
            "emergency_fund": summary["net_worth"] * 0.2, # Mock
            "goals": [] # Mock
        }
        
        insights = insight_generator.generate_insights(
            financial_data=norm_data,
            patterns=patterns,
            historical_data=historical_data
        )
        
        return {
            "success": True,
            "insights": insights,
            "total_insights": len(insights),
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/behavior")
async def analyze_behavior(
    current_user: Dict = Depends(get_current_user)
):
    """
    Analyze financial behavior
    """
    try:
        user_id = current_user.get("sub")
        financial_data = UserManagerJSON.get_all_user_data(user_id)
        
        if "error" in financial_data:
            raise HTTPException(status_code=404, detail=financial_data["error"])
            
        # Get historical data
        historical_data = compute_forecast(financial_data)
        
        # Normalize summary
        summary = extract_financials_summary(financial_data)
        norm_data = {
            "total_income": summary["monthly_income"],
            "total_expenses": summary["monthly_expense"],
            "net_worth": summary["net_worth"],
            "emergency_fund": summary["net_worth"] * 0.2,
            "investments": {"equity": summary["net_worth"] * 0.4, "fixed": summary["net_worth"] * 0.2}
        }
        
        # Analyze behavior
        analysis = behavior_analyzer.analyze_behavior(
            financial_data=norm_data,
            historical_data=historical_data
        )
        
        return {
            "success": True,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_dashboard_metrics(
    current_user: Dict = Depends(get_current_user)
):
    """
    Get comprehensive dashboard metrics
    """
    try:
        user_id = current_user.get("sub")
        financial_data = UserManagerJSON.get_all_user_data(user_id)
        
        if "error" in financial_data:
            raise HTTPException(status_code=404, detail=financial_data["error"])
            
        # Get historical data
        historical_data = compute_forecast(financial_data)
        
        # Detect patterns
        patterns = pattern_detector.detect_patterns(financial_data=financial_data)
        
        # Normalize summary
        summary = extract_financials_summary(financial_data)
        norm_data = {
            "total_income": summary["monthly_income"],
            "total_expenses": summary["monthly_expense"],
            "net_worth": summary["net_worth"],
            "emergency_fund": summary["net_worth"] * 0.2,
            "investments": {"equity": summary["net_worth"] * 0.4, "fixed": summary["net_worth"] * 0.2},
            "goals": []
        }
        
        # Generate insights
        insights = insight_generator.generate_insights(
            financial_data=norm_data,
            patterns=patterns,
            historical_data=historical_data
        )
        
        # Analyze behavior
        behavior = behavior_analyzer.analyze_behavior(
            financial_data=norm_data,
            historical_data=historical_data
        )

        # Map insights to match frontend expectation (insight instead of message)
        mapped_insights = []
        for ins in insights:
            mapped_insights.append({
                "category": ins.get("category", "General"),
                "title": ins.get("title", "Insight"),
                "insight": ins.get("message", ""),
                "impact": ins.get("impact", "low"),
                "type": "positive" if ins.get("impact") == "positive" else "info" if ins.get("impact") == "medium" else "negative"
            })

        # Map strengths and recommendations to strings
        strengths_list = [s.get("message", s) if isinstance(s, dict) else s for s in behavior.get("strengths", [])]
        recommendations_list = behavior.get("recommendations", [])
        
        # Get trends
        net_worth_trend = insight_generator.generate_trend_analysis(
            historical_data=historical_data,
            metric="netWorth"
        )
        
        return {
            "success": True,
            "dashboard": {
                "summary": {
                    "net_worth": summary["net_worth"],
                    "monthly_income": summary["monthly_income"],
                    "monthly_expenses": summary["monthly_expense"],
                    "monthly_savings": summary["monthly_savings"],
                    "savings_rate": summary["savings_rate"]
                },
                "top_insights": mapped_insights[:5],
                "behavior_score": behavior.get("overall_score", 0),
                "behavior_profile": behavior.get("behavior_profile", ""),
                "patterns_detected": len(patterns.get("spending_patterns", [])),
                "net_worth_trend": net_worth_trend,
                "strengths": strengths_list[:3],
                "recommendations": recommendations_list[:3]
            },
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/spending-analysis")
async def analyze_spending(
    category: Optional[str] = None,
    days: int = 30,
    current_user: Dict = Depends(get_current_user)
):
    """
    Detailed spending analysis
    """
    try:
        user_id = current_user.get("sub")
        financial_data = UserManagerJSON.get_all_user_data(user_id)
        
        # Simple extraction for now
        summary = extract_financials_summary(financial_data)
        
        return {
            "success": True,
            "analysis": {
                "total_spending": summary["monthly_expense"],
                "transaction_count": 25, # Mock
                "average_transaction": round(summary["monthly_expense"] / 25, 2) if 25 > 0 else 0,
                "by_category": {"Food": 5000, "Rent": 15000, "Travel": 3000}, # Mock
                "by_day": {}, # Mock
                "analysis_period_days": days,
                "category_filter": category
            },
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
