"""
Advanced Analytics Routes
API endpoints for pattern detection, insights, and behavior analysis
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from auth.dependencies import get_current_user
from database_legacy import User
from models.financial import FinancialModel
from analytics.pattern_detector import pattern_detector
from analytics.insight_generator import insight_generator
from analytics.behavior_analyzer import behavior_analyzer

router = APIRouter(prefix="/api/analytics", tags=["Advanced Analytics"])


@router.get("/patterns")
async def detect_patterns(
    days: int = 90,
    current_user: User = Depends(get_current_user)
):
    """
    Detect financial patterns
    
    Args:
        days: Number of days to analyze
        current_user: Authenticated user
        
    Returns:
        Detected patterns
    """
    try:
        # Get financial data
        financial_data = await FinancialModel.get_user_financial_summary(current_user.id)
        
        # Get transactions
        transactions = await FinancialModel.get_user_transactions(
            current_user.id,
            days=days
        )
        
        # Detect patterns
        patterns = pattern_detector.detect_patterns(
            financial_data=financial_data,
            transactions=transactions
        )
        
        return {
            "success": True,
            "patterns": patterns,
            "analysis_period_days": days,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights")
async def generate_insights(
    include_patterns: bool = True,
    current_user: User = Depends(get_current_user)
):
    """
    Generate financial insights
    
    Args:
        include_patterns: Include pattern-based insights
        current_user: Authenticated user
        
    Returns:
        Generated insights
    """
    try:
        # Get current financial data
        financial_data = await FinancialModel.get_user_financial_summary(current_user.id)
        
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=6
        )
        
        # Get patterns if requested
        patterns = None
        if include_patterns:
            transactions = await FinancialModel.get_user_transactions(
                current_user.id,
                days=90
            )
            patterns = pattern_detector.detect_patterns(
                financial_data=financial_data,
                transactions=transactions
            )
        
        # Generate insights
        insights = insight_generator.generate_insights(
            financial_data=financial_data,
            patterns=patterns,
            historical_data=historical_data
        )
        
        return {
            "success": True,
            "insights": insights,
            "total_insights": len(insights),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/behavior")
async def analyze_behavior(
    current_user: User = Depends(get_current_user)
):
    """
    Analyze financial behavior
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Behavior analysis
    """
    try:
        # Get financial data
        financial_data = await FinancialModel.get_user_financial_summary(current_user.id)
        
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=6
        )
        
        # Get transactions
        transactions = await FinancialModel.get_user_transactions(
            current_user.id,
            days=180
        )
        
        # Analyze behavior
        analysis = behavior_analyzer.analyze_behavior(
            financial_data=financial_data,
            historical_data=historical_data,
            transactions=transactions
        )
        
        return {
            "success": True,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends/{metric}")
async def analyze_trend(
    metric: str,
    months: int = 6,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze trend for a specific metric
    
    Args:
        metric: Metric to analyze (net_worth, total_income, total_expenses, etc.)
        months: Number of months to analyze
        current_user: Authenticated user
        
    Returns:
        Trend analysis
    """
    try:
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=months
        )
        
        if not historical_data:
            raise HTTPException(status_code=404, detail="Insufficient historical data")
        
        # Analyze trend
        trend_analysis = insight_generator.generate_trend_analysis(
            historical_data=historical_data,
            metric=metric
        )
        
        return {
            "success": True,
            "metric": metric,
            "trend_analysis": trend_analysis,
            "analysis_period_months": months,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_dashboard_metrics(
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive dashboard metrics
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Dashboard metrics
    """
    try:
        # Get current financial data
        financial_data = await FinancialModel.get_user_financial_summary(current_user.id)
        
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=12
        )
        
        # Get transactions
        transactions = await FinancialModel.get_user_transactions(
            current_user.id,
            days=90
        )
        
        # Detect patterns
        patterns = pattern_detector.detect_patterns(
            financial_data=financial_data,
            transactions=transactions
        )
        
        # Generate insights
        insights = insight_generator.generate_insights(
            financial_data=financial_data,
            patterns=patterns,
            historical_data=historical_data
        )
        
        # Analyze behavior
        behavior = behavior_analyzer.analyze_behavior(
            financial_data=financial_data,
            historical_data=historical_data,
            transactions=transactions
        )
        
        # Calculate key metrics
        income = financial_data.get("total_income", 0)
        expenses = financial_data.get("total_expenses", 0)
        savings = income - expenses
        savings_rate = (savings / income * 100) if income > 0 else 0
        
        # Get trends
        net_worth_trend = insight_generator.generate_trend_analysis(
            historical_data=historical_data,
            metric="net_worth"
        ) if historical_data else None
        
        return {
            "success": True,
            "dashboard": {
                "summary": {
                    "net_worth": financial_data.get("net_worth", 0),
                    "monthly_income": income,
                    "monthly_expenses": expenses,
                    "monthly_savings": savings,
                    "savings_rate": round(savings_rate, 1)
                },
                "top_insights": insights[:5],
                "behavior_score": behavior.get("overall_score", 0),
                "behavior_profile": behavior.get("behavior_profile", ""),
                "patterns_detected": len(patterns.get("spending_patterns", [])),
                "net_worth_trend": net_worth_trend,
                "strengths": behavior.get("strengths", [])[:3],
                "recommendations": behavior.get("recommendations", [])[:3]
            },
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/spending-analysis")
async def analyze_spending(
    category: Optional[str] = None,
    days: int = 30,
    current_user: User = Depends(get_current_user)
):
    """
    Detailed spending analysis
    
    Args:
        category: Specific category to analyze (optional)
        days: Number of days to analyze
        current_user: Authenticated user
        
    Returns:
        Spending analysis
    """
    try:
        # Get transactions
        transactions = await FinancialModel.get_user_transactions(
            current_user.id,
            days=days
        )
        
        # Filter by category if specified
        if category:
            transactions = [t for t in transactions if t.get("category") == category]
        
        # Calculate statistics
        total_spending = sum(t.get("amount", 0) for t in transactions if t.get("type") == "expense")
        avg_transaction = total_spending / len(transactions) if transactions else 0
        
        # Group by category
        by_category = {}
        for t in transactions:
            if t.get("type") == "expense":
                cat = t.get("category", "other")
                by_category[cat] = by_category.get(cat, 0) + t.get("amount", 0)
        
        # Group by day
        by_day = {}
        for t in transactions:
            if t.get("type") == "expense":
                date = t.get("date", "")[:10]  # YYYY-MM-DD
                by_day[date] = by_day.get(date, 0) + t.get("amount", 0)
        
        return {
            "success": True,
            "analysis": {
                "total_spending": round(total_spending, 2),
                "transaction_count": len(transactions),
                "average_transaction": round(avg_transaction, 2),
                "by_category": {k: round(v, 2) for k, v in by_category.items()},
                "by_day": {k: round(v, 2) for k, v in sorted(by_day.items())},
                "analysis_period_days": days,
                "category_filter": category
            },
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comparative-analysis")
async def comparative_analysis(
    period1_months: int = 1,
    period2_months: int = 1,
    current_user: User = Depends(get_current_user)
):
    """
    Compare two time periods
    
    Args:
        period1_months: Months ago for period 1 (0 = current month)
        period2_months: Months ago for period 2
        current_user: Authenticated user
        
    Returns:
        Comparative analysis
    """
    try:
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=max(period1_months, period2_months) + 1
        )
        
        if len(historical_data) < 2:
            raise HTTPException(status_code=404, detail="Insufficient data for comparison")
        
        # Get data for both periods
        period1_data = historical_data[period1_months] if period1_months < len(historical_data) else {}
        period2_data = historical_data[period2_months] if period2_months < len(historical_data) else {}
        
        # Calculate changes
        comparisons = {}
        metrics = ["total_income", "total_expenses", "net_worth"]
        
        for metric in metrics:
            val1 = period1_data.get(metric, 0)
            val2 = period2_data.get(metric, 0)
            change = val1 - val2
            change_pct = (change / val2 * 100) if val2 != 0 else 0
            
            comparisons[metric] = {
                "period1_value": round(val1, 2),
                "period2_value": round(val2, 2),
                "absolute_change": round(change, 2),
                "percentage_change": round(change_pct, 2),
                "trend": "up" if change > 0 else "down" if change < 0 else "stable"
            }
        
        return {
            "success": True,
            "comparison": comparisons,
            "period1_months_ago": period1_months,
            "period2_months_ago": period2_months,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
