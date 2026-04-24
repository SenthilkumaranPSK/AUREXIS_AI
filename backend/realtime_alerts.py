"""
AUREXIS AI — Real-time Alert System
Intelligent real-time alerts for financial events and anomalies
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger("aurexis")


class RealtimeAlertSystem:
    """Real-time financial alert generation and management"""
    
    def __init__(self):
        self.alert_thresholds = {
            "large_transaction": 50000,
            "unusual_spending": 2.0,  # 2x average
            "low_balance": 10000,
            "bill_due_days": 3,
            "goal_milestone": 0.25  # 25% increments
        }
    
    def generate_realtime_alerts(
        self,
        financial_data: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate real-time alerts based on financial activity
        """
        alerts = []
        
        # 1. Transaction alerts
        alerts.extend(self._check_transaction_alerts(financial_data))
        
        # 2. Balance alerts
        alerts.extend(self._check_balance_alerts(financial_data))
        
        # 3. Bill payment alerts
        alerts.extend(self._check_bill_alerts(financial_data))
        
        # 4. Goal progress alerts
        alerts.extend(self._check_goal_alerts(financial_data))
        
        # 5. Spending pattern alerts
        alerts.extend(self._check_spending_alerts(financial_data))
        
        # 6. Investment alerts
        alerts.extend(self._check_investment_alerts(financial_data))
        
        # 7. Credit score alerts
        alerts.extend(self._check_credit_alerts(financial_data))
        
        # 8. Savings alerts
        alerts.extend(self._check_savings_alerts(financial_data))
        
        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        alerts.sort(key=lambda x: priority_order.get(x["priority"], 4))
        
        return alerts
    
    def _check_transaction_alerts(
        self,
        financial_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check for transaction-related alerts"""
        alerts = []
        transactions = financial_data.get("fetch_bank_transactions", {}).get("transactions", [])
        
        if not transactions:
            return alerts
        
        # Get recent transactions (last 24 hours)
        now = datetime.now()
        recent_transactions = []
        
        for txn in transactions:
            try:
                txn_date = datetime.strptime(txn.get("date", ""), "%Y-%m-%d")
                if (now - txn_date).days <= 1:
                    recent_transactions.append(txn)
            except:
                continue
        
        # Check for large transactions
        for txn in recent_transactions:
            amount = abs(float(txn.get("amount", 0)))
            if amount >= self.alert_thresholds["large_transaction"]:
                alerts.append({
                    "id": f"txn_{txn.get('id', 'unknown')}",
                    "type": "large_transaction",
                    "priority": "high",
                    "title": "Large Transaction Detected",
                    "message": f"₹{amount:,.0f} spent on {txn.get('description', 'Unknown')}",
                    "amount": amount,
                    "category": txn.get("category", "Other"),
                    "timestamp": txn.get("date"),
                    "action_required": False,
                    "icon": "💳"
                })
        
        # Check for duplicate transactions
        txn_signatures = defaultdict(list)
        for txn in recent_transactions:
            signature = f"{txn.get('amount')}_{txn.get('description')}"
            txn_signatures[signature].append(txn)
        
        for signature, txns in txn_signatures.items():
            if len(txns) > 1:
                alerts.append({
                    "id": f"dup_{signature}",
                    "type": "duplicate_transaction",
                    "priority": "medium",
                    "title": "Duplicate Transaction Detected",
                    "message": f"{len(txns)} identical transactions found",
                    "count": len(txns),
                    "timestamp": datetime.now().isoformat(),
                    "action_required": True,
                    "icon": "⚠️"
                })
        
        return alerts
    
    def _check_balance_alerts(
        self,
        financial_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check for balance-related alerts"""
        alerts = []
        
        net_worth_data = financial_data.get("fetch_net_worth", {})
        current_balance = net_worth_data.get("totalAssets", 0) - net_worth_data.get("totalLiabilities", 0)
        
        # Low balance alert
        if current_balance < self.alert_thresholds["low_balance"]:
            alerts.append({
                "id": "low_balance",
                "type": "low_balance",
                "priority": "high",
                "title": "Low Balance Alert",
                "message": f"Your balance is ₹{current_balance:,.0f}. Consider transferring funds.",
                "current_balance": current_balance,
                "threshold": self.alert_thresholds["low_balance"],
                "timestamp": datetime.now().isoformat(),
                "action_required": True,
                "icon": "⚠️"
            })
        
        # Negative balance alert
        if current_balance < 0:
            alerts.append({
                "id": "negative_balance",
                "type": "negative_balance",
                "priority": "critical",
                "title": "Negative Balance!",
                "message": f"Your account is overdrawn by ₹{abs(current_balance):,.0f}",
                "current_balance": current_balance,
                "timestamp": datetime.now().isoformat(),
                "action_required": True,
                "icon": "🚨"
            })
        
        return alerts
    
    def _check_bill_alerts(
        self,
        financial_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check for upcoming bill payments"""
        alerts = []
        
        # Simulate upcoming bills (in real system, would fetch from database)
        upcoming_bills = [
            {"name": "Credit Card", "amount": 15000, "due_date": "2026-04-25"},
            {"name": "Electricity", "amount": 3000, "due_date": "2026-04-28"},
            {"name": "Internet", "amount": 1500, "due_date": "2026-04-30"},
        ]
        
        now = datetime.now()
        
        for bill in upcoming_bills:
            try:
                due_date = datetime.strptime(bill["due_date"], "%Y-%m-%d")
                days_until_due = (due_date - now).days
                
                if 0 <= days_until_due <= self.alert_thresholds["bill_due_days"]:
                    priority = "high" if days_until_due <= 1 else "medium"
                    alerts.append({
                        "id": f"bill_{bill['name'].lower().replace(' ', '_')}",
                        "type": "bill_due",
                        "priority": priority,
                        "title": f"{bill['name']} Bill Due Soon",
                        "message": f"₹{bill['amount']:,.0f} due in {days_until_due} day(s)",
                        "amount": bill["amount"],
                        "due_date": bill["due_date"],
                        "days_until_due": days_until_due,
                        "timestamp": datetime.now().isoformat(),
                        "action_required": True,
                        "icon": "📅"
                    })
            except:
                continue
        
        return alerts
    
    def _check_goal_alerts(
        self,
        financial_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check for financial goal progress"""
        alerts = []
        
        # Simulate goals (in real system, would fetch from database)
        goals = [
            {"name": "Emergency Fund", "target": 300000, "current": 275000},
            {"name": "New Car", "target": 1200000, "current": 350000},
        ]
        
        for goal in goals:
            progress = (goal["current"] / goal["target"]) * 100
            
            # Check for milestone achievements (25%, 50%, 75%, 90%)
            milestones = [25, 50, 75, 90]
            for milestone in milestones:
                if abs(progress - milestone) < 2:  # Within 2% of milestone
                    alerts.append({
                        "id": f"goal_{goal['name'].lower().replace(' ', '_')}_{milestone}",
                        "type": "goal_milestone",
                        "priority": "low",
                        "title": f"Goal Milestone Reached! 🎉",
                        "message": f"{goal['name']}: {milestone}% complete (₹{goal['current']:,.0f}/₹{goal['target']:,.0f})",
                        "goal_name": goal["name"],
                        "progress": round(progress, 1),
                        "milestone": milestone,
                        "timestamp": datetime.now().isoformat(),
                        "action_required": False,
                        "icon": "🎯"
                    })
        
        return alerts
    
    def _check_spending_alerts(
        self,
        financial_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check for unusual spending patterns"""
        alerts = []
        transactions = financial_data.get("fetch_bank_transactions", {}).get("transactions", [])
        
        if not transactions:
            return alerts
        
        # Calculate average monthly spending
        monthly_spending = defaultdict(float)
        for txn in transactions:
            if txn.get("type") == "debit":
                try:
                    month = txn.get("date", "")[:7]  # YYYY-MM
                    amount = abs(float(txn.get("amount", 0)))
                    monthly_spending[month] += amount
                except:
                    continue
        
        if len(monthly_spending) < 2:
            return alerts
        
        # Get current month and previous average
        current_month = datetime.now().strftime("%Y-%m")
        previous_months = [m for m in monthly_spending.keys() if m != current_month]
        
        if previous_months:
            avg_spending = sum(monthly_spending[m] for m in previous_months) / len(previous_months)
            current_spending = monthly_spending.get(current_month, 0)
            
            # Alert if current month spending is significantly higher
            if current_spending > avg_spending * self.alert_thresholds["unusual_spending"]:
                alerts.append({
                    "id": "unusual_spending",
                    "type": "unusual_spending",
                    "priority": "medium",
                    "title": "Unusual Spending Pattern",
                    "message": f"You've spent ₹{current_spending:,.0f} this month (avg: ₹{avg_spending:,.0f})",
                    "current_spending": current_spending,
                    "average_spending": avg_spending,
                    "increase_percentage": round(((current_spending - avg_spending) / avg_spending) * 100, 1),
                    "timestamp": datetime.now().isoformat(),
                    "action_required": False,
                    "icon": "📊"
                })
        
        return alerts
    
    def _check_investment_alerts(
        self,
        financial_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check for investment-related alerts"""
        alerts = []
        
        # Check mutual fund performance
        mf_data = financial_data.get("fetch_mf_transactions", {}).get("mfTransactions", [])
        
        for scheme in mf_data:
            scheme_name = scheme.get("schemeName", "Unknown")
            total_invested = 0
            current_value = 0
            
            for txn in scheme.get("txns", []):
                if len(txn) >= 5:
                    total_invested += txn[3]  # Invested amount
                    current_value += txn[4]   # Current value
            
            if total_invested > 0:
                returns = ((current_value - total_invested) / total_invested) * 100
                
                # Alert for significant gains
                if returns > 20:
                    alerts.append({
                        "id": f"mf_gain_{scheme_name.lower().replace(' ', '_')}",
                        "type": "investment_gain",
                        "priority": "low",
                        "title": "Investment Performing Well! 📈",
                        "message": f"{scheme_name}: +{returns:.1f}% returns",
                        "scheme_name": scheme_name,
                        "returns": round(returns, 2),
                        "invested": total_invested,
                        "current_value": current_value,
                        "timestamp": datetime.now().isoformat(),
                        "action_required": False,
                        "icon": "💹"
                    })
                
                # Alert for significant losses
                elif returns < -10:
                    alerts.append({
                        "id": f"mf_loss_{scheme_name.lower().replace(' ', '_')}",
                        "type": "investment_loss",
                        "priority": "medium",
                        "title": "Investment Underperforming",
                        "message": f"{scheme_name}: {returns:.1f}% returns. Consider reviewing.",
                        "scheme_name": scheme_name,
                        "returns": round(returns, 2),
                        "invested": total_invested,
                        "current_value": current_value,
                        "timestamp": datetime.now().isoformat(),
                        "action_required": True,
                        "icon": "📉"
                    })
        
        return alerts
    
    def _check_credit_alerts(
        self,
        financial_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check for credit score related alerts"""
        alerts = []
        
        credit_report = financial_data.get("fetch_credit_report", {}).get("creditReport", {})
        credit_score = credit_report.get("score", 750)
        
        # Alert for excellent credit score
        if credit_score >= 800:
            alerts.append({
                "id": "excellent_credit",
                "type": "credit_achievement",
                "priority": "low",
                "title": "Excellent Credit Score! 🌟",
                "message": f"Your credit score is {credit_score}. You qualify for best rates!",
                "credit_score": credit_score,
                "timestamp": datetime.now().isoformat(),
                "action_required": False,
                "icon": "⭐"
            })
        
        # Alert for low credit score
        elif credit_score < 650:
            alerts.append({
                "id": "low_credit",
                "type": "credit_warning",
                "priority": "high",
                "title": "Credit Score Needs Attention",
                "message": f"Your credit score is {credit_score}. Take action to improve it.",
                "credit_score": credit_score,
                "timestamp": datetime.now().isoformat(),
                "action_required": True,
                "icon": "⚠️"
            })
        
        return alerts
    
    def _check_savings_alerts(
        self,
        financial_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check for savings-related alerts"""
        alerts = []
        
        # Calculate savings rate
        transactions = financial_data.get("fetch_bank_transactions", {}).get("transactions", [])
        
        monthly_income = 0
        monthly_expense = 0
        income_count = 0
        expense_count = 0
        
        for txn in transactions:
            amount = abs(float(txn.get("amount", 0)))
            if txn.get("type") == "credit":
                monthly_income += amount
                income_count += 1
            elif txn.get("type") == "debit":
                monthly_expense += amount
                expense_count += 1
        
        if income_count > 0 and expense_count > 0:
            monthly_income = monthly_income / income_count
            monthly_expense = monthly_expense / expense_count
            savings_rate = ((monthly_income - monthly_expense) / monthly_income) * 100
            
            # Alert for low savings rate
            if savings_rate < 10:
                alerts.append({
                    "id": "low_savings",
                    "type": "savings_warning",
                    "priority": "high",
                    "title": "Low Savings Rate",
                    "message": f"You're saving only {savings_rate:.1f}% of income. Aim for 20%+",
                    "savings_rate": round(savings_rate, 1),
                    "monthly_income": monthly_income,
                    "monthly_expense": monthly_expense,
                    "timestamp": datetime.now().isoformat(),
                    "action_required": True,
                    "icon": "💰"
                })
            
            # Alert for excellent savings rate
            elif savings_rate > 30:
                alerts.append({
                    "id": "excellent_savings",
                    "type": "savings_achievement",
                    "priority": "low",
                    "title": "Excellent Savings! 🎉",
                    "message": f"You're saving {savings_rate:.1f}% of income. Keep it up!",
                    "savings_rate": round(savings_rate, 1),
                    "timestamp": datetime.now().isoformat(),
                    "action_required": False,
                    "icon": "💎"
                })
        
        return alerts
    
    def get_alert_summary(
        self,
        alerts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate summary of alerts"""
        
        priority_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        type_counts = defaultdict(int)
        action_required_count = 0
        
        for alert in alerts:
            priority_counts[alert["priority"]] += 1
            type_counts[alert["type"]] += 1
            if alert.get("action_required", False):
                action_required_count += 1
        
        return {
            "total_alerts": len(alerts),
            "priority_breakdown": priority_counts,
            "type_breakdown": dict(type_counts),
            "action_required": action_required_count,
            "most_common_type": max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else None,
            "timestamp": datetime.now().isoformat()
        }


# Singleton instance
realtime_alert_system = RealtimeAlertSystem()
