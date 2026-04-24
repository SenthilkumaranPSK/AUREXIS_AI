"""
AUREXIS AI — Financial Report Generator
Generates a complete structured financial report for a user.
All logic in Python — frontend just renders the JSON.
"""

from typing import Dict, Any
from analytics_legacy import (
    extract_transactions, extract_net_worth, extract_credit_score,
    compute_metrics, compute_risk, compute_expenses, compute_investments, compute_goals
)
from health import compute_health
from recommendations_legacy import generate_recommendations
from alerts import generate_alerts
from forecasting import compute_net_worth_forecast, compute_goal_forecast, compute_savings_projection
from datetime import datetime


def _grade(score: int) -> str:
    if score >= 85: return "A+"
    if score >= 75: return "A"
    if score >= 65: return "B+"
    if score >= 55: return "B"
    if score >= 45: return "C"
    return "D"


def _trend(current: float, previous: float) -> str:
    if previous == 0:
        return "stable"
    change = (current - previous) / previous * 100
    if change > 5:   return "up"
    if change < -5:  return "down"
    return "stable"


def generate_report(user: Dict[str, Any], financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a complete financial report for a user."""
    income, expense, transactions = extract_transactions(financial_data)
    net_worth   = extract_net_worth(financial_data)
    credit_score = extract_credit_score(financial_data)

    savings      = income - expense
    savings_rate = round(savings / income * 100, 1) if income > 0 else 0
    dti          = round(expense / income * 100, 1) if income > 0 else 0

    metrics      = compute_metrics(financial_data)
    health       = compute_health(financial_data)
    risk         = compute_risk(financial_data)
    expenses_bkd = compute_expenses(financial_data)
    investments  = compute_investments(financial_data)
    goals        = compute_goals(financial_data)
    recs         = generate_recommendations(financial_data)
    alerts       = generate_alerts(financial_data)
    nw_forecast  = compute_net_worth_forecast(financial_data, years=3)
    goal_fc      = compute_goal_forecast(financial_data)
    savings_proj = compute_savings_projection(financial_data)

    # Overall grade
    grade = _grade(health["overall"])

    # Key strengths and weaknesses
    strengths = []
    weaknesses = []

    if savings_rate > 30:  strengths.append(f"Strong savings rate of {savings_rate}%")
    if credit_score >= 750: strengths.append(f"Excellent credit score of {credit_score}")
    if metrics["emergencyFundMonths"] >= 6: strengths.append("Emergency fund fully secured")
    if net_worth > income * 12: strengths.append("Net worth exceeds annual income")

    if savings_rate < 10:  weaknesses.append(f"Low savings rate of {savings_rate}%")
    if credit_score < 700: weaknesses.append(f"Credit score {credit_score} needs improvement")
    if dti > 50:           weaknesses.append(f"High expense ratio of {dti:.0f}%")
    if metrics["emergencyFundMonths"] < 3: weaknesses.append("Emergency fund critically low")

    if not strengths:  strengths.append("Consistent financial activity detected")
    if not weaknesses: weaknesses.append("No major financial risks identified")

    return {
        "generatedAt":   datetime.now().isoformat(),
        "userName":      user.get("name", "User"),
        "reportPeriod":  "Last 6 Months",
        "grade":         grade,
        "summary": {
            "netWorth":      net_worth,
            "monthlyIncome": income,
            "monthlyExpense": expense,
            "monthlySavings": savings,
            "savingsRate":   savings_rate,
            "creditScore":   credit_score,
            "healthScore":   health["overall"],
            "healthLabel":   health["label"],
            "riskLevel":     risk["riskLevel"],
            "dti":           dti,
        },
        "strengths":     strengths,
        "weaknesses":    weaknesses,
        "health":        health,
        "risk":          risk,
        "metrics":       metrics,
        "expenseBreakdown": expenses_bkd,
        "investments":   investments,
        "goals":         goals,
        "goalForecast":  goal_fc,
        "netWorthForecast": nw_forecast,
        "savingsProjection": savings_proj,
        "recommendations": recs[:5],
        "alerts":        alerts,
        "topTransactions": sorted(
            [t for t in transactions if t["type"] == "DEBIT"],
            key=lambda x: x["amount"], reverse=True
        )[:5],
    }
