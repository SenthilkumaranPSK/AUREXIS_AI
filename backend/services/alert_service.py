"""
Alert Service
Manage user alerts and notifications
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from database.db_utils import get_db

logger = logging.getLogger(__name__)


class AlertService:
    """Manage user alerts and notifications"""
    
    @staticmethod
    def get_stored_alerts(
        user_id: str,
        is_read: Optional[bool] = None
    ) -> List[Dict]:
        """
        Get stored alerts for a user
        
        Args:
            user_id: User identifier
            is_read: Filter by read status
            
        Returns:
            List of alert dictionaries
        """
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                
                if is_read is not None:
                    cursor.execute("""
                        SELECT id, user_id, type, title, message, severity,
                               is_read, created_at
                        FROM alerts
                        WHERE user_id = ? AND is_read = ?
                        ORDER BY created_at DESC
                    """, (user_id, 1 if is_read else 0))
                else:
                    cursor.execute("""
                        SELECT id, user_id, type, title, message, severity,
                               is_read, created_at
                        FROM alerts
                        WHERE user_id = ?
                        ORDER BY created_at DESC
                    """, (user_id,))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error fetching alerts: {e}")
            return []
    
    @staticmethod
    def get_alert_by_id(alert_id: int) -> Optional[Dict]:
        """Get a single alert by ID"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, user_id, type, title, message, severity,
                           is_read, created_at
                    FROM alerts
                    WHERE id = ?
                """, (alert_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error fetching alert: {e}")
            return None
    
    @staticmethod
    def mark_alert_read(alert_id: int) -> bool:
        """
        Mark an alert as read
        
        Args:
            alert_id: Alert ID
            
        Returns:
            True if successful
        """
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE alerts
                    SET is_read = 1
                    WHERE id = ?
                """, (alert_id,))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error marking alert as read: {e}")
            return False
    
    @staticmethod
    def generate_alerts(user_id: str) -> Dict:
        """
        Generate new alerts based on user's financial patterns
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with generated alerts count
        """
        alerts_created = 0
        
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                
                # Check for large expenses in last 7 days
                cursor.execute("""
                    SELECT amount, category, date
                    FROM expenses
                    WHERE user_id = ? 
                    AND date >= date('now', '-7 days')
                    AND amount > 10000
                    ORDER BY amount DESC
                    LIMIT 5
                """, (user_id,))
                
                large_expenses = cursor.fetchall()
                for expense in large_expenses:
                    AlertService.create_alert(
                        user_id=user_id,
                        alert_type="expense",
                        title="Large Expense Detected",
                        message=f"Large {expense['category']} expense of ₹{expense['amount']:,.0f} on {expense['date']}",
                        severity="medium"
                    )
                    alerts_created += 1
                
                # Check for approaching goal deadlines
                cursor.execute("""
                    SELECT id, name, target_amount, current_amount, deadline
                    FROM goals
                    WHERE user_id = ?
                    AND status = 'active'
                    AND deadline <= date('now', '+30 days')
                    AND deadline >= date('now')
                """, (user_id,))
                
                approaching_goals = cursor.fetchall()
                for goal in approaching_goals:
                    progress = (goal['current_amount'] / goal['target_amount']) * 100 if goal['target_amount'] > 0 else 0
                    AlertService.create_alert(
                        user_id=user_id,
                        alert_type="goal",
                        title="Goal Deadline Approaching",
                        message=f"Your goal '{goal['name']}' is due on {goal['deadline']}. Current progress: {progress:.1f}%",
                        severity="high" if progress < 50 else "medium"
                    )
                    alerts_created += 1
                
                # Check for unusual spending patterns
                cursor.execute("""
                    SELECT category, SUM(amount) as total
                    FROM expenses
                    WHERE user_id = ?
                    AND date >= date('now', '-7 days')
                    GROUP BY category
                    HAVING total > (
                        SELECT AVG(category_total) * 1.5
                        FROM (
                            SELECT SUM(amount) as category_total
                            FROM expenses
                            WHERE user_id = ?
                            AND date >= date('now', '-30 days')
                            AND date < date('now', '-7 days')
                            GROUP BY category
                        )
                    )
                """, (user_id, user_id))
                
                unusual_spending = cursor.fetchall()
                for spending in unusual_spending:
                    AlertService.create_alert(
                        user_id=user_id,
                        alert_type="spending",
                        title="Unusual Spending Pattern",
                        message=f"Your {spending['category']} spending is 50% higher than usual this week (₹{spending['total']:,.0f})",
                        severity="medium"
                    )
                    alerts_created += 1
                
                logger.info(f"Generated {alerts_created} alerts for user {user_id}")
                
        except Exception as e:
            logger.error(f"Error generating alerts: {e}")
        
        return {"alerts_created": alerts_created}
    
    @staticmethod
    def create_alert(
        user_id: str,
        alert_type: str,
        title: str,
        message: str,
        severity: str = "medium"
    ) -> Optional[Dict]:
        """
        Create a new alert
        
        Args:
            user_id: User identifier
            alert_type: Type of alert (expense, goal, spending, etc.)
            title: Alert title
            message: Alert message
            severity: Severity level (low, medium, high, critical)
            
        Returns:
            Created alert dictionary or None
        """
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO alerts 
                    (user_id, type, title, message, severity, is_read)
                    VALUES (?, ?, ?, ?, ?, 0)
                """, (user_id, alert_type, title, message, severity))
                
                alert_id = cursor.lastrowid
                conn.commit()
                
                return {
                    "id": alert_id,
                    "user_id": user_id,
                    "type": alert_type,
                    "title": title,
                    "message": message,
                    "severity": severity,
                    "is_read": False,
                    "created_at": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return None
    
    @staticmethod
    def delete_old_alerts(user_id: str, days: int = 90) -> int:
        """
        Delete alerts older than specified days
        
        Args:
            user_id: User identifier
            days: Number of days to keep
            
        Returns:
            Number of alerts deleted
        """
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM alerts
                    WHERE user_id = ?
                    AND created_at < datetime('now', '-' || ? || ' days')
                """, (user_id, days))
                deleted_count = cursor.rowcount
                conn.commit()
                return deleted_count
        except Exception as e:
            logger.error(f"Error deleting old alerts: {e}")
            return 0
