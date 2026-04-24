"""
AUREXIS AI — Recommendations Engine
Generates personalized financial recommendations from real user data.
"""

from typing import Dict, Any, List
from analytics_legacy import extract_transactions, extract_net_worth, extract_credit_score


def generate_recommendations(financial_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate personalized recommendations based on actual financial data."""
    income, expense, transactions = extract_transactions(financial_data)
    net_worth = extract_net_worth(financial_data)
    credit_score = extract_credit_score(financial_data)

    savings = income - expense
    savings_rate = round(savings / income * 100, 1) if income > 0 else 0
    dti = round(expense / income * 100, 1) if income > 0 else 0
    emergency_months = round(net_worth * 0.2 / expense, 1) if expense > 0 else 0

    recs = []

    # Emergency fund
    if emergency_months < 3:
        recs.append({
            "text": "Build emergency fund urgently — less than 3 months covered",
            "impact": f"Target ₹{int(expense * 6 / 100000):.0f}L buffer",
            "type": "safety",
            "priority": 1,
        })
    elif emergency_months < 6:
        recs.append({
            "text": "Increase emergency fund contributions to reach 6-month target",
            "impact": f"{6 - emergency_months:.1f} months remaining",
            "type": "safety",
            "priority": 2,
        })

    # Savings rate
    if savings_rate < 10:
        recs.append({
            "text": "Savings rate is critically low — review and cut non-essential expenses",
            "impact": f"Currently saving {savings_rate}%",
            "type": "savings",
            "priority": 1,
        })
    elif savings_rate < 20:
        recs.append({
            "text": f"Increase savings rate from {savings_rate}% to at least 20%",
            "impact": f"Save ₹{int((income * 0.20 - savings) / 1000):.0f}K more/mo",
            "type": "savings",
            "priority": 2,
        })
    elif savings_rate > 30:
        recs.append({
            "text": "Excellent savings rate — consider increasing SIP investments",
            "impact": "Maximize wealth growth",
            "type": "invest",
            "priority": 4,
        })

    # Debt / DTI
    if dti > 50:
        recs.append({
            "text": "Expense-to-income ratio is very high — avoid new loans",
            "impact": f"DTI at {dti:.0f}% — target below 40%",
            "type": "debt",
            "priority": 1,
        })
    elif dti > 35:
        recs.append({
            "text": "Reduce monthly expenses to improve debt-to-income ratio",
            "impact": f"DTI {dti:.0f}% → target 35%",
            "type": "debt",
            "priority": 2,
        })

    # Credit score
    if credit_score < 650:
        recs.append({
            "text": "Credit score needs urgent attention — pay dues on time",
            "impact": f"Score {credit_score} → target 750+",
            "type": "credit",
            "priority": 1,
        })
    elif credit_score < 750:
        recs.append({
            "text": "Improve credit score by reducing credit card utilization below 30%",
            "impact": f"+{750 - credit_score} points needed",
            "type": "credit",
            "priority": 3,
        })

    # Investment
    investment_value = int(net_worth * 0.6)
    if income > 0 and investment_value < income * 12:
        recs.append({
            "text": "Investment corpus is below 1 year of income — increase SIP",
            "impact": "Start ₹5,000/mo SIP",
            "type": "invest",
            "priority": 3,
        })

    # Tax planning
    if income > 50000:
        recs.append({
            "text": "Maximize 80C deductions with ELSS, EPF, and PPF contributions",
            "impact": "Save up to ₹46,800 in tax",
            "type": "planning",
            "priority": 4,
        })

    # General
    recs.append({
        "text": "Review and rebalance investment portfolio quarterly",
        "impact": "Optimise risk-return",
        "type": "invest",
        "priority": 5,
    })

    # Sort by priority and return top 7
    recs.sort(key=lambda x: x["priority"])
    return recs[:7]
