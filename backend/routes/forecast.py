"""
Forecast Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict
from services.forecast_service import ForecastService
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/forecast", tags=["Forecasting"])


@router.get("/monthly")
async def get_monthly_forecast(
    months: int = Query(6, ge=1, le=24),
    current_user: Dict = Depends(get_current_user)
):
    """Get monthly income/expense/savings forecast"""
    try:
        user_id = current_user.get("sub")
        return ForecastService.get_monthly_forecast(user_id, months)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate forecast: {str(e)}"
        )


@router.get("/networth")
async def get_networth_forecast(
    years: int = Query(5, ge=1, le=20),
    current_user: Dict = Depends(get_current_user)
):
    """Get multi-year net worth projection"""
    try:
        user_id = current_user.get("sub")
        return ForecastService.get_networth_forecast(user_id, years)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate forecast: {str(e)}"
        )


@router.get("/goals")
async def get_goal_forecast(current_user: Dict = Depends(get_current_user)):
    """Get goal completion timeline forecast"""
    try:
        user_id = current_user.get("sub")
        return ForecastService.get_goal_forecast(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate forecast: {str(e)}"
        )


@router.get("/expenses")
async def get_expense_forecast(
    months: int = Query(6, ge=1, le=24),
    current_user: Dict = Depends(get_current_user)
):
    """Get category-wise expense trend forecast"""
    try:
        user_id = current_user.get("sub")
        return ForecastService.get_expense_forecast(user_id, months)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate forecast: {str(e)}"
        )


@router.get("/savings")
async def get_savings_projection(current_user: Dict = Depends(get_current_user)):
    """Get savings projection at different rates"""
    try:
        user_id = current_user.get("sub")
        return ForecastService.get_savings_projection(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate projection: {str(e)}"
        )


@router.get("/ml")
async def get_ml_forecast(
    steps: int = Query(6, ge=1, le=24),
    current_user: Dict = Depends(get_current_user)
):
    """Get ML-based forecast using multiple models"""
    try:
        user_id = current_user.get("sub")
        return ForecastService.get_ml_forecast(user_id, steps)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate ML forecast: {str(e)}"
        )


@router.post("/scenario")
async def run_scenario_simulation(
    new_loan: float = 0,
    salary_increase: float = 0,
    job_loss: bool = False,
    vacation_expense: float = 0,
    house_purchase: bool = False,
    car_purchase: bool = False,
    investment_increase: float = 0,
    current_user: Dict = Depends(get_current_user)
):
    """Run what-if scenario simulation"""
    try:
        user_id = current_user.get("sub")
        return ForecastService.run_scenario_simulation(
            user_id=user_id,
            new_loan=new_loan,
            salary_increase=salary_increase,
            job_loss=job_loss,
            vacation_expense=vacation_expense,
            house_purchase=house_purchase,
            car_purchase=car_purchase,
            investment_increase=investment_increase
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to run simulation: {str(e)}"
        )
