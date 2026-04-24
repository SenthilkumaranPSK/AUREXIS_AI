"""
AUREXIS AI — Alerts Engine
Generates real-time financial alerts from actual user data patterns.
"""

from typing import Dict, Any, List
from datetime import datetime
from analytics_legacy import extract_transactions, extract_net_worth, extract_credit_score


def generate_alerts(financial_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate alerts based on actual financial data analysis."""
    income, expense, transactions = extract_transactions(financial_data)
    net_worth = extract_net_worth(financial_data)
    credit_score = extract_credit_score(financial_data)

    savings = income - expense
    savings_rate = round(savings / income * 100, 1) if income > 0 else 0
    dti = round(expense / income * 100, 1) if income > 0 else 0
    emergency_months = round(net_worth * 0.2 / expense, 1) if expense > 0 else 0

    today = datetime.now().strftime("%Y-%m-%d")
    alerts = []
    aid = 1

    # Critical alerts
    if savings < 0:
        alerts.append({
            "id": f"a{aid}", "type": "danger",
            "title": "Negative Cash Flow",
            "message": f"Expenses exceed income by ₹{abs(int(savings)):,}. Immediate action needed.",
            "timestamp": today,
        })
        aid += 1

    if emergency_months < 3:
        alerts.append({
            "id": f"a{aid}", "type": "danger",
            "title": "Critical: Low Emergency Fund",
            "message": f"Only {emergency_months} months of expenses covered. Target is 6 months.",
            "timestamp": today,
        })
        aid += 1

    if credit_score < 650:
        alerts.append({
            "id": f"a{aid}", "type": "danger",
            "title": "Low Credit Score",
            "message": f"Credit score {credit_score} is below safe threshold. Pay dues on time.",
            "timestamp": today,
        })
        aid += 1

    # Warning alerts
    if dti > 50:
        alerts.append({
            "id": f"a{aid}", "type": "warning",
            "title": "High Expense Ratio",
            "message": f"Expenses are {dti:.0f}% of income. Recommended maximum is 50%.",
            "timestamp": today,
        })
        aid += 1

    if 3 <= emergency_months < 6:
        alerts.append({
            "id": f"a{aid}", "type": "warning",
            "title": "Emergency Fund Below Target",
            "message": f"{emergency_months} months covered. Increase contributions to reach 6 months.",
            "timestamp": today,
        })
        aid += 1

    if 650 <= credit_score < 750:
        alerts.append({
            "id": f"a{aid}", "type": "warning",
            "title": "Credit Score Can Improve",
            "message": f"Score {credit_score}. Reduce credit utilization to improve it.",
            "timestamp": today,
        })
        aid += 1

    # Positive alerts
    if savings_rate > 30:
        alerts.append({
            "id": f"a{aid}", "type": "success",
            "title": "Excellent Savings Rate",
            "message": f"You are saving {savings_rate}% of income. Keep it up!",
            "timestamp": today,
        })
        aid += 1

    if credit_score >= 750:
        alerts.append({
            "id": f"a{aid}", "type": "success",
            "title": "Strong Credit Score",
            "message": f"Credit score {credit_score} qualifies you for the best loan rates.",
            "timestamp": today,
        })
        aid += 1

    if emergency_months >= 6:
        alerts.append({
            "id": f"a{aid}", "type": "success",
            "title": "Emergency Fund Secured",
            "message": f"{emergency_months} months of expenses covered. Well done!",
            "timestamp": today,
        })
        aid += 1

    # Info alerts
    if net_worth > 0:
        alerts.append({
            "id": f"a{aid}", "type": "info",
            "title": "Portfolio Review Due",
            "message": "Quarterly portfolio rebalancing recommended to maintain target allocation.",
            "timestamp": today,
        })
        aid += 1

    return alerts[:6]  # Return top 6 alerts


def generate_emis(financial_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate upcoming EMI reminders."""
    from datetime import datetime, timedelta

    income, expense, _ = extract_transactions(financial_data)

    # Estimate EMI from expense patterns
    estimated_emi = int(expense * 0.25)  # ~25% of expense assumed as EMI

    today = datetime.now()
    emis = []

    if estimated_emi > 10000:
        emis.append({
            "name": "Home Loan",
            "amount": int(estimated_emi * 0.6),
            "dueDate": (today + timedelta(days=5)).strftime("%Y-%m-%d"),
            "type": "Mortgage",
        })
        emis.append({
            "name": "Car Loan",
            "amount": int(estimated_emi * 0.4),
            "dueDate": (today + timedelta(days=12)).strftime("%Y-%m-%d"),
            "type": "Auto",
        })

    return emis
