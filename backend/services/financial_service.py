"""
Financial Service
Business logic for financial operations
"""

from typing import List, Optional, Dict
from datetime import datetime, date
from analytics import compute_metrics, compute_expenses
from health import compute_health
from user_manager_json import UserManagerJSON


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
        """Create a new expense - Not implemented in JSON version"""
        # In JSON-based version, expenses are read-only from JSON files
        # To implement: Add expense to user's JSON file
        return {
            "message": "Expense creation not implemented in JSON version",
            "note": "Expenses are loaded from JSON files"
        }
    
    @staticmethod
    def get_expenses(
        user_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category: Optional[str] = None
    ) -> List[Dict]:
        """Get user expenses with filters"""
        # Load from JSON files
        data = UserManagerJSON.get_all_user_data(user_id)
        bank_data = data.get('fetch_bank_transactions', {})
        
        # Extract expenses from bank transactions
        expenses = []
        for bank in bank_data.get('bankTransactions', []):
            for txn in bank.get('txns', []):
                if len(txn) >= 6 and txn[3] == 2:  # Type 2 = DEBIT
                    expenses.append({
                        'amount': float(txn[0]),
                        'description': txn[1],
                        'date': txn[2],
                        'category': 'General',  # Could be parsed from description
                        'merchant': txn[1].split('-')[0] if '-' in txn[1] else 'Unknown'
                    })
        
        return expenses

    @staticmethod
    def get_expense_by_id(expense_id: int) -> Optional[Dict]:
        """Get an expense by id - Not implemented in JSON version"""
        return None
    
    @staticmethod
    def update_expense(expense_id: int, **kwargs) -> Dict:
        """Update expense - Not implemented in JSON version"""
        return {"message": "Update not implemented in JSON version"}
    
    @staticmethod
    def delete_expense(expense_id: int) -> bool:
        """Delete expense - Not implemented in JSON version"""
        return False
    
    @staticmethod
    def get_expense_analytics(user_id: str) -> Dict:
        """Get expense analytics"""
        data = UserManagerJSON.get_all_user_data(user_id)
        return compute_expenses(data)
    
    # ==================== INCOME ====================
    
    @staticmethod
    def create_income(user_id: str, month: date, amount: float, source: str) -> Dict:
        """Create income record - Not implemented in JSON version"""
        return {"message": "Income creation not implemented in JSON version"}
    
    @staticmethod
    def get_income(
        user_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict]:
        """Get user income records"""
        # Load from JSON files
        data = UserManagerJSON.get_all_user_data(user_id)
        bank_data = data.get('fetch_bank_transactions', {})
        
        # Extract income from bank transactions
        income = []
        for bank in bank_data.get('bankTransactions', []):
            for txn in bank.get('txns', []):
                if len(txn) >= 6 and txn[3] == 1:  # Type 1 = CREDIT
                    income.append({
                        'amount': float(txn[0]),
                        'description': txn[1],
                        'date': txn[2],
                        'source': 'Salary' if 'SALARY' in txn[1] else 'Other'
                    })
        
        return income
    
    # ==================== GOALS ====================
    
    @staticmethod
    def create_goal(
        user_id: str,
        name: str,
        target_amount: float,
        deadline: date,
        category: str
    ) -> Dict:
        """Create a new goal - Not implemented in JSON version"""
        return {"message": "Goal creation not implemented in JSON version"}
    
    @staticmethod
    def get_goals(user_id: str, status: Optional[str] = None) -> List[Dict]:
        """Get user goals"""
        from datetime import datetime, timedelta
        # Load from user profile
        data = UserManagerJSON.get_all_user_data(user_id)
        profile = data.get('profile', {})
        
        # Return financial goals from profile
        goals = []
        goal_id = 1
        for goal_name in profile.get('financial_goals', []):
            # Create a deadline 1 year from now
            deadline = (datetime.now() + timedelta(days=365)).date()
            created_at = datetime.now()
            
            goals.append({
                'id': goal_id,
                'user_id': user_id,
                'name': goal_name,
                'target_amount': 100000.0,  # Default target
                'current_amount': 0.0,
                'deadline': deadline,
                'category': 'General',
                'status': 'active',
                'progress': 0.0,
                'created_at': created_at,
                'updated_at': created_at
            })
            goal_id += 1
        
        return goals

    @staticmethod
    def get_goal_by_id(goal_id: int) -> Optional[Dict]:
        """Get a goal by id - Not implemented in JSON version"""
        return None
    
    @staticmethod
    def update_goal(goal_id: int, **kwargs) -> Dict:
        """Update goal - Not implemented in JSON version"""
        return {"message": "Update not implemented in JSON version"}
    
    @staticmethod
    def delete_goal(goal_id: int) -> bool:
        """Delete goal - Not implemented in JSON version"""
        return False
    
    # ==================== ALERTS ====================
    
    @staticmethod
    def get_alerts(user_id: str, is_read: Optional[bool] = None) -> List[Dict]:
        """Get user alerts"""
        # Generate alerts based on user data
        return []
    
    @staticmethod
    def mark_alert_read(alert_id: int) -> bool:
        """Mark alert as read - Not implemented in JSON version"""
        return False
    
    # ==================== RECOMMENDATIONS ====================
    
    @staticmethod
    def get_recommendations(user_id: str, status: Optional[str] = None) -> List[Dict]:
        """Get user recommendations"""
        # Generate recommendations based on user data
        return []
    
    @staticmethod
    def update_recommendation_status(rec_id: int, status: str) -> bool:
        """Update recommendation status - Not implemented in JSON version"""
        return False
    
    # ==================== ANALYTICS ====================
    
    @staticmethod
    def get_financial_metrics(user_id: str) -> Dict:
        """Get key financial metrics"""
        data = UserManagerJSON.get_all_user_data(user_id)
        return compute_metrics(data)
    
    @staticmethod
    def get_financial_health(user_id: str) -> Dict:
        """Get financial health score"""
        data = UserManagerJSON.get_all_user_data(user_id)
        data.setdefault("user_id", user_id)
        return compute_health(data)
    
    @staticmethod
    def get_risk_analysis(user_id: str) -> Dict:
        """Get risk analysis and assessment"""
        from analytics import compute_risk
        data = UserManagerJSON.get_all_user_data(user_id)
        return compute_risk(data)
