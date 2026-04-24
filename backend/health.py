"""
AUREXIS AI — Health Score Engine
Computes detailed financial health breakdown with sub-scores.
"""

from typing import Dict, Any
from analytics import extract_transactions, extract_net_worth, extract_credit_score


def compute_health(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """Compute detailed financial health score with sub-scores and color metadata."""
    income, expense, _ = extract_transactions(financial_data)
    net_worth = extract_net_worth(financial_data)
    credit_score = extract_credit_score(financial_data)

    savings = income - expense
    savings_rate = round(savings / income * 100, 1) if income > 0 else 0
    dti = round(expense / income * 100, 1) if income > 0 else 0
    emergency_months = round(net_worth * 0.2 / expense, 1) if expense > 0 else 0

    # Sub-scores (0-100 each)
    savings_score   = min(100, max(0, int(savings_rate * 2.5)))          # 40% savings = 100
    credit_sub      = min(100, max(0, int((credit_score - 300) / 5.5)))  # 850 = 100
    emergency_sub   = min(100, max(0, int(emergency_months / 6 * 100)))  # 6 months = 100
    expense_sub     = min(100, max(0, int((1 - dti / 100) * 100)))       # 0% DTI = 100

    # Weighted overall score
    overall = int(
        savings_sub   := savings_score * 0.35 +
        credit_sub    * 0.25 +
        emergency_sub * 0.25 +
        expense_sub   * 0.15
    )
    overall = min(100, max(0, overall))

    def score_label(s: int):
        if s >= 80: return "Excellent"
        if s >= 60: return "Good"
        if s >= 40: return "Fair"
        return "Poor"

    def score_color(s: int):
        if s >= 80: return "success"
        if s >= 60: return "primary"
        if s >= 40: return "warning"
        return "danger"

    return {
        "overall": overall,
        "label": score_label(overall),
        "color": score_color(overall),
        "subScores": [
            {
                "name": "Savings",
                "score": savings_score,
                "label": score_label(savings_score),
                "color": score_color(savings_score),
                "detail": f"{savings_rate}% savings rate",
            },
            {
                "name": "Credit",
                "score": credit_sub,
                "label": score_label(credit_sub),
                "color": score_color(credit_sub),
                "detail": f"Score {credit_score}",
            },
            {
                "name": "Emergency",
                "score": emergency_sub,
                "label": score_label(emergency_sub),
                "color": score_color(emergency_sub),
                "detail": f"{emergency_months} months covered",
            },
            {
                "name": "Expenses",
                "score": expense_sub,
                "label": score_label(expense_sub),
                "color": score_color(expense_sub),
                "detail": f"{dti:.0f}% of income",
            },
        ],
        "stats": {
            "savingsRate": savings_rate,
            "creditScore": credit_score,
            "dti": round(dti / 100, 2),
            "emergencyMonths": emergency_months,
        },
    }
