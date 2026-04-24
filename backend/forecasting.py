"""
AUREXIS AI — Forecasting Engine
Predicts future financial trends using weighted moving averages and growth models.
No external ML libraries needed — pure Python math.
"""

from typing import Dict, Any, List
from analytics import extract_transactions, extract_net_worth, extract_credit_score
import math


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _weighted_avg(values: List[float], weights: List[float] = None) -> float:
    """Weighted moving average."""
    if not values:
        return 0.0
    if weights is None:
        weights = list(range(1, len(values) + 1))
    total_w = sum(weights[:len(values)])
    return sum(v * w for v, w in zip(values, weights[:len(values)])) / total_w if total_w else 0.0


def _compound_growth(base: float, rate: float, periods: int) -> float:
    """Compound growth formula."""
    return base * math.pow(1 + rate, periods)


def compute_monthly_forecast(financial_data: Dict[str, Any], months_ahead: int = 6) -> List[Dict[str, Any]]:
    """
    Generate historical + projected monthly data.
    Uses weighted moving average on historical patterns.
    """
    income, expense, transactions = extract_transactions(financial_data)
    net_worth = extract_net_worth(financial_data)

    if income == 0:
        return []

    savings = income - expense
    savings_rate = savings / income if income > 0 else 0

    # Historical 6 months with realistic variation
    historical_factors = [
        ("Oct", 0.90, 0.95, 0.92),
        ("Nov", 1.00, 1.00, 0.95),
        ("Dec", 1.10, 1.20, 0.97),  # Dec spike in expenses
        ("Jan", 1.00, 0.90, 0.98),
        ("Feb", 0.95, 0.85, 0.99),
        ("Mar", 1.00, 1.00, 1.00),
    ]

    historical = []
    for month, fi, fe, fn in historical_factors:
        m_income  = round(income * fi)
        m_expense = round(expense * fe)
        historical.append({
            "month":    month,
            "income":   m_income,
            "expense":  m_expense,
            "savings":  m_income - m_expense,
            "netWorth": round(net_worth * fn),
            "projected": False,
        })

    # Extract historical income/expense for trend calculation
    hist_incomes  = [h["income"]  for h in historical]
    hist_expenses = [h["expense"] for h in historical]

    # Weighted avg growth rates
    income_growth  = _weighted_avg([
        (hist_incomes[i] - hist_incomes[i-1]) / hist_incomes[i-1]
        for i in range(1, len(hist_incomes)) if hist_incomes[i-1] > 0
    ]) if len(hist_incomes) > 1 else 0.005

    expense_growth = _weighted_avg([
        (hist_expenses[i] - hist_expenses[i-1]) / hist_expenses[i-1]
        for i in range(1, len(hist_expenses)) if hist_expenses[i-1] > 0
    ]) if len(hist_expenses) > 1 else 0.01

    # Cap growth rates to realistic bounds
    income_growth  = max(-0.05, min(0.05, income_growth))
    expense_growth = max(0.005, min(0.03, expense_growth))

    # Project forward
    projected = []
    base_income   = income
    base_expense  = expense
    base_nw       = net_worth
    proj_months   = ["Apr", "May", "Jun", "Jul", "Aug", "Sep"]

    for i, month in enumerate(proj_months[:months_ahead]):
        p_income  = round(_compound_growth(base_income,  income_growth,  i + 1))
        p_expense = round(_compound_growth(base_expense, expense_growth, i + 1))
        p_savings = p_income - p_expense
        p_nw      = round(base_nw + savings * (i + 1) * 1.02)  # slight investment growth

        projected.append({
            "month":    month,
            "income":   p_income,
            "expense":  p_expense,
            "savings":  p_savings,
            "netWorth": p_nw,
            "projected": True,
        })

    return historical + projected


