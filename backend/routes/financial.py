"""
Financial Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict
from datetime import date
from schemas.financial import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    IncomeCreate,
    IncomeResponse,
    GoalCreate,
    GoalUpdate,
    GoalResponse,
    AlertResponse,
    RecommendationResponse
)
from services.financial_service import FinancialService
from services.recommendation_service import RecommendationService
from services.alert_service import AlertService
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/financial", tags=["Financial"])


# ==================== EXPENSES ====================

@router.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense: ExpenseCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new expense"""
    try:
        user_id = current_user.get("sub")
        result = FinancialService.create_expense(
            user_id=user_id,
            date=expense.date,
            amount=expense.amount,
            category=expense.category,
            description=expense.description,
            merchant=expense.merchant
        )
        return ExpenseResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create expense: {str(e)}"
        )


@router.get("/expenses", response_model=List[ExpenseResponse])
async def get_expenses(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """Get user expenses with optional filters"""
    try:
        user_id = current_user.get("sub")
        expenses = FinancialService.get_expenses(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            category=category
        )
        return [ExpenseResponse(**exp) for exp in expenses]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch expenses: {str(e)}"
        )


@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    current_user: Dict = Depends(get_current_user)
):
    """Update an expense"""
    try:
        updates = expense.model_dump(exclude_unset=True)
        result = FinancialService.update_expense(expense_id, **updates)
        return ExpenseResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update expense: {str(e)}"
        )


@router.delete("/expenses/{expense_id}")
async def delete_expense(
    expense_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """Delete an expense"""
    try:
        FinancialService.delete_expense(expense_id)
        return {"success": True, "message": "Expense deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete expense: {str(e)}"
        )


@router.get("/expenses/analytics")
async def get_expense_analytics(current_user: Dict = Depends(get_current_user)):
    """Get expense analytics"""
    try:
        user_id = current_user.get("sub")
        return FinancialService.get_expense_analytics(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch analytics: {str(e)}"
        )


# ==================== INCOME ====================

@router.post("/income", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
async def create_income(
    income: IncomeCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Create income record"""
    try:
        user_id = current_user.get("sub")
        result = FinancialService.create_income(
            user_id=user_id,
            month=income.month,
            amount=income.amount,
            source=income.source
        )
        return IncomeResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create income: {str(e)}"
        )


@router.get("/income", response_model=List[IncomeResponse])
async def get_income(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: Dict = Depends(get_current_user)
):
    """Get user income records"""
    try:
        user_id = current_user.get("sub")
        income_records = FinancialService.get_income(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        return [IncomeResponse(**inc) for inc in income_records]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch income: {str(e)}"
        )


# ==================== GOALS ====================

@router.post("/goals", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal: GoalCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new goal"""
    try:
        user_id = current_user.get("sub")
        result = FinancialService.create_goal(
            user_id=user_id,
            name=goal.name,
            target_amount=goal.target_amount,
            deadline=goal.deadline,
            category=goal.category
        )
        return GoalResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create goal: {str(e)}"
        )


@router.get("/goals", response_model=List[GoalResponse])
async def get_goals(
    status: Optional[str] = Query(None, pattern="^(active|completed|cancelled)$"),
    current_user: Dict = Depends(get_current_user)
):
    """Get user goals"""
    try:
        user_id = current_user.get("sub")
        goals = FinancialService.get_goals(user_id, status)
        return [GoalResponse(**goal) for goal in goals]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch goals: {str(e)}"
        )


@router.put("/goals/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: int,
    goal: GoalUpdate,
    current_user: Dict = Depends(get_current_user)
):
    """Update a goal"""
    try:
        updates = goal.model_dump(exclude_unset=True)
        result = FinancialService.update_goal(goal_id, **updates)
        return GoalResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update goal: {str(e)}"
        )


@router.delete("/goals/{goal_id}")
async def delete_goal(
    goal_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """Delete a goal"""
    try:
        FinancialService.delete_goal(goal_id)
        return {"success": True, "message": "Goal deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete goal: {str(e)}"
        )


# ==================== ALERTS ====================

@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(
    is_read: Optional[bool] = None,
    current_user: Dict = Depends(get_current_user)
):
    """Get user alerts"""
    try:
        user_id = current_user.get("sub")
        alerts = AlertService.get_stored_alerts(user_id, is_read)
        return [AlertResponse(**alert) for alert in alerts]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch alerts: {str(e)}"
        )


@router.post("/alerts/{alert_id}/read")
async def mark_alert_read(
    alert_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """Mark alert as read"""
    try:
        AlertService.mark_alert_read(alert_id)
        return {"success": True, "message": "Alert marked as read"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark alert: {str(e)}"
        )


@router.post("/alerts/generate")
async def generate_alerts(current_user: Dict = Depends(get_current_user)):
    """Generate new alerts from data patterns"""
    try:
        user_id = current_user.get("sub")
        return AlertService.generate_alerts(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate alerts: {str(e)}"
        )


# ==================== RECOMMENDATIONS ====================

@router.get("/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(
    status: Optional[str] = Query(None, pattern="^(pending|accepted|rejected)$"),
    current_user: Dict = Depends(get_current_user)
):
    """Get user recommendations"""
    try:
        user_id = current_user.get("sub")
        recommendations = RecommendationService.get_stored_recommendations(user_id, status)
        return [RecommendationResponse(**rec) for rec in recommendations]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch recommendations: {str(e)}"
        )


@router.post("/recommendations/generate")
async def generate_recommendations(current_user: Dict = Depends(get_current_user)):
    """Generate new recommendations"""
    try:
        user_id = current_user.get("sub")
        return {
            "recommendations": RecommendationService.generate_recommendations(user_id)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.post("/recommendations/{rec_id}/status")
async def update_recommendation_status(
    rec_id: int,
    status: str = Query(..., pattern="^(pending|accepted|rejected)$"),
    current_user: Dict = Depends(get_current_user)
):
    """Update recommendation status"""
    try:
        RecommendationService.update_recommendation_status(rec_id, status)
        return {"success": True, "message": "Status updated"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update status: {str(e)}"
        )


# ==================== ANALYTICS ====================

@router.get("/metrics")
async def get_financial_metrics(current_user: Dict = Depends(get_current_user)):
    """Get key financial metrics"""
    try:
        user_id = current_user.get("sub")
        return FinancialService.get_financial_metrics(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch metrics: {str(e)}"
        )


@router.get("/health")
async def get_financial_health(current_user: Dict = Depends(get_current_user)):
    """Get financial health score"""
    try:
        user_id = current_user.get("sub")
        return FinancialService.get_financial_health(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch health score: {str(e)}"
        )
