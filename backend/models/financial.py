"""
Financial Model
Database operations for financial data
"""

from typing import List, Optional, Dict
from datetime import datetime, timezone
from database.connection_enhanced import get_db


class FinancialModel:
    """Financial data database operations"""
    
    # ==================== EXPENSES ====================
    
    @staticmethod
    def create_expense(
        user_id: str,
        date: str,
        amount: float,
        category: str,
        description: str,
        merchant: Optional[str] = None
    ) -> Dict:
        """Create a new expense"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO expenses (user_id, date, amount, category, description, merchant)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, date, amount, category, description, merchant))
            
            expense_id = cursor.lastrowid
            cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def get_expense_by_id(expense_id: int) -> Optional[Dict]:
        """Get expense by ID"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM expenses WHERE id = ?
            """, (expense_id,))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    @staticmethod
    def get_user_expenses(
        user_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict]:
        """Get user expenses with optional filters"""
        query = "SELECT * FROM expenses WHERE user_id = ?"
        params = [user_id]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY date DESC"
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def update_expense(expense_id: int, **kwargs) -> Optional[Dict]:
        """Update expense"""
        allowed_fields = ['date', 'amount', 'category', 'description', 'merchant']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            return FinancialModel.get_expense_by_id(expense_id)
        
        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        values = list(update_fields.values()) + [expense_id]
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE expenses SET {set_clause} WHERE id = ?
            """, values)
        
        return FinancialModel.get_expense_by_id(expense_id)

    @staticmethod
    def get_goal_by_id(goal_id: int) -> Optional[Dict]:
        """Get goal by id."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM goals WHERE id = ?
            """, (goal_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def delete_expense(expense_id: int) -> bool:
        """Delete expense"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            return cursor.rowcount > 0
    
    # ==================== INCOME ====================
    
    @staticmethod
    def create_income(user_id: str, month: str, amount: float, source: str) -> Dict:
        """Create income record"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO monthly_income (user_id, month, amount, source)
                VALUES (?, ?, ?, ?)
            """, (user_id, month, amount, source))
            
            income_id = cursor.lastrowid
            cursor.execute("SELECT * FROM monthly_income WHERE id = ?", (income_id,))
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_user_income(
        user_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """Get user income records"""
        query = "SELECT * FROM monthly_income WHERE user_id = ?"
        params = [user_id]
        
        if start_date:
            query += " AND month >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND month <= ?"
            params.append(end_date)
        
        query += " ORDER BY month DESC"
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== GOALS ====================
    
    @staticmethod
    def create_goal(
        user_id: str,
        name: str,
        target_amount: float,
        deadline: str,
        category: str
    ) -> Dict:
        """Create a new goal"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO goals (user_id, name, target_amount, deadline, category)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, name, target_amount, deadline, category))
            
            goal_id = cursor.lastrowid
            cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_user_goals(user_id: str, status: Optional[str] = None) -> List[Dict]:
        """Get user goals"""
        query = "SELECT * FROM goals WHERE user_id = ?"
        params = [user_id]
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def update_goal(goal_id: int, **kwargs) -> Optional[Dict]:
        """Update goal"""
        allowed_fields = ['name', 'target_amount', 'current_amount', 'deadline', 'category', 'status']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        
        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        values = list(update_fields.values()) + [datetime.now(timezone.utc), goal_id]
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE goals SET {set_clause}, updated_at = ? WHERE id = ?
            """, values)
            
            cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def delete_goal(goal_id: int) -> bool:
        """Delete goal"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
            return cursor.rowcount > 0
    
    # ==================== ALERTS ====================
    
    @staticmethod
    def create_alert(
        user_id: str,
        alert_type: str,
        title: str,
        message: str,
        severity: str
    ) -> Dict:
        """Create an alert"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO alerts (user_id, type, title, message, severity)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, alert_type, title, message, severity))
            
            alert_id = cursor.lastrowid
            cursor.execute("SELECT * FROM alerts WHERE id = ?", (alert_id,))
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_user_alerts(user_id: str, is_read: Optional[bool] = None) -> List[Dict]:
        """Get user alerts"""
        query = "SELECT * FROM alerts WHERE user_id = ?"
        params = [user_id]
        
        if is_read is not None:
            query += " AND is_read = ?"
            params.append(1 if is_read else 0)
        
        query += " ORDER BY created_at DESC"
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def mark_alert_as_read(alert_id: int) -> bool:
        """Mark alert as read"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE alerts SET is_read = 1 WHERE id = ?", (alert_id,))
            return cursor.rowcount > 0
    
    # ==================== RECOMMENDATIONS ====================
    
    @staticmethod
    def create_recommendation(
        user_id: str,
        category: str,
        title: str,
        description: str,
        priority: str,
        impact: Optional[str] = None
    ) -> Dict:
        """Create a recommendation"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO recommendations (user_id, category, title, description, priority, impact)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, category, title, description, priority, impact))
            
            rec_id = cursor.lastrowid
            cursor.execute("SELECT * FROM recommendations WHERE id = ?", (rec_id,))
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_user_recommendations(user_id: str, status: Optional[str] = None) -> List[Dict]:
        """Get user recommendations"""
        query = "SELECT * FROM recommendations WHERE user_id = ?"
        params = [user_id]
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def update_recommendation_status(rec_id: int, status: str) -> bool:
        """Update recommendation status"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE recommendations SET status = ? WHERE id = ?
            """, (status, rec_id))
            return cursor.rowcount > 0