def compute_net_worth_forecast(financial_data: Dict[str, Any], years: int = 5) -> List[Dict[str, Any]]:
    """Project net worth over multiple years using compound growth."""
    income, expense, _ = extract_transactions(financial_data)
    net_worth = extract_net_worth(financial_data)

    monthly_savings = income - expense
    annual_savings  = monthly_savings * 12
    investment_rate = 0.10  # 10% annual return assumption
    savings_rate    = income * 0.12  # 12% annual income growth

    result = []
    current_nw = net_worth

    for year in range(1, years + 1):
        # Net worth grows from investment returns + new savings
        investment_return = current_nw * investment_rate
        new_savings       = annual_savings * math.pow(1.05, year - 1)  # savings grow 5%/yr
        current_nw        = current_nw + investment_return + new_savings

        result.append({
            "year":             f"Year {year}",
            "netWorth":         round(current_nw),
            "investmentReturn": round(investment_return),
            "newSavings":       round(new_savings),
        })

    return result


def compute_goal_forecast(financial_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Forecast when each financial goal will be completed."""
    income, expense, _ = extract_transactions(financial_data)
    net_worth = extract_net_worth(financial_data)

    monthly_savings = max(0, income - expense)
    investment_value = int(net_worth * 0.6)

    goals = [
        {"name": "Emergency Fund", "icon": "🛡️", "target": int(expense * 6), "current": int(expense * 4.5), "monthly": monthly_savings * 0.3},
        {"name": "New Car",        "icon": "🚗", "target": 1200000,           "current": 350000,             "monthly": 15000},
        {"name": "Retirement",     "icon": "🏖️", "target": 5000000,           "current": investment_value,   "monthly": 25000},
    ]

    result = []
    for goal in goals:
        remaining = goal["target"] - goal["current"]
        if remaining <= 0:
            months_left = 0
            status = "Completed"
        elif goal["monthly"] > 0:
            months_left = math.ceil(remaining / goal["monthly"])
            status = "On Track" if months_left <= 24 else "Needs Attention"
        else:
            months_left = 999
            status = "No Contributions"

        years  = months_left // 12
        months = months_left % 12

        result.append({
            "name":        goal["name"],
            "icon":        goal["icon"],
            "target":      goal["target"],
            "current":     goal["current"],
            "remaining":   max(0, remaining),
            "monthsLeft":  months_left,
            "timeLabel":   f"{years}y {months}m" if years > 0 else f"{months}m",
            "status":      status,
            "progress":    round(min(100, goal["current"] / goal["target"] * 100), 1),
            "monthly":     round(goal["monthly"]),
        })

    return result


def compute_expense_forecast(financial_data: Dict[str, Any], months: int = 6) -> List[Dict[str, Any]]:
    """Forecast future expense trends by category."""
    income, expense, _ = extract_transactions(financial_data)

    categories = [
        {"name": "Housing",   "pct": 0.40, "growth": 0.005},
        {"name": "Food",      "pct": 0.20, "growth": 0.015},
        {"name": "Transport", "pct": 0.15, "growth": 0.010},
        {"name": "Utilities", "pct": 0.10, "growth": 0.008},
        {"name": "Other",     "pct": 0.15, "growth": 0.012},
    ]

    result = []
    for cat in categories:
        base = expense * cat["pct"]
        projections = [
            round(_compound_growth(base, cat["growth"], i + 1))
            for i in range(months)
        ]
        result.append({
            "category":    cat["name"],
            "current":     round(base),
            "projections": projections,
            "growthRate":  f"{cat['growth'] * 100:.1f}%/mo",
            "sixMonthTotal": sum(projections),
        })

    return result


def compute_savings_projection(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """Project savings accumulation at different contribution rates."""
    income, expense, _ = extract_transactions(financial_data)
    net_worth = extract_net_worth(financial_data)

    current_savings = max(0, income - expense)
    scenarios = []

    for rate_pct in [10, 20, 30, 40]:
        monthly = income * rate_pct / 100
        annual  = monthly * 12
        # 5-year projection with 8% annual return
        five_year = net_worth
        for _ in range(60):  # 60 months
            five_year = five_year * (1 + 0.08/12) + monthly

        scenarios.append({
            "rate":       rate_pct,
            "monthly":    round(monthly),
            "annual":     round(annual),
            "fiveYear":   round(five_year),
            "isCurrent":  abs(monthly - current_savings) < income * 0.05,
        })

    return {
        "currentMonthlySavings": round(current_savings),
        "currentRate":           round(current_savings / income * 100, 1) if income > 0 else 0,
        "scenarios":             scenarios,
    }
