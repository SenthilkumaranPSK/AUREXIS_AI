import logging
from datetime import datetime, timedelta
from urllib.parse import quote
from typing import Dict, Any, List, Optional

# Import helpers from analytics and health
from analytics import (
    compute_expenses,
    compute_forecast,
    compute_goals,
    compute_investments,
    compute_metrics,
    compute_risk,
)
from health import compute_health
from user_manager_json import UserManagerJSON

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    def build_user_profile(user: dict) -> dict:
        """Build user profile for frontend"""
        user_id = user.get("id", "")
        financial_data = user.get("financial_data")
        
        logger.info(f"Building profile for user {user_id}. Data type: {type(financial_data)}")
        
        # Ensure financial_data is a dictionary
        if not isinstance(financial_data, dict):
            logger.warning(f"financial_data is {type(financial_data)}, expected dict. Fetching fresh...")
            if user_id:
                financial_data = UserManagerJSON.get_all_user_data(user_id)
            else:
                financial_data = {}
        
        # Double check if get_all_user_data returned a list (which it shouldn't) or other
        if not isinstance(financial_data, dict):
            logger.error(f"FATAL: financial_data is still {type(financial_data)} after fetch. Defaulting to empty dict.")
            financial_data = {}

        metrics = compute_metrics(financial_data)
        expenses = compute_expenses(financial_data)
        goals = compute_goals(financial_data)
        investments = compute_investments(financial_data).get("portfolio", [])
        risk = compute_risk(financial_data)
        health = compute_health(financial_data)
        monthly_data = compute_forecast(financial_data)

        name = user.get("name", "Unknown")
        occupation = user.get("occupation") or "Professional"
        age = user.get("age") or 30
        location = user.get("location") or ""
        last_login = user.get("last_login")

        if hasattr(last_login, "isoformat"):
            last_active = last_login.isoformat()
        else:
            last_active = last_login or datetime.now().isoformat()

        avatar = UserService.build_avatar_data_uri(name)
        bank_name = user.get("bank_name", "") or ""
        account_number = UserService.mask_account_number(user.get("account_number", "") or "")
        account_type = user.get("account_type", "") or ""
        bank_location = user.get("bank_location", "") or location
        has_credit_card = bool(user.get("has_credit_card", False))

        alerts = UserService.build_profile_alerts(metrics, health)
        upcoming_emis = UserService.build_upcoming_emis(metrics, monthly_data)

        return {
            "id": user_id,
            "name": name,
            "avatar": avatar,
            "email": user.get("email", ""),
            "phone": user.get("phone", "") or "",
            "occupation": occupation,
            "age": age,
            "bankName": bank_name,
            "accountNumber": account_number,
            "accountType": account_type,
            "bankLocation": bank_location,
            "hasCreditCard": has_credit_card,
            "location": location,
            "monthlyIncome": metrics["monthlyIncome"],
            "monthlyExpense": metrics["monthlyExpense"],
            "netWorth": metrics["netWorth"],
            "savings": metrics["savings"],
            "totalDebt": metrics["totalDebt"],
            "riskLevel": risk["riskLevel"],
            "personalityTag": UserService.derive_personality_tag(metrics, risk),
            "lastActive": last_active,
            "creditScore": metrics["creditScore"],
            "emergencyFundMonths": metrics["emergencyFundMonths"],
            "investmentValue": metrics["investmentValue"],
            "savingsRate": metrics["savingsRate"],
            "debtToIncomeRatio": metrics["debtToIncomeRatio"],
            "financialHealthScore": health["overall"],
            "goals": [
                {
                    "id": goal.get("id", f"goal_{index}"),
                    "name": goal.get("name", "Goal"),
                    "target": goal.get("target", 0),
                    "current": goal.get("current", 0),
                    "deadline": goal.get("deadline", ""),
                    "icon": goal.get("icon", "Target"),
                    "monthlySavingsNeeded": goal.get("monthlySavingsNeeded", 0),
                }
                for index, goal in enumerate(goals, start=1)
            ],
            "monthlyData": [
                {
                    "month": item.get("month", ""),
                    "income": item.get("income", 0),
                    "expense": item.get("expense", 0),
                    "savings": item.get("savings", 0),
                    "netWorth": item.get("netWorth", 0),
                    "debt": metrics["totalDebt"],
                }
                for item in monthly_data
            ],
            "expenses": expenses,
            "investments": investments,
            "upcomingEMIs": upcoming_emis,
            "alerts": alerts,
        }

    @staticmethod
    def build_avatar_data_uri(name: str) -> str:
        """Generate a lightweight inline avatar for the frontend."""
        initials = "".join(part[0].upper() for part in name.split()[:2] if part) or "A"
        svg = (
            "<svg xmlns='http://www.w3.org/2000/svg' width='96' height='96' viewBox='0 0 96 96'>"
            "<rect width='96' height='96' rx='24' fill='#1d4ed8'/>"
            "<text x='48' y='56' text-anchor='middle' font-family='Arial, sans-serif' "
            "font-size='32' font-weight='700' fill='white'>"
            f"{initials}</text></svg>"
        )
        return f"data:image/svg+xml;utf8,{quote(svg)}"

    @staticmethod
    def mask_account_number(account_number: str) -> str:
        """Mask sensitive account numbers for the UI."""
        digits = "".join(char for char in account_number if char.isdigit())
        if len(digits) < 4:
            return ""
        return f"•••• {digits[-4:]}"

    @staticmethod
    def derive_personality_tag(metrics: dict, risk: dict) -> str:
        """Infer a lightweight personality label for the dashboard."""
        if metrics["savingsRate"] >= 30 and risk["riskLevel"] == "Low":
            return "Conservative Saver"
        if metrics["investmentValue"] >= max(metrics["netWorth"] * 0.45, 1):
            return "Investor"
        if metrics["debtToIncomeRatio"] >= 0.45:
            return "Debt Heavy"
        if metrics["savingsRate"] <= 10:
            return "High Spender"
        return "Balanced Planner"

    @staticmethod
    def build_profile_alerts(metrics: dict, health: dict) -> list[dict]:
        """Create dashboard-friendly alert cards from current metrics."""
        timestamp = datetime.now().isoformat()
        alerts = []

        if metrics["savingsRate"] < 20:
            alerts.append(
                {
                    "id": "alert_savings",
                    "type": "warning",
                    "title": "Savings Deficit Detected",
                    "message": f"Your savings velocity is currently at {metrics['savingsRate']}%. Target a minimum of 20% to ensure sustainable wealth accumulation.",
                    "timestamp": timestamp,
                }
            )

        if metrics["creditScore"] < 700:
            alerts.append(
                {
                    "id": "alert_credit",
                    "type": "warning",
                    "title": "Suboptimal Credit Profile",
                    "message": f"Credit score currently reads {metrics['creditScore']}. Consistent liability management can elevate this into the prime tier.",
                    "timestamp": timestamp,
                }
            )

        if not alerts:
            alerts.append(
                {
                    "id": "alert_health",
                    "type": "info",
                    "title": "System Health Overview",
                    "message": f"Your financial matrix shows a {health['label'].lower()} standing, scoring {health['overall']}/100. All primary indicators are within safe thresholds.",
                    "timestamp": timestamp,
                }
            )

        return alerts

    @staticmethod
    def build_upcoming_emis(metrics: dict, monthly_data: list) -> list[dict]:
        """Provide a simple EMI reminder set for the sidebar."""
        if metrics["totalDebt"] <= 0:
            return []

        due_date = (datetime.now() + timedelta(days=10)).date().isoformat()
        return [
            {
                "name": "Loan EMI",
                "amount": min(12500, max(2500, round(metrics["monthlyIncome"] * 0.12))),
                "dueDate": due_date,
                "type": "Loan",
            }
        ]
