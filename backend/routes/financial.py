"""
Financial Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import List, Optional, Dict
from datetime import date, datetime, timedelta
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

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

financial_router = APIRouter(prefix="/api/financial", tags=["Financial"])


class SimulationRequestBody(BaseModel):
    """Optional JSON body for scenario simulation (frontend uses JSON)."""
    new_loan: float = 0
    salary_increase: float = 0
    new_expense: float = 0
    investment_amount: float = 0
    months: int = 12


# ==================== EXPENSES ====================

@financial_router.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
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


@financial_router.get("/expenses", response_model=List[ExpenseResponse])
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


@financial_router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    current_user: Dict = Depends(get_current_user)
):
    """Update an expense"""
    try:
        user_id = current_user.get("sub")
        
        # AUTHORIZATION CHECK: Verify user owns this expense
        existing_expense = FinancialService.get_expense_by_id(expense_id)
        if not existing_expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        if existing_expense.get('user_id') != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized: You don't own this expense"
            )
        
        updates = expense.model_dump(exclude_unset=True)
        result = FinancialService.update_expense(expense_id, **updates)
        return ExpenseResponse(**result)
    except HTTPException:
        raise
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


@financial_router.delete("/expenses/{expense_id}")
async def delete_expense(
    expense_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """Delete an expense"""
    try:
        user_id = current_user.get("sub")
        
        # AUTHORIZATION CHECK: Verify user owns this expense
        existing_expense = FinancialService.get_expense_by_id(expense_id)
        if not existing_expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        if existing_expense.get('user_id') != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized: You don't own this expense"
            )
        
        FinancialService.delete_expense(expense_id)
        return {"success": True, "message": "Expense deleted"}
    except HTTPException:
        raise
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


@financial_router.get("/expenses/analytics")
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

@financial_router.post("/income", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
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


@financial_router.get("/income", response_model=List[IncomeResponse])
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

@financial_router.post("/goals", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
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


@financial_router.get("/goals", response_model=List[GoalResponse])
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


@financial_router.put("/goals/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: int,
    goal: GoalUpdate,
    current_user: Dict = Depends(get_current_user)
):
    """Update a goal"""
    try:
        user_id = current_user.get("sub")
        
        # AUTHORIZATION CHECK: Verify user owns this goal
        existing_goal = FinancialService.get_goal_by_id(goal_id)
        if not existing_goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        if existing_goal.get('user_id') != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized: You don't own this goal"
            )
        
        updates = goal.model_dump(exclude_unset=True)
        result = FinancialService.update_goal(goal_id, **updates)
        return GoalResponse(**result)
    except HTTPException:
        raise
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


@financial_router.delete("/goals/{goal_id}")
async def delete_goal(
    goal_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """Delete a goal"""
    try:
        user_id = current_user.get("sub")
        
        # AUTHORIZATION CHECK: Verify user owns this goal
        existing_goal = FinancialService.get_goal_by_id(goal_id)
        if not existing_goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        if existing_goal.get('user_id') != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized: You don't own this goal"
            )
        
        FinancialService.delete_goal(goal_id)
        return {"success": True, "message": "Goal deleted"}
    except HTTPException:
        raise
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

@financial_router.get("/alerts", response_model=List[AlertResponse])
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


@financial_router.post("/alerts/{alert_id}/read")
async def mark_alert_read(
    alert_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """Mark alert as read"""
    try:
        user_id = current_user.get("sub")
        
        # AUTHORIZATION CHECK: Verify user owns this alert
        existing_alert = AlertService.get_alert_by_id(alert_id)
        if not existing_alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found"
            )
        if existing_alert.get('user_id') != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized: You don't own this alert"
            )
        
        AlertService.mark_alert_read(alert_id)
        return {"success": True, "message": "Alert marked as read"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark alert: {str(e)}"
        )


@financial_router.post("/alerts/generate")
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

@financial_router.get("/recommendations", response_model=List[RecommendationResponse])
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


@financial_router.post("/recommendations/generate")
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


@financial_router.post("/recommendations/{rec_id}/status")
async def update_recommendation_status(
    rec_id: int,
    status: str = Query(..., pattern="^(pending|accepted|rejected)$"),
    current_user: Dict = Depends(get_current_user)
):
    """Update recommendation status"""
    try:
        user_id = current_user.get("sub")
        
        # AUTHORIZATION CHECK: Verify user owns this recommendation
        existing_rec = RecommendationService.get_recommendation_by_id(rec_id)
        if not existing_rec:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recommendation not found"
            )
        if existing_rec.get('user_id') != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized: You don't own this recommendation"
            )
        
        RecommendationService.update_recommendation_status(rec_id, status)
        return {"success": True, "message": "Status updated"}
    except HTTPException:
        raise
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

@financial_router.get("/metrics")
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


@financial_router.get("/health")
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


# ==================== SCENARIO SIMULATION ====================

@financial_router.post("/simulation")
async def run_scenario_simulation(
    body: Optional[SimulationRequestBody] = Body(default=None),
    new_loan: float = 0,
    salary_increase: float = 0,
    new_expense: float = 0,
    investment_amount: float = 0,
    months: int = 12,
    current_user: Dict = Depends(get_current_user)
):
    """
    Run what-if scenario simulation
    
    Simulates financial outcomes based on hypothetical changes:
    - New loan or debt
    - Salary increase/decrease
    - New recurring expense
    - Investment amount
    - Time period (months)
    
    Returns projected financial metrics and recommendations
    """
    try:
        user_id = current_user.get("sub")

        # Frontend posts JSON; tests/CLI may use query params. Support both.
        if body is not None:
            new_loan = body.new_loan
            salary_increase = body.salary_increase
            new_expense = body.new_expense
            investment_amount = body.investment_amount
            months = body.months
        
        # Get current financial data
        from database.db_utils import get_db
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Get current income
            cursor.execute("""
                SELECT amount FROM monthly_income
                WHERE user_id = ?
                ORDER BY month DESC
                LIMIT 1
            """, (user_id,))
            income_row = cursor.fetchone()
            current_income = income_row['amount'] if income_row else 75000
            
            # Get current expenses (last 30 days average)
            cursor.execute("""
                SELECT AVG(monthly_total) as avg_expense
                FROM (
                    SELECT strftime('%Y-%m', date) as month, SUM(amount) as monthly_total
                    FROM expenses
                    WHERE user_id = ? AND date >= date('now', '-90 days')
                    GROUP BY month
                )
            """, (user_id,))
            expense_row = cursor.fetchone()
            current_expense = expense_row['avg_expense'] if expense_row and expense_row['avg_expense'] else 45000
        
        # Calculate projected values
        projected_income = current_income + salary_increase
        projected_expense = current_expense + new_expense
        
        # Calculate loan impact (assuming 10% annual interest)
        monthly_loan_payment = 0
        if new_loan > 0:
            annual_rate = 0.10
            monthly_rate = annual_rate / 12
            num_payments = months
            if monthly_rate > 0:
                monthly_loan_payment = new_loan * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        
        projected_expense += monthly_loan_payment
        
        # Calculate investment growth (assuming 8% annual return)
        investment_value = 0
        if investment_amount > 0:
            monthly_return = 0.08 / 12
            investment_value = investment_amount * ((1 + monthly_return)**months)
        
        # Calculate monthly savings
        monthly_savings = projected_income - projected_expense
        total_savings = monthly_savings * months
        
        # Calculate final net worth
        final_net_worth = total_savings + investment_value - new_loan
        
        # Calculate savings rate
        savings_rate = (monthly_savings / projected_income * 100) if projected_income > 0 else 0
        
        # Generate recommendations
        recommendations = []
        
        if savings_rate < 10:
            recommendations.append({
                "type": "warning",
                "message": "Low savings rate. Consider reducing expenses or increasing income."
            })
        elif savings_rate >= 20:
            recommendations.append({
                "type": "success",
                "message": "Excellent savings rate! You're on track for financial security."
            })
        
        if new_loan > 0 and monthly_loan_payment > projected_income * 0.3:
            recommendations.append({
                "type": "warning",
                "message": "Loan payment exceeds 30% of income. This may strain your budget."
            })
        
        if investment_amount > 0:
            roi = ((investment_value - investment_amount) / investment_amount * 100) if investment_amount > 0 else 0
            recommendations.append({
                "type": "info",
                "message": f"Projected investment return: ₹{investment_value - investment_amount:,.0f} ({roi:.1f}% over {months} months)"
            })
        
        # Return simulation results
        debt_ratio = (projected_expense / projected_income * 100) if projected_income > 0 else 0
        is_viable = savings_rate >= 10 and debt_ratio < 50
        advice = (
            "This scenario looks viable. Keep maintaining a strong savings rate and monitor your EMI burden."
            if is_viable
            else "This scenario looks risky. Reduce expenses/loan size or increase income before proceeding."
        )

        # Backward-compatible flattened fields for the frontend UI component.
        response_payload = {
            "success": True,
            "newSavings": monthly_savings,
            "newEMI": monthly_loan_payment,
            "newRiskScore": max(0, min(100, 100 - savings_rate)),  # heuristic
            "newDebtRatio": max(0, min(100, debt_ratio)),
            "isViable": is_viable,
            "advice": advice,
            "simulation": {
                "current": {
                    "monthly_income": current_income,
                    "monthly_expense": current_expense,
                    "monthly_savings": current_income - current_expense,
                    "savings_rate": ((current_income - current_expense) / current_income * 100) if current_income > 0 else 0
                },
                "projected": {
                    "monthly_income": projected_income,
                    "monthly_expense": projected_expense,
                    "monthly_savings": monthly_savings,
                    "savings_rate": savings_rate,
                    "loan_payment": monthly_loan_payment,
                    "investment_value": investment_value,
                    "total_savings": total_savings,
                    "final_net_worth": final_net_worth
                },
                "changes": {
                    "income_change": salary_increase,
                    "expense_change": new_expense + monthly_loan_payment,
                    "savings_change": monthly_savings - (current_income - current_expense),
                    "net_worth_change": final_net_worth
                },
                "timeline": {
                    "months": months,
                    "start_date": datetime.now().strftime("%Y-%m"),
                    "end_date": (datetime.now().replace(day=1) + timedelta(days=32*months)).strftime("%Y-%m")
                }
            },
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
        return response_payload
        
    except Exception as e:
        logger.error(f"Error running simulation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to run simulation: {str(e)}"
        )
