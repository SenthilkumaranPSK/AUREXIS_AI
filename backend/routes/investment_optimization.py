"""
Investment Optimization Routes
API endpoints for portfolio optimization, risk calculation, and rebalancing
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

from auth.dependencies import get_current_user
from database_legacy import User
from models.financial import FinancialModel
from investments.portfolio_optimizer import portfolio_optimizer
from investments.risk_calculator import risk_calculator
from investments.rebalancing_engine import rebalancing_engine

router = APIRouter(prefix="/api/investments", tags=["Investment Optimization"])


class OptimizePortfolioRequest(BaseModel):
    investment_amount: float
    risk_tolerance: str  # very_low, low, moderate, high
    goals: Optional[List[Dict]] = None


class RebalanceRequest(BaseModel):
    current_allocation: Dict[str, float]
    target_allocation: Dict[str, float]
    portfolio_value: float


class RiskAssessmentRequest(BaseModel):
    age: int
    income: float
    expenses: float
    dependents: int = 0
    emergency_fund_months: float = 0


@router.post("/optimize")
async def optimize_portfolio(
    request: OptimizePortfolioRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Optimize portfolio allocation
    
    Args:
        request: Optimization parameters
        current_user: Authenticated user
        
    Returns:
        Optimized portfolio allocation
    """
    try:
        # Get user profile
        user_profile = await User.get_by_id(current_user.id)
        age = user_profile.get("age", 30)
        
        # Optimize portfolio
        optimization = portfolio_optimizer.optimize_portfolio(
            risk_tolerance=request.risk_tolerance,
            investment_amount=request.investment_amount,
            age=age,
            goals=request.goals
        )
        
        # Calculate risk metrics
        risk_metrics = risk_calculator.calculate_portfolio_risk(
            optimization["target_allocation"]
        )
        
        # Calculate efficient frontier
        efficient_frontier = portfolio_optimizer.calculate_efficient_frontier(
            min_return=5.0,
            max_return=15.0,
            steps=10
        )
        
        return {
            "success": True,
            "optimization": optimization,
            "risk_metrics": risk_metrics,
            "efficient_frontier": efficient_frontier,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-risk")
async def analyze_portfolio_risk(
    allocation: Dict[str, float],
    current_user: User = Depends(get_current_user)
):
    """
    Analyze portfolio risk
    
    Args:
        allocation: Asset allocation percentages
        current_user: Authenticated user
        
    Returns:
        Risk analysis
    """
    try:
        # Validate allocation
        total = sum(allocation.values())
        if abs(total - 100) > 0.1:
            raise HTTPException(
                status_code=400,
                detail=f"Allocation must sum to 100% (current: {total}%)"
            )
        
        # Calculate risk metrics
        risk_metrics = risk_calculator.calculate_portfolio_risk(allocation)
        
        # Calculate expected return
        expected_return = portfolio_optimizer._calculate_portfolio_return(allocation)
        
        # Calculate risk-adjusted returns
        risk_adjusted = risk_calculator.calculate_risk_adjusted_return(
            expected_return=expected_return,
            volatility=risk_metrics["portfolio_volatility"]
        )
        
        return {
            "success": True,
            "allocation": allocation,
            "risk_metrics": risk_metrics,
            "expected_return": round(expected_return, 2),
            "risk_adjusted_metrics": risk_adjusted,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rebalance")
async def analyze_rebalancing(
    request: RebalanceRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze rebalancing needs
    
    Args:
        request: Rebalancing parameters
        current_user: Authenticated user
        
    Returns:
        Rebalancing analysis and recommendations
    """
    try:
        # Analyze rebalancing need
        analysis = rebalancing_engine.analyze_rebalancing_need(
            current_allocation=request.current_allocation,
            target_allocation=request.target_allocation,
            portfolio_value=request.portfolio_value
        )
        
        # Get user profile for schedule recommendation
        user_profile = await User.get_by_id(current_user.id)
        risk_tolerance = user_profile.get("risk_tolerance", "moderate")
        
        # Calculate portfolio volatility
        portfolio_vol = risk_calculator._calculate_portfolio_volatility(
            request.target_allocation
        )
        
        # Generate rebalancing schedule
        schedule = rebalancing_engine.generate_rebalancing_schedule(
            risk_tolerance=risk_tolerance,
            portfolio_volatility=portfolio_vol
        )
        
        return {
            "success": True,
            "analysis": analysis,
            "schedule": schedule,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tax-efficient-rebalance")
async def tax_efficient_rebalancing(
    request: RebalanceRequest,
    cost_basis: Optional[Dict[str, float]] = None,
    holding_period: Optional[Dict[str, int]] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Generate tax-efficient rebalancing recommendations
    
    Args:
        request: Rebalancing parameters
        cost_basis: Cost basis for each asset
        holding_period: Holding period in months
        current_user: Authenticated user
        
    Returns:
        Tax-efficient rebalancing plan
    """
    try:
        # Generate tax-efficient plan
        plan = rebalancing_engine.calculate_tax_efficient_rebalancing(
            current_allocation=request.current_allocation,
            target_allocation=request.target_allocation,
            portfolio_value=request.portfolio_value,
            cost_basis=cost_basis,
            holding_period=holding_period
        )
        
        return {
            "success": True,
            "plan": plan,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/simulate-rebalancing")
async def simulate_rebalancing_impact(
    current_allocation: Dict[str, float],
    target_allocation: Dict[str, float],
    years: int = 5,
    current_user: User = Depends(get_current_user)
):
    """
    Simulate the impact of rebalancing
    
    Args:
        current_allocation: Current allocation
        target_allocation: Target allocation
        years: Simulation period
        current_user: Authenticated user
        
    Returns:
        Simulation results
    """
    try:
        # Get expected returns
        expected_returns = portfolio_optimizer.expected_returns
        
        # Simulate
        simulation = rebalancing_engine.simulate_rebalancing_impact(
            current_allocation=current_allocation,
            target_allocation=target_allocation,
            expected_returns=expected_returns,
            years=years
        )
        
        return {
            "success": True,
            "simulation": simulation,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/assess-risk-capacity")
async def assess_risk_capacity(
    request: RiskAssessmentRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Assess investor's risk capacity
    
    Args:
        request: Risk assessment parameters
        current_user: Authenticated user
        
    Returns:
        Risk capacity assessment
    """
    try:
        # Assess risk capacity
        assessment = risk_calculator.assess_risk_capacity(
            age=request.age,
            income=request.income,
            expenses=request.expenses,
            dependents=request.dependents,
            emergency_fund_months=request.emergency_fund_months
        )
        
        # Get recommended allocation based on capacity
        risk_level_map = {
            "very_low": "very_low",
            "low": "low",
            "moderate": "moderate",
            "high": "high"
        }
        
        risk_tolerance = risk_level_map.get(
            assessment["capacity_level"],
            "moderate"
        )
        
        recommended_allocation = portfolio_optimizer._get_target_allocation(
            risk_tolerance=risk_tolerance,
            age=request.age
        )
        
        return {
            "success": True,
            "assessment": assessment,
            "recommended_allocation": recommended_allocation,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/efficient-frontier")
async def get_efficient_frontier(
    min_return: float = 5.0,
    max_return: float = 15.0,
    steps: int = 20,
    current_user: User = Depends(get_current_user)
):
    """
    Calculate efficient frontier
    
    Args:
        min_return: Minimum return
        max_return: Maximum return
        steps: Number of points
        current_user: Authenticated user
        
    Returns:
        Efficient frontier points
    """
    try:
        # Calculate efficient frontier
        frontier = portfolio_optimizer.calculate_efficient_frontier(
            min_return=min_return,
            max_return=max_return,
            steps=steps
        )
        
        return {
            "success": True,
            "efficient_frontier": frontier,
            "min_return": min_return,
            "max_return": max_return,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/current-portfolio")
async def get_current_portfolio_analysis(
    current_user: User = Depends(get_current_user)
):
    """
    Analyze current portfolio
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Current portfolio analysis
    """
    try:
        # Get user's current investments
        financial_data = await FinancialModel.get_user_financial_summary(current_user.id)
        investments = financial_data.get("investments", {})
        
        if not investments or sum(investments.values()) == 0:
            raise HTTPException(
                status_code=404,
                detail="No investment data found"
            )
        
        # Calculate current allocation
        total_invested = sum(investments.values())
        current_allocation = {
            asset: (amount / total_invested * 100)
            for asset, amount in investments.items()
        }
        
        # Calculate risk metrics
        risk_metrics = risk_calculator.calculate_portfolio_risk(current_allocation)
        
        # Calculate expected return
        expected_return = portfolio_optimizer._calculate_portfolio_return(current_allocation)
        
        # Calculate risk-adjusted returns
        risk_adjusted = risk_calculator.calculate_risk_adjusted_return(
            expected_return=expected_return,
            volatility=risk_metrics["portfolio_volatility"]
        )
        
        # Get user profile
        user_profile = await User.get_by_id(current_user.id)
        age = user_profile.get("age", 30)
        risk_tolerance = user_profile.get("risk_tolerance", "moderate")
        
        # Get recommended allocation
        target_allocation = portfolio_optimizer._get_target_allocation(
            risk_tolerance=risk_tolerance,
            age=age
        )
        
        # Analyze rebalancing need
        rebalancing_analysis = rebalancing_engine.analyze_rebalancing_need(
            current_allocation=current_allocation,
            target_allocation=target_allocation,
            portfolio_value=total_invested
        )
        
        return {
            "success": True,
            "portfolio": {
                "total_value": round(total_invested, 2),
                "current_allocation": {k: round(v, 2) for k, v in current_allocation.items()},
                "target_allocation": {k: round(v, 2) for k, v in target_allocation.items()},
                "investments_by_asset": {k: round(v, 2) for k, v in investments.items()}
            },
            "risk_metrics": risk_metrics,
            "expected_return": round(expected_return, 2),
            "risk_adjusted_metrics": risk_adjusted,
            "rebalancing": rebalancing_analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
