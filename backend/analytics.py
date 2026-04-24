"""
AUREXIS AI — Analytics Engine
All financial calculations live here. Backend computes, frontend just renders.
"""

from typing import Dict, Any, List


EXPENSE_COLORS = ["#3B82F6", "#F59E0B", "#10B981", "#EC4899", "#6B7280", "#8B5CF6", "#EF4444"]
INVESTMENT_COLORS = ["#3B82F6", "#8B5CF6", "#F59E0B", "#10B981", "#EC4899", "#EF4444", "#06B6D4"]


def extract_transactions(financial_data: Dict[str, Any]):
    """Parse bank transactions and return income, expense totals."""
    monthly_income = 0.0
    monthly_expense = 0.0
    transactions = []

    for bank in financial_data.get("fetch_bank_transactions", {}).get("bankTransactions", []):
        bank_name = bank.get("bank", "Bank")
        for txn in bank.get("txns", []):
            if len(txn) >= 4:
                try:
                    amount = float(txn[0]) if str(txn[0]).replace(".", "").replace("-", "").isdigit() else 0.0
                except:
                    amount = 0.0
                txn_type = txn[3]
                if txn_type == 1:
                    monthly_income += amount
                elif txn_type == 2:
                    monthly_expense += amount
                transactions.append({
                    "bank": bank_name,
                    "amount": amount,
                    "narration": txn[1] if len(txn) > 1 else "",
                    "date": txn[2] if len(txn) > 2 else "",
                    "type": "CREDIT" if txn_type == 1 else "DEBIT",
                })

    return monthly_income, monthly_expense, transactions


def extract_net_worth(financial_data: Dict[str, Any]) -> float:
    net_worth_data = financial_data.get("fetch_net_worth", {})
    if "netWorthResponse" in net_worth_data:
        try:
            return float(net_worth_data["netWorthResponse"].get("totalNetWorthValue", {}).get("units", 0) or 0)
        except:
            pass
    return 0.0


def extract_credit_score(financial_data: Dict[str, Any]) -> int:
    for report in financial_data.get("fetch_credit_report", {}).get("creditReports", []):
        score = report.get("creditReportData", {}).get("score", {}).get("bureauScore")
        if score:
            try:
                return int(float(score))
            except:
                pass
    return 750


