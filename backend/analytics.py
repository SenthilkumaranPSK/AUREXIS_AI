"""
Analytics Module
Financial analytics and insights generation
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from database.db_utils import get_db

logger = logging.getLogger(__name__)


def get_spending_trends(user_id: str, days: int = 30) -> Dict:
    """
    Analyze spending trends over time
    
    Args:
        user_id: User identifier
        days: Number of days to analyze
        
    Returns:
        Dictionary with trend analysis
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Get daily spending
            cursor.execute("""
                SELECT date, SUM(amount) as daily_total
                FROM expenses
                WHERE user_id = ? AND date >= date('now', '-' || ? || ' days')
                GROUP BY date
                ORDER BY date
            """, (user_id, days))
            
            daily_spending = [dict(row) for row in cursor.fetchall()]
            
            # Calculate average
            total = sum(day['daily_total'] for day in daily_spending)
            avg_daily = total / days if days > 0 else 0
            
            # Get category breakdown
            cursor.execute("""
                SELECT category, SUM(amount) as total, COUNT(*) as count
                FROM expenses
                WHERE user_id = ? AND date >= date('now', '-' || ? || ' days')
                GROUP BY category
                ORDER BY total DESC
            """, (user_id, days))
            
            category_breakdown = [dict(row) for row in cursor.fetchall()]
            
            return {
                "period_days": days,
                "total_spending": total,
                "average_daily": avg_daily,
                "daily_spending": daily_spending,
                "category_breakdown": category_breakdown
            }
    except Exception as e:
        logger.error(f"Error analyzing spending trends: {e}")
        return {}


def get_category_insights(user_id: str) -> List[Dict]:
    """
    Get insights about spending by category
    
    Args:
        user_id: User identifier
        
    Returns:
        List of category insights
    """
    insights = []
    
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Compare current month vs last month by category
            cursor.execute("""
                SELECT 
                    category,
                    SUM(CASE WHEN date >= date('now', 'start of month') THEN amount ELSE 0 END) as current_month,
                    SUM(CASE WHEN date >= date('now', 'start of month', '-1 month') 
                             AND date < date('now', 'start of month') THEN amount ELSE 0 END) as last_month
                FROM expenses
                WHERE user_id = ?
                AND date >= date('now', 'start of month', '-1 month')
                GROUP BY category
            """, (user_id,))
            
            for row in cursor.fetchall():
                category = row['category']
                current = row['current_month']
                last = row['last_month']
                
                if last > 0:
                    change_pct = ((current - last) / last) * 100
                    
                    if abs(change_pct) > 20:
                        insights.append({
                            "category": category,
                            "current_month": current,
                            "last_month": last,
                            "change_percent": change_pct,
                            "insight": f"{'Increased' if change_pct > 0 else 'Decreased'} by {abs(change_pct):.1f}%"
                        })
            
    except Exception as e:
        logger.error(f"Error getting category insights: {e}")
    
    return insights


def predict_monthly_expenses(user_id: str) -> Dict:
    """
    Predict end-of-month expenses based on current spending
    
    Args:
        user_id: User identifier
        
    Returns:
        Dictionary with prediction
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Get current month spending
            cursor.execute("""
                SELECT SUM(amount) as current_total
                FROM expenses
                WHERE user_id = ? AND date >= date('now', 'start of month')
            """, (user_id,))
            
            current_total = cursor.fetchone()['current_total'] or 0
            
            # Calculate days elapsed and remaining
            now = datetime.now()
            days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day if now.month < 12 else 31
            days_elapsed = now.day
            days_remaining = days_in_month - days_elapsed
            
            # Simple linear projection
            if days_elapsed > 0:
                daily_avg = current_total / days_elapsed
                predicted_total = current_total + (daily_avg * days_remaining)
            else:
                predicted_total = 0
            
            return {
                "current_spending": current_total,
                "days_elapsed": days_elapsed,
                "days_remaining": days_remaining,
                "predicted_total": predicted_total,
                "daily_average": daily_avg if days_elapsed > 0 else 0
            }
    except Exception as e:
        logger.error(f"Error predicting expenses: {e}")
        return {}


def get_savings_analysis(user_id: str) -> Dict:
    """
    Analyze savings patterns
    
    Args:
        user_id: User identifier
        
    Returns:
        Dictionary with savings analysis
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Get last 6 months of income and expenses
            cursor.execute("""
                SELECT 
                    strftime('%Y-%m', date) as month,
                    SUM(amount) as total_expenses
                FROM expenses
                WHERE user_id = ? AND date >= date('now', '-6 months')
                GROUP BY month
                ORDER BY month
            """, (user_id,))
            
            monthly_expenses = {row['month']: row['total_expenses'] for row in cursor.fetchall()}
            
            cursor.execute("""
                SELECT month, amount as income
                FROM monthly_income
                WHERE user_id = ? AND month >= date('now', '-6 months')
                ORDER BY month
            """, (user_id,))
            
            monthly_income = {row['month']: row['income'] for row in cursor.fetchall()}
            
            # Calculate savings for each month
            savings_history = []
            for month in sorted(set(list(monthly_expenses.keys()) + list(monthly_income.keys()))):
                income = monthly_income.get(month, 0)
                expenses = monthly_expenses.get(month, 0)
                savings = income - expenses
                savings_rate = (savings / income * 100) if income > 0 else 0
                
                savings_history.append({
                    "month": month,
                    "income": income,
                    "expenses": expenses,
                    "savings": savings,
                    "savings_rate": savings_rate
                })
            
            # Calculate averages
            avg_savings_rate = sum(s['savings_rate'] for s in savings_history) / len(savings_history) if savings_history else 0
            
            return {
                "savings_history": savings_history,
                "average_savings_rate": avg_savings_rate,
                "months_analyzed": len(savings_history)
            }
    except Exception as e:
        logger.error(f"Error analyzing savings: {e}")
        return {}


def get_goal_progress_analysis(user_id: str) -> List[Dict]:
    """
    Analyze progress towards financial goals
    
    Args:
        user_id: User identifier
        
    Returns:
        List of goal progress analyses
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, target_amount, current_amount, deadline, created_at
                FROM goals
                WHERE user_id = ? AND status = 'active'
            """, (user_id,))
            
            goals = []
            for row in cursor.fetchall():
                goal = dict(row)
                
                # Calculate progress
                progress_pct = (goal['current_amount'] / goal['target_amount'] * 100) if goal['target_amount'] > 0 else 0
                remaining = goal['target_amount'] - goal['current_amount']
                
                # Calculate time metrics
                created = datetime.fromisoformat(goal['created_at'])
                deadline = datetime.fromisoformat(goal['deadline'])
                now = datetime.now()
                
                total_days = (deadline - created).days
                days_elapsed = (now - created).days
                days_remaining = (deadline - now).days
                
                # Calculate required monthly savings
                months_remaining = max(days_remaining / 30, 1)
                required_monthly = remaining / months_remaining if months_remaining > 0 else remaining
                
                goals.append({
                    **goal,
                    "progress_percent": progress_pct,
                    "remaining_amount": remaining,
                    "days_remaining": days_remaining,
                    "required_monthly_savings": required_monthly,
                    "on_track": progress_pct >= (days_elapsed / total_days * 100) if total_days > 0 else True
                })
            
            return goals
    except Exception as e:
        logger.error(f"Error analyzing goal progress: {e}")
        return []
