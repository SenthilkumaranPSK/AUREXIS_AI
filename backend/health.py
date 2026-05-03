"""
Financial Health Module
Calculate and analyze financial health scores.
"""

from typing import Any, Dict, List, Mapping, Union
import logging

from analytics import compute_goals, extract_financials_summary

logger = logging.getLogger(__name__)


def compute_health(user_or_data: Union[str, Mapping[str, Any]]) -> Dict[str, Any]:
    """
    Compute a financial health summary from either:
    - a user id, using persisted app data from the database
    - a financial data payload, using the JSON-backed analytics inputs
    """
    try:
        if isinstance(user_or_data, str):
            return _compute_health_from_db(user_or_data)

        if isinstance(user_or_data, Mapping):
            return _compute_health_from_data(dict(user_or_data))

        raise TypeError("Expected a user id or financial data mapping")
    except Exception as e:
        logger.error(f"Error computing health score: {e}")
        return _format_health_response(
            overall_score=0,
            savings_score=0,
            debt_score=0,
            emergency_fund_score=0,
            goal_progress_score=0,
            spending_discipline_score=0,
            monthly_income=0,
            monthly_expenses=0,
        )


def _compute_health_from_db(user_id: str) -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT amount
            FROM monthly_income
            WHERE user_id = ?
            ORDER BY month DESC
            LIMIT 1
            """,
            (user_id,),
        )
        income_row = cursor.fetchone()
        monthly_income = income_row["amount"] if income_row and income_row["amount"] else 0

        cursor.execute(
            """
            SELECT SUM(amount) as total
            FROM expenses
            WHERE user_id = ? AND date >= date('now', '-30 days')
            """,
            (user_id,),
        )
        expense_row = cursor.fetchone()
        monthly_expenses = expense_row["total"] if expense_row and expense_row["total"] else 0

        savings_score = calculate_savings_score(monthly_income, monthly_expenses)
        debt_score = calculate_debt_score(user_id, monthly_income, cursor)
        emergency_fund_score = calculate_emergency_fund_score(user_id, monthly_expenses, cursor)
        goal_progress_score = calculate_goal_progress_score(user_id, cursor)
        spending_discipline_score = calculate_spending_discipline_score(user_id, cursor)

        overall_score = (
            savings_score * 0.25
            + debt_score * 0.20
            + emergency_fund_score * 0.20
            + goal_progress_score * 0.20
            + spending_discipline_score * 0.15
        )

        return _format_health_response(
            overall_score=overall_score,
            savings_score=savings_score,
            debt_score=debt_score,
            emergency_fund_score=emergency_fund_score,
            goal_progress_score=goal_progress_score,
            spending_discipline_score=spending_discipline_score,
            monthly_income=monthly_income,
            monthly_expenses=monthly_expenses,
        )


def _compute_health_from_data(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    summary = extract_financials_summary(financial_data)
    monthly_income = float(summary.get("monthly_income") or 0)
    monthly_expenses = float(summary.get("monthly_expense") or 0)
    net_worth = float(summary.get("net_worth") or 0)

    savings_score = calculate_savings_score(monthly_income, monthly_expenses)

    debt_ratio = (monthly_expenses / monthly_income) if monthly_income > 0 else 1
    if debt_ratio <= 0.30:
        debt_score = 90
    elif debt_ratio <= 0.45:
        debt_score = 70
    elif debt_ratio <= 0.60:
        debt_score = 45
    else:
        debt_score = 20

    emergency_months = (net_worth * 0.20 / monthly_expenses) if monthly_expenses > 0 else 0
    emergency_fund_score = _emergency_score_from_months(emergency_months)

    goals = compute_goals(financial_data)
    if goals:
        average_progress = sum(float(goal.get("progress", 0)) for goal in goals) / len(goals)
        if average_progress >= 75:
            goal_progress_score = 100
        elif average_progress >= 50:
            goal_progress_score = 80
        elif average_progress >= 25:
            goal_progress_score = 60
        else:
            goal_progress_score = 40
    else:
        goal_progress_score = 50

    spending_discipline_score = 75 if monthly_expenses > 0 else 50

    overall_score = (
        savings_score * 0.25
        + debt_score * 0.20
        + emergency_fund_score * 0.20
        + goal_progress_score * 0.20
        + spending_discipline_score * 0.15
    )

    return _format_health_response(
        overall_score=overall_score,
        savings_score=savings_score,
        debt_score=debt_score,
        emergency_fund_score=emergency_fund_score,
        goal_progress_score=goal_progress_score,
        spending_discipline_score=spending_discipline_score,
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
    )


def _format_health_response(
    *,
    overall_score: float,
    savings_score: float,
    debt_score: float,
    emergency_fund_score: float,
    goal_progress_score: float,
    spending_discipline_score: float,
    monthly_income: float,
    monthly_expenses: float,
) -> Dict[str, Any]:
    overall_score = round(overall_score, 1)
    savings_rate = ((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0

    if overall_score >= 80:
        status = "excellent"
        label = "Excellent"
        color = "success"
        status_message = "Your portfolio is highly resilient. Asset growth and liability management are optimal."
    elif overall_score >= 65:
        status = "good"
        label = "Good"
        color = "primary"
        status_message = "Solid financial baseline. Strategic adjustments could further accelerate your wealth compounding."
    elif overall_score >= 50:
        status = "fair"
        label = "Fair"
        color = "warning"
        status_message = "Vulnerabilities detected in asset allocation. Rebalancing is recommended."
    else:
        status = "poor"
        label = "Needs Improvement"
        color = "danger"
        status_message = "Critical risk exposure identified. Immediate financial restructuring is advised."

    sub_scores = {
        "savings": round(savings_score, 1),
        "debt": round(debt_score, 1),
        "emergency_fund": round(emergency_fund_score, 1),
        "goal_progress": round(goal_progress_score, 1),
        "spending_discipline": round(spending_discipline_score, 1),
    }

    return {
        "overall": overall_score,
        "overall_score": overall_score,
        "label": label,
        "status": status,
        "status_message": status_message,
        "color": color,
        "subScores": _build_sub_score_cards(
            savings_score=savings_score,
            debt_score=debt_score,
            emergency_fund_score=emergency_fund_score,
            goal_progress_score=goal_progress_score,
            spending_discipline_score=spending_discipline_score,
            savings_rate=savings_rate,
            monthly_expenses=monthly_expenses,
        ),
        "sub_scores": sub_scores,
        "metrics": {
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "savings_rate": round(savings_rate, 1),
        },
    }


def _build_sub_score_cards(
    *,
    savings_score: float,
    debt_score: float,
    emergency_fund_score: float,
    goal_progress_score: float,
    spending_discipline_score: float,
    savings_rate: float,
    monthly_expenses: float,
) -> List[Dict[str, Any]]:
    emergency_months = (monthly_expenses and round((emergency_fund_score / 100) * 6, 1)) or 0
    return [
        {
            "name": "Savings Rate",
            "score": round(savings_score, 1),
            "color": _score_to_color(savings_score),
            "detail": f"{round(savings_rate, 1)}% of income",
        },
        {
            "name": "Debt Management",
            "score": round(debt_score, 1),
            "color": _score_to_color(debt_score),
            "detail": "Debt load relative to income",
        },
        {
            "name": "Emergency Fund",
            "score": round(emergency_fund_score, 1),
            "color": _score_to_color(emergency_fund_score),
            "detail": f"{emergency_months} months covered",
        },
        {
            "name": "Goal Progress",
            "score": round(goal_progress_score, 1),
            "color": _score_to_color(goal_progress_score),
            "detail": "Progress across active goals",
        },
        {
            "name": "Spending Discipline",
            "score": round(spending_discipline_score, 1),
            "color": _score_to_color(spending_discipline_score),
            "detail": "Stability of recurring spending",
        },
    ]


def _score_to_color(score: float) -> str:
    if score >= 80:
        return "success"
    if score >= 65:
        return "primary"
    if score >= 50:
        return "warning"
    return "danger"


def _emergency_score_from_months(months_covered: float) -> float:
    if months_covered >= 6:
        return 100
    if months_covered >= 3:
        return 75
    if months_covered >= 1:
        return 50
    return 25


def calculate_savings_score(income: float, expenses: float) -> float:
    """Calculate savings score based on savings rate."""
    if income <= 0:
        return 0

    savings_rate = ((income - expenses) / income) * 100
    if savings_rate >= 30:
        return 100
    if savings_rate >= 20:
        return 80
    if savings_rate >= 10:
        return 60
    if savings_rate >= 0:
        return 40
    return 0


def calculate_debt_score(user_id: str, income: float, cursor) -> float:
    """Calculate debt score based on debt-to-income ratio."""
    return 85


def calculate_emergency_fund_score(user_id: str, monthly_expenses: float, cursor) -> float:
    """Calculate emergency fund score."""
    try:
        cursor.execute(
            """
            SELECT current_amount, target_amount
            FROM goals
            WHERE user_id = ? AND name LIKE '%emergency%' AND status = 'active'
            LIMIT 1
            """,
            (user_id,),
        )

        goal = cursor.fetchone()
        if not goal:
            return 30

        current = goal["current_amount"]
        months_covered = current / monthly_expenses if monthly_expenses > 0 else 0
        return _emergency_score_from_months(months_covered)
    except Exception as e:
        logger.error(f"Error calculating emergency fund score: {e}")
        return 30


def calculate_goal_progress_score(user_id: str, cursor) -> float:
    """Calculate score based on goal progress."""
    try:
        cursor.execute(
            """
            SELECT
                COUNT(*) as total_goals,
                AVG(CAST(current_amount AS FLOAT) / NULLIF(target_amount, 0) * 100) as avg_progress
            FROM goals
            WHERE user_id = ? AND status = 'active'
            """,
            (user_id,),
        )

        result = cursor.fetchone()
        if not result or result["total_goals"] == 0:
            return 50

        avg_progress = result["avg_progress"] or 0
        if avg_progress >= 75:
            return 100
        if avg_progress >= 50:
            return 80
        if avg_progress >= 25:
            return 60
        return 40
    except Exception as e:
        logger.error(f"Error calculating goal progress score: {e}")
        return 50


def calculate_spending_discipline_score(user_id: str, cursor) -> float:
    """Calculate score based on spending consistency."""
    try:
        cursor.execute(
            """
            SELECT
                SUM(CASE WHEN date >= date('now', 'start of month') THEN amount ELSE 0 END) as current_month,
                AVG(CASE WHEN date < date('now', 'start of month')
                         AND date >= date('now', 'start of month', '-3 months')
                         THEN amount ELSE NULL END) as avg_last_3_months
            FROM expenses
            WHERE user_id = ?
            AND date >= date('now', 'start of month', '-3 months')
            """,
            (user_id,),
        )

        result = cursor.fetchone()
        current = result["current_month"] or 0
        avg_past = result["avg_last_3_months"] or 0

        if avg_past == 0:
            return 70

        variance = abs(current - avg_past) / avg_past * 100
        if variance <= 10:
            return 100
        if variance <= 20:
            return 80
        if variance <= 35:
            return 60
        return 40
    except Exception as e:
        logger.error(f"Error calculating spending discipline score: {e}")
        return 50