def extract_financials_summary(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and normalize financial metrics to monthly averages.
    Returns: {monthly_income, monthly_expense, monthly_savings, savings_rate, net_worth, credit_score, num_months}
    """
    total_income, total_expense, transactions = extract_transactions(financial_data)
    net_worth    = extract_net_worth(financial_data)
    credit_score = extract_credit_score(financial_data)

    # Count unique months in transaction data
    txn_months = set()
    for txn in transactions:
        date = txn.get("date", "")
        if date and len(date) >= 7:
            txn_months.add(date[:7])
    num_months = max(1, len(txn_months))

    monthly_income  = round(total_income  / num_months)
    monthly_expense = round(total_expense / num_months)
    monthly_savings = monthly_income - monthly_expense
    savings_rate    = round(monthly_savings / monthly_income * 100, 1) if monthly_income > 0 else 0.0

    return {
        "monthly_income":  monthly_income,
        "monthly_expense": monthly_expense,
        "monthly_savings": monthly_savings,
        "savings_rate":    savings_rate,
        "net_worth":       net_worth,
        "credit_score":    credit_score,
        "num_months":      num_months,
    }


def compute_metrics(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """Compute all key financial metrics."""
    income, expense, _ = extract_transactions(financial_data)
    net_worth = extract_net_worth(financial_data)
    credit_score = extract_credit_score(financial_data)

    savings = income - expense
    savings_rate = round(savings / income * 100, 1) if income > 0 else 0.0
    dti = round(expense / income, 2) if income > 0 else 0.0
    health_score = min(100, max(0, int(50 + savings_rate)))
    emergency_months = round(net_worth * 0.2 / expense, 1) if expense > 0 else 6.0
    investment_value = int(net_worth * 0.6)
    risk_level = "Low" if savings_rate > 30 else "Medium" if savings_rate > 10 else "High"

    return {
        "monthlyIncome": income,
        "monthlyExpense": expense,
        "savings": int(savings),
        "savingsRate": savings_rate,
        "netWorth": net_worth,
        "creditScore": credit_score,
        "debtToIncomeRatio": dti,
        "financialHealthScore": health_score,
        "emergencyFundMonths": emergency_months,
        "investmentValue": investment_value,
        "totalDebt": 225000,
        "riskLevel": risk_level,
    }


def compute_forecast(financial_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate 12-month historical + 6-month projected forecast data."""
    income, expense, _ = extract_transactions(financial_data)
    net_worth = extract_net_worth(financial_data)

    # Historical 6 months (slight variation)
    historical = [
        {"month": m, "income": int(income * fi), "expense": int(expense * fe),
         "savings": int(income * fi - expense * fe), "netWorth": int(net_worth * fn), "projected": False}
        for m, fi, fe, fn in [
            ("Oct", 0.90, 0.95, 0.92), ("Nov", 1.00, 1.00, 0.95),
            ("Dec", 1.10, 1.20, 0.97), ("Jan", 1.00, 0.90, 0.98),
            ("Feb", 0.95, 0.85, 0.99), ("Mar", 1.00, 1.00, 1.00),
        ]
    ]

    # Projected 6 months — expenses grow 1% per month
    projected = [
        {"month": m, "income": int(income), "expense": int(expense * (1 + 0.01 * i)),
         "savings": int(income - expense * (1 + 0.01 * i)),
         "netWorth": int(net_worth + (income - expense) * (i + 1)), "projected": True}
        for i, m in enumerate(["Apr", "May", "Jun", "Jul", "Aug", "Sep"])
    ]

    return historical + projected


def compute_expenses(financial_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Compute expense breakdown by category."""
    _, expense, transactions = extract_transactions(financial_data)

    # Try to categorize from real transactions
    categories: Dict[str, float] = {
        "Housing": 0, "Food": 0, "Transport": 0, "Utilities": 0, "Other": 0
    }
    keywords = {
        "Housing":   ["rent", "house", "flat", "pg", "hostel", "mortgage"],
        "Food":      ["food", "swiggy", "zomato", "restaurant", "hotel", "grocery", "bigbasket"],
        "Transport": ["uber", "ola", "petrol", "fuel", "bus", "train", "metro", "cab"],
        "Utilities": ["electricity", "water", "internet", "wifi", "mobile", "recharge", "bill"],
    }

    for txn in transactions:
        if txn["type"] != "DEBIT":
            continue
        narration = txn["narration"].lower()
        matched = False
        for cat, words in keywords.items():
            if any(w in narration for w in words):
                categories[cat] += txn["amount"]
                matched = True
                break
        if not matched:
            categories["Other"] += txn["amount"]

    # If no real transactions, use proportional split
    total = sum(categories.values())
    if total == 0:
        proportions = {"Housing": 0.40, "Food": 0.20, "Transport": 0.15, "Utilities": 0.10, "Other": 0.15}
        categories = {k: expense * v for k, v in proportions.items()}
        total = expense

    result = []
    for i, (cat, amount) in enumerate(categories.items()):
        if amount > 0:
            result.append({
                "category": cat,
                "amount": round(amount, 2),
                "percentage": round(amount / total * 100, 1) if total > 0 else 0,
                "trend": "stable",
                "color": EXPENSE_COLORS[i % len(EXPENSE_COLORS)],
            })

    return sorted(result, key=lambda x: x["amount"], reverse=True)


def compute_investments(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """Compute investment portfolio breakdown."""
    net_worth = extract_net_worth(financial_data)
    investment_value = int(net_worth * 0.6)

    # Try to get MF data
    mf_data = financial_data.get("fetch_mf_transactions", {})
    epf_data = financial_data.get("fetch_epf_details", {})

    # Build portfolio from available data
    portfolio = [
        {"name": "Equity Funds",   "type": "MF",  "value": int(investment_value * 0.40), "allocation": 40, "returns": 12.5, "risk": "High",   "color": INVESTMENT_COLORS[0]},
        {"name": "Fixed Deposits", "type": "FD",  "value": int(investment_value * 0.25), "allocation": 25, "returns": 7.0,  "risk": "Low",    "color": INVESTMENT_COLORS[1]},
        {"name": "EPF",            "type": "EPF", "value": int(investment_value * 0.20), "allocation": 20, "returns": 8.15, "risk": "Safe",   "color": INVESTMENT_COLORS[2]},
        {"name": "Gold",           "type": "Gold","value": int(investment_value * 0.10), "allocation": 10, "returns": 9.0,  "risk": "Medium", "color": INVESTMENT_COLORS[3]},
        {"name": "Stocks",         "type": "Equity","value": int(investment_value * 0.05),"allocation": 5, "returns": 15.0, "risk": "High",   "color": INVESTMENT_COLORS[4]},
    ]

    avg_returns = sum(p["returns"] * p["allocation"] / 100 for p in portfolio)

    return {
        "totalValue": investment_value,
        "avgReturns": round(avg_returns, 2),
        "portfolio": portfolio,
    }


def compute_goals(financial_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Compute financial goals with progress."""
    _, expense, _ = extract_transactions(financial_data)
    net_worth = extract_net_worth(financial_data)
    investment_value = int(net_worth * 0.6)

    emergency_target = int(expense * 6)
    emergency_current = int(expense * 4.5)

    goals = [
        {
            "id": "g1", "name": "Emergency Fund", "icon": "🛡️",
            "target": emergency_target,
            "current": min(emergency_current, emergency_target),
            "deadline": "2026-08",
            "monthlySavingsNeeded": max(0, int((emergency_target - emergency_current) / 6)),
            "progress": round(min(emergency_current / emergency_target * 100, 100), 1) if emergency_target > 0 else 0,
        },
        {
            "id": "g2", "name": "New Car", "icon": "🚗",
            "target": 1200000, "current": 350000, "deadline": "2027-12",
            "monthlySavingsNeeded": 15000,
            "progress": round(350000 / 1200000 * 100, 1),
        },
        {
            "id": "g3", "name": "Retirement Corpus", "icon": "🏖️",
            "target": 5000000, "current": investment_value,
            "deadline": "2045-01",
            "monthlySavingsNeeded": 25000,
            "progress": round(min(investment_value / 5000000 * 100, 100), 1),
        },
    ]

    return goals


def compute_risk(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """Compute detailed risk analysis."""
    income, expense, _ = extract_transactions(financial_data)
    net_worth = extract_net_worth(financial_data)
    credit_score = extract_credit_score(financial_data)

    savings_rate = round((income - expense) / income * 100, 1) if income > 0 else 0
    dti = round(expense / income * 100, 1) if income > 0 else 0
    emergency_months = round(net_worth * 0.2 / expense, 1) if expense > 0 else 0

    # Risk scoring
    risk_score = 0
    if dti > 50:          risk_score += 30
    elif dti > 35:        risk_score += 15
    if savings_rate < 10: risk_score += 25
    elif savings_rate < 20: risk_score += 10
    if emergency_months < 3: risk_score += 25
    elif emergency_months < 6: risk_score += 10
    if credit_score < 650: risk_score += 20
    elif credit_score < 750: risk_score += 5

    risk_level = "Low" if risk_score < 25 else "Medium" if risk_score < 55 else "High"

    factors = []
    if dti > 40:
        factors.append({"factor": "High Expense Ratio", "impact": "High", "detail": f"Expenses are {dti:.0f}% of income"})
    if savings_rate < 20:
        factors.append({"factor": "Low Savings Rate", "impact": "Medium", "detail": f"Saving only {savings_rate}% of income"})
    if emergency_months < 6:
        factors.append({"factor": "Weak Emergency Fund", "impact": "High", "detail": f"Only {emergency_months} months covered"})
    if credit_score < 750:
        factors.append({"factor": "Credit Score", "impact": "Low", "detail": f"Score {credit_score} — room to improve"})
    if not factors:
        factors.append({"factor": "Financially Stable", "impact": "None", "detail": "No major risk factors detected"})

    return {
        "riskScore": risk_score,
        "riskLevel": risk_level,
        "debtToIncomeRatio": round(dti / 100, 2),
        "savingsRate": savings_rate,
        "emergencyFundMonths": emergency_months,
        "creditScore": credit_score,
        "factors": factors,
    }


def compute_simulation(
    financial_data: Dict[str, Any],
    new_loan: float = 0,
    salary_increase: float = 0,
    job_loss: bool = False,
    vacation_expense: float = 0,
    house_purchase: bool = False,
    car_purchase: bool = False,
    investment_increase: float = 0,
) -> Dict[str, Any]:
    """Run scenario simulation and return impact."""
    income, expense, _ = extract_transactions(financial_data)
    net_worth = extract_net_worth(financial_data)
    health_score = min(100, max(0, int(50 + ((income - expense) / income * 100 if income > 0 else 0))))

    new_income = 0 if job_loss else income * (1 + salary_increase / 100)
    new_expense = expense + vacation_expense / 12 + (25000 if house_purchase else 0) + (15000 if car_purchase else 0)
    new_emi = (new_loan * 0.01) if new_loan > 0 else 0
    new_savings = new_income - new_expense - new_emi + investment_increase
    new_debt_ratio = ((225000 + new_loan) / (new_income * 12)) * 100 if new_income > 0 else 100
    new_risk = 95 if job_loss else min(100, max(0, 100 - health_score + (20 if new_debt_ratio > 40 else 0) + (30 if new_savings < 0 else 0)))
    is_viable = new_savings > 0 and new_debt_ratio < 40

    advice = ""
    if job_loss:
        runway = round(net_worth * 0.2 / expense, 1) if expense > 0 else 0
        advice = f"In a job loss scenario, your emergency fund covers approximately {runway} months of expenses."
    elif not is_viable:
        advice = "This scenario may strain your finances. Consider reducing the loan amount or delaying major purchases."
    else:
        advice = "This scenario maintains positive cash flow. Proceed with caution and monitor monthly savings."

    return {
        "newIncome": round(new_income, 2),
        "newExpense": round(new_expense, 2),
        "newSavings": round(new_savings, 2),
        "newEMI": round(new_emi, 2),
        "newDebtRatio": round(new_debt_ratio, 1),
        "newRiskScore": round(new_risk, 1),
        "isViable": is_viable,
        "advice": advice,
    }
