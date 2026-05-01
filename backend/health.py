"""
Financial Health Module
Calculate and analyze financial health scores
"""

from typing import Dict
import logging
from database.db_utils import get_db

logger = logging.getLogger(__name__)


def compute_health(user_id: str) -> Dict:
    """
    Compute comprehensive financial health score
    
    Args:
        user_id: User identifier
        
    Returns:
        Dictionary with health score and sub-scores
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Get income
            cursor.execute("""
                SELECT amount
                FROM monthly_income
                WHERE user_id = ?
                ORDER BY month DESC
                LIMIT 1
            """, (user_id,))
            income_row = cursor.fetchone()
            monthly_income = income_row['amount'] if income_row else 0
            
            # Get expenses (last 30 days)
            cursor.execute("""
                SELECT SUM(amount) as total
                FROM expenses
                WHERE user_id = ? AND date >= date('now', '-30 days')
            """, (user_id,))
            expense_row = cursor.fetchone()
            monthly_expenses = expense_row['total'] if expense_row else 0
            
            # Calculate sub-scores
            savings_score = calculate_savings_score(monthly_income, monthly_expenses)
            debt_score = calculate_debt_score(user_id, monthly_income, cursor)
            emergency_fund_score = calculate_emergency_fund_score(user_id, monthly_expenses, cursor)
            goal_progress_score = calculate_goal_progress_score(user_id, cursor)
            spending_discipline_score = calculate_spending_discipline_score(user_id, cursor)
            
            # Calculate overall health score (weighted average)
            overall_score = (
                savings_score * 0.25 +
                debt_score * 0.20 +
                emergency_fund_score * 0.20 +
                goal_progress_score * 0.20 +
                spending_discipline_score * 0.15
            )
            
            # Determine health status
            if overall_score >= 80:
                status = "excellent"
                status_message = "Your financial health is excellent!"
            elif overall_score >= 60:
                status = "good"
                status_message = "Your financial health is good, with room for improvement."
            elif overall_score >= 40:
                status = "fair"
                status_message = "Your financial health needs attention."
            else:
                status = "poor"
                status_message = "Your financial health requires immediate action."
            
            return {
                "overall_score": round(overall_score, 1),
                "status": status,
                "status_message": status_message,
                "sub_scores": {
                    "savings": round(savings_score, 1),
                    "debt": round(debt_score, 1),
                    "emergency_fund": round(emergency_fund_score, 1),
                    "goal_progress": round(goal_progress_score, 1),
                    "spending_discipline": round(spending_discipline_score, 1)
                },
                "metrics": {
                    "monthly_income": monthly_income,
                    "monthly_expenses": monthly_expenses,
                    "savings_rate": ((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0
                }
            }
    except Exception as e:
        logger.error(f"Error computing health score: {e}")
        return {
            "overall_score": 0,
            "status": "unknown",
            "status_message": "Unable to calculate health score",
            "sub_scores": {},
            "metrics": {}
        }


def calculate_savings_score(income: float, expenses: float) -> float:
    """Calculate savings score based on savings rate"""
    if income <= 0:
        return 0
    
    savings_rate = ((income - expenses) / income) * 100
    
    if savings_rate >= 30:
        return 100
    elif savings_rate >= 20:
        return 80
    elif savings_rate >= 10:
        return 60
    elif savings_rate >= 0:
        return 40
    else:
        return 0  # Negative savings


def calculate_debt_score(user_id: str, income: float, cursor) -> float:
    """Calculate debt score based on debt-to-income ratio"""
    # For now, assume no debt tracking - return high score
    # TODO: Implement debt tracking
    return 85


def calculate_emergency_fund_score(user_id: str, monthly_expenses: float, cursor) -> float:
    """Calculate emergency fund score"""
    try:
        # Check for emergency fund goal
        cursor.execute("""
            SELECT current_amount, target_amount
            FROM goals
            WHERE user_id = ? AND name LIKE '%emergency%' AND status = 'active'
            LIMIT 1
        """, (user_id,))
        
        goal = cursor.fetchone()
        if not goal:
            return 30  # No emergency fund
        
        current = goal['current_amount']
        target = goal['target_amount']
        
        # Calculate months of expenses covered
        months_covered = current / monthly_expenses if monthly_expenses > 0 else 0
        
        if months_covered >= 6:
            return 100
        elif months_covered >= 3:
            return 75
        elif months_covered >= 1:
            return 50
        else:
            return 25
    except Exception as e:
        logger.error(f"Error calculating emergency fund score: {e}")
        return 30


def calculate_goal_progress_score(user_id: str, cursor) -> float:
    """Calculate score based on goal progress"""
    try:
        cursor.execute("""
            SELECT 
                COUNT(*) as total_goals,
                AVG(CAST(current_amount AS FLOAT) / NULLIF(target_amount, 0) * 100) as avg_progress
            FROM goals
            WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        
        result = cursor.fetchone()
        if not result or result['total_goals'] == 0:
            return 50  # Neutral score if no goals
        
        avg_progress = result['avg_progress'] or 0
        
        # Score based on average progress
        if avg_progress >= 75:
            return 100
        elif avg_progress >= 50:
            return 80
        elif avg_progress >= 25:
            return 60
        else:
            return 40
    except Exception as e:
        logger.error(f"Error calculating goal progress score: {e}")
        return 50


def calculate_spending_discipline_score(user_id: str, cursor) -> float:
    """Calculate score based on spending consistency"""
    try:
        # Compare current month vs average of last 3 months
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN date >= date('now', 'start of month') THEN amount ELSE 0 END) as current_month,
                AVG(CASE WHEN date < date('now', 'start of month') 
                         AND date >= date('now', 'start of month', '-3 months') 
                         THEN amount ELSE NULL END) as avg_last_3_months
            FROM expenses
            WHERE user_id = ?
            AND date >= date('now', 'start of month', '-3 months')
        """, (user_id,))
        
        result = cursor.fetchone()
        current = result['current_month'] or 0
        avg_past = result['avg_last_3_months'] or 0
        
        if avg_past == 0:
            return 70  # Not enough data
        
        # Calculate variance
        variance = abs(current - avg_past) / avg_past * 100
        
        if variance <= 10:
            return 100  # Very consistent
        elif variance <= 20:
            return 80
        elif variance <= 30:
            return 60
        else:
            return 40  # High variance
    except Exception as e:
        logger.error(f"Error calculating spending discipline score: {e}")
        return 70
