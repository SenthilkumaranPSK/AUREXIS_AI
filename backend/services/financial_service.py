"""
Financial Service
Business logic for financial operations
"""

from typing import List, Optional, Dict
from datetime import datetime, date
from models.financial import FinancialModel
from analytics_legacy import compute_metrics, compute_expenses
from health import compute_health
from user_manager import get_all_user_data


class FinancialService:
    """Financial data business logic"""
    
    # ==================== EXPENSES ====================
    
    @staticmethod
    def create_expense(
        user_id: str,
        date: date,
        amount: float,
        category: str,
        description: str,
        merchant: Optional[str] = None
    ) -> Dict:
        """Create a new expense"""
        expense = FinancialModel.create_expense(
            user_id=user_id,
            date=date.isoformat(),
            amount=amount,
            category=category,
            description=description,
            merchant=merchant
        )
        return expense
    
    @staticmethod
    def get_expenses(
        user_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category: Optional[str] = None
    ) -> List[Dict]:
        """Get user expenses with filters"""
        return FinancialModel.get_user_expenses(
            user_id=user_id,
            start_date=start_date.isoformat() if start_date else None,
            end_date=end_date.isoformat() if end_date else None,
            category=category
        )
    
    @staticmethod
    def update_expense(expense_id: int, **kwargs) -> Dict:
        """Update expense"""
        # Convert date to string if present
        if 'date' in kwargs and isinstance(kwargs['date'], date):
            kwargs['date'] = kwargs['date'].isoformat()
        
        expense = FinancialModel.update_expense(expense_id, **kwargs)
        if not expense:
            raise ValueError("Expense not found")
        return expense
    
    @staticmethod
    def delete_expense(expense_id: int) -> bool:
        """Delete expense"""
        success = FinancialModel.delete_expense(expense_id)
        if not success:
            raise ValueError("Expense not found")
        return success
    
    @staticmethod
    def get_expense_analytics(user_id: str) -> Dict:
        """Get expense analytics"""
        data = get_all_user_data(user_id)
        return compute_expenses(data)
    
    # ==================== INCOME ====================
    
    @staticmethod
    def create_income(user_id: str, month: date, amount: float, source: str) -> Dict:
        """Create income record"""
        return FinancialModel.create_income(
            user_id=user_id,
            month=month.isoformat(),
            amount=amount,
            source=source
        )
    
    @staticmethod
    def get_income(
        user_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict]:
        """Get user income records"""
        return FinancialModel.get_user_income(
            user_id=user_id,
            start_date=start_date.isoformat() if start_date else None,
            end_date=end_date.isoformat() if end_date else None
        )
    
    # ==================== GOALS ====================
    
    @staticmethod
    def create_goal(
        user_id: str,
        name: str,
        target_amount: float,
        deadline: date,
        category: str
    ) -> Dict:
        """Create a new goal"""
        goal = FinancialModel.create_goal(
            user_id=user_id,
            name=name,
            target_amount=target_amount,
            deadline=deadline.isoformat(),
            category=category
        )
        # Add progress calculation
        goal['progress'] = (goal['current_amount'] / goal['target_amount'] * 100) if goal['target_amount'] > 0 else 0
        return goal
    
    @staticmethod
    def get_goals(user_id: str, status: Optional[str] = None) -> List[Dict]:
        """Get user goals"""
        goals = FinancialModel.get_user_goals(user_id, status)
        # Add progress to each goal
        for goal in goals:
            goal['progress'] = (goal['current_amount'] / goal['target_amount'] * 100) if goal['target_amount'] > 0 else 0
        return goals
    
    @staticmethod
    def update_goal(goal_id: int, **kwargs) -> Dict:
        """Update goal"""
        # Convert date to string if present
        if 'deadline' in kwargs and isinstance(kwargs['deadline'], date):
            kwargs['deadline'] = kwargs['deadline'].isoformat()
        
        goal = FinancialModel.update_goal(goal_id, **kwargs)
        if not goal:
            raise ValueError("Goal not found")
        
        # Add progress calculation
        goal['progress'] = (goal['current_amount'] / goal['target_amount'] * 100) if goal['target_amount'] > 0 else 0
        return goal
    
    @staticmethod
    def delete_goal(goal_id: int) -> bool:
        """Delete goal"""
        success = FinancialModel.delete_goal(goal_id)
        if not success:
            raise ValueError("Goal not found")
        return success
    
    # ==================== ALERTS ====================
    
    @staticmethod
    def get_alerts(user_id: str, is_read: Optional[bool] = None) -> List[Dict]:
        """Get user alerts"""
        return FinancialModel.get_user_alerts(user_id, is_read)
    
    @staticmethod
    def mark_alert_read(alert_id: int) -> bool:
        """Mark alert as read"""
        return FinancialModel.mark_alert_as_read(alert_id)
    
    # ==================== RECOMMENDATIONS ====================
    
    @staticmethod
    def get_recommendations(user_id: str, status: Optional[str] = None) -> List[Dict]:
        """Get user recommendations"""
        return FinancialModel.get_user_recommendations(user_id, status)
    
    @staticmethod
    def update_recommendation_status(rec_id: int, status: str) -> bool:
        """Update recommendation status"""
        return FinancialModel.update_recommendation_status(rec_id, status)
    
    # ==================== ANALYTICS ====================
    
    @staticmethod
    def get_financial_metrics(user_id: str) -> Dict:
        """Get key financial metrics"""
        data = get_all_user_data(user_id)
        return compute_metrics(data)
    
    @staticmethod
    def get_financial_health(user_id: str) -> Dict:
        """Get financial health score"""
        data = get_all_user_data(user_id)
        return compute_health(data)
