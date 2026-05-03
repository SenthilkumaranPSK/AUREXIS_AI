"""
Analytics Module
Financial analytics and insights generation
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def extract_transactions(financial_data: Dict) -> Tuple[float, float, List[Dict]]:
    """
    Extract income, expense, and transaction list from financial data
    
    Args:
        financial_data: User's complete financial data from JSON files
        
    Returns:
        Tuple of (monthly_income, monthly_expense, transactions_list)
        where transactions_list is a list of dicts with 'date', 'type', 'amount', 'narration'
    """
    monthly_income = 0
    monthly_expense = 0
    transactions_list = []
    
    if not financial_data:
        return (0, 0, [])
    
    # Extract from bank transactions
    bank_data = financial_data.get("fetch_bank_transactions", {})
    bank_transactions = bank_data.get("bankTransactions", [])
    
    if bank_transactions:
        # Process transactions from all banks
        total_credits = 0
        total_debits = 0
        
        for bank_entry in bank_transactions:
            txns = bank_entry.get("txns", [])
            
            for txn in txns:
                # Transaction format: [amount, narration, date, type, mode, balance]
                # type: 1=CREDIT, 2=DEBIT, 4=INTEREST, 6=INSTALLMENT
                if len(txn) >= 4:
                    amount = float(txn[0])
                    narration = txn[1] if len(txn) > 1 else ""
                    date_str = txn[2] if len(txn) > 2 else ""
                    txn_type = int(txn[3])
                    
                    # Convert type code to string
                    type_str = "CREDIT" if txn_type == 1 else "DEBIT" if txn_type in [2, 6] else "INTEREST"
                    
                    # Add to transactions list
                    transactions_list.append({
                        "date": date_str,
                        "type": type_str,
                        "amount": amount,
                        "narration": narration
                    })
                    
                    if txn_type == 1:  # CREDIT (income)
                        total_credits += amount
                    elif txn_type in [2, 6]:  # DEBIT or INSTALLMENT (expense)
                        total_debits += amount
        
        # Calculate monthly averages (assuming data covers multiple months)
        # Count unique months in transactions
        unique_months = set()
        for bank_entry in bank_transactions:
            for txn in bank_entry.get("txns", []):
                if len(txn) >= 3:
                    try:
                        date_str = txn[2]
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        unique_months.add(f"{date_obj.year}-{date_obj.month:02d}")
                    except:
                        pass
        
        num_months = max(len(unique_months), 1)
        monthly_income = round(total_credits / num_months)
        monthly_expense = round(total_debits / num_months)
    
    return (monthly_income, monthly_expense, transactions_list)


def extract_net_worth(financial_data: Dict) -> float:
    """
    Extract total net worth from financial data
    
    Args:
        financial_data: User's complete financial data from JSON files
        
    Returns:
        Total net worth value
    """
    if not financial_data:
        return 0
    
    net_worth_data = financial_data.get("fetch_net_worth", {})
    net_worth_response = net_worth_data.get("netWorthResponse", {})
    total_net_worth = net_worth_response.get("totalNetWorthValue", {})
    
    # Extract units (amount) from net worth
    units_str = total_net_worth.get("units", "0")
    try:
        return float(units_str)
    except (ValueError, TypeError):
        return 0


def extract_credit_score(financial_data: Dict) -> int:
    """
    Extract credit score from financial data
    
    Args:
        financial_data: User's complete financial data from JSON files
        
    Returns:
        Credit score (defaults to 700 if not found)
    """
    if not financial_data:
        return 700
    
    credit_data = financial_data.get("fetch_credit_report", {})
    
    # Try to extract credit score from various possible locations
    if isinstance(credit_data, dict):
        # Check common credit score fields
        score = credit_data.get("credit_score") or credit_data.get("score") or credit_data.get("creditScore")
        if score:
            try:
                return int(score)
            except (ValueError, TypeError):
                pass
        
        # Check nested structures
        report = credit_data.get("creditReport", {})
        if isinstance(report, dict):
            score = report.get("score") or report.get("credit_score")
            if score:
                try:
                    return int(score)
                except (ValueError, TypeError):
                    pass
    
    # Default credit score
    return 700


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

def extract_financials_summary(financial_data: Dict) -> Dict:
    """Extract and calculate core financial metrics from user data"""
    monthly_income = 0
    monthly_expense = 0
    monthly_savings = 0
    savings_rate = 0
    net_worth = 0
    credit_score = 700

    if not financial_data:
        return {
            "monthly_income": monthly_income,
            "monthly_expense": monthly_expense,
            "monthly_savings": monthly_savings,
            "savings_rate": savings_rate,
            "net_worth": net_worth,
            "credit_score": credit_score
        }

    net_worth_data = financial_data.get("fetch_net_worth", {}).get("data", {})
    if isinstance(net_worth_data, dict):
        net_worth = net_worth_data.get("total_net_worth", 0)

    bank_data = financial_data.get("fetch_bank_transactions", {}).get("data", {})
    if isinstance(bank_data, dict):
        monthly_income = bank_data.get("monthly_income", 50000)
        monthly_expense = bank_data.get("monthly_expense", 30000)

    monthly_savings = max(0, monthly_income - monthly_expense)
    if monthly_income > 0:
        savings_rate = round((monthly_savings / monthly_income) * 100, 2)

    return {
        "monthly_income": monthly_income,
        "monthly_expense": monthly_expense,
        "monthly_savings": monthly_savings,
        "savings_rate": savings_rate,
        "net_worth": net_worth,
        "credit_score": credit_score
    }
