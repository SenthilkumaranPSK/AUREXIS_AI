"""
AUREXIS AI — AI-Powered Budget Optimizer
Analyzes spending patterns, predicts expenses, and suggests optimal budget allocation
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger("aurexis")


class BudgetOptimizer:
    """AI-powered budget optimization engine"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        
    def analyze_spending_patterns(self, transactions: List[Dict]) -> Dict[str, Any]:
        """
        Analyze spending patterns from transaction history
        Returns insights about spending behavior
        """
        if not transactions:
            return {"error": "No transactions available"}
        
        # Categorize transactions
        category_spending = defaultdict(float)
        monthly_spending = defaultdict(float)
        day_of_week_spending = defaultdict(list)
        time_of_day_spending = defaultdict(list)
        
        for txn in transactions:
            amount = abs(float(txn.get("amount", 0)))
            category = txn.get("category", "Other")
            date_str = txn.get("date", "")
            
            if txn.get("type") == "debit" or amount < 0:
                category_spending[category] += amount
                
                # Parse date for temporal analysis
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    month_key = date.strftime("%Y-%m")
                    monthly_spending[month_key] += amount
                    
                    day_of_week = date.strftime("%A")
                    day_of_week_spending[day_of_week].append(amount)
                    
                    hour = date.hour if hasattr(date, 'hour') else 12
                    if hour < 12:
                        time_of_day_spending["Morning"].append(amount)
                    elif hour < 17:
                        time_of_day_spending["Afternoon"].append(amount)
                    else:
                        time_of_day_spending["Evening"].append(amount)
                except:
                    pass
        
        # Calculate insights
        total_spending = sum(category_spending.values())
        
        # Category analysis
        category_percentages = {
            cat: (amount / total_spending * 100) if total_spending > 0 else 0
            for cat, amount in category_spending.items()
        }
        
        # Find spending patterns
        highest_category = max(category_spending.items(), key=lambda x: x[1]) if category_spending else ("None", 0)
        
        # Day of week analysis
        day_averages = {
            day: np.mean(amounts) if amounts else 0
            for day, amounts in day_of_week_spending.items()
        }
        highest_spending_day = max(day_averages.items(), key=lambda x: x[1]) if day_averages else ("None", 0)
        
        # Time of day analysis
        time_averages = {
            time: np.mean(amounts) if amounts else 0
            for time, amounts in time_of_day_spending.items()
        }
        
        # Monthly trend
        monthly_trend = dict(sorted(monthly_spending.items()))
        avg_monthly_spending = np.mean(list(monthly_spending.values())) if monthly_spending else 0
        
        return {
            "total_spending": round(total_spending, 2),
            "category_breakdown": {k: round(v, 2) for k, v in category_spending.items()},
            "category_percentages": {k: round(v, 2) for k, v in category_percentages.items()},
            "highest_category": {
                "name": highest_category[0],
                "amount": round(highest_category[1], 2),
                "percentage": round(highest_category[1] / total_spending * 100, 2) if total_spending > 0 else 0
            },
            "temporal_patterns": {
                "highest_spending_day": highest_spending_day[0],
                "day_averages": {k: round(v, 2) for k, v in day_averages.items()},
                "time_of_day_averages": {k: round(v, 2) for k, v in time_averages.items()}
            },
            "monthly_trend": {k: round(v, 2) for k, v in monthly_trend.items()},
            "average_monthly_spending": round(avg_monthly_spending, 2)
        }
    
    def predict_future_expenses(self, transactions: List[Dict], months_ahead: int = 3) -> Dict[str, Any]:
        """
        Predict future expenses using historical data and ML
        """
        if not transactions:
            return {"error": "No transactions available"}
        
        # Extract monthly spending
        monthly_data = defaultdict(float)
        category_monthly = defaultdict(lambda: defaultdict(float))
        
        for txn in transactions:
            amount = abs(float(txn.get("amount", 0)))
            category = txn.get("category", "Other")
            date_str = txn.get("date", "")
            
            if txn.get("type") == "debit" or amount < 0:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    month_key = date.strftime("%Y-%m")
                    monthly_data[month_key] += amount
                    category_monthly[category][month_key] += amount
                except:
                    pass
        
        if not monthly_data:
            return {"error": "Insufficient data for prediction"}
        
        # Sort by date
        sorted_months = sorted(monthly_data.items())
        spending_values = [v for k, v in sorted_months]
        
        # Simple trend analysis with seasonality
        if len(spending_values) >= 3:
            # Calculate trend
            recent_avg = np.mean(spending_values[-3:])
            overall_avg = np.mean(spending_values)
            trend_factor = recent_avg / overall_avg if overall_avg > 0 else 1.0
            
            # Calculate growth rate
            if len(spending_values) >= 2:
                growth_rate = (spending_values[-1] - spending_values[-2]) / spending_values[-2] if spending_values[-2] > 0 else 0
            else:
                growth_rate = 0
            
            # Predict future months
            predictions = []
            last_value = spending_values[-1]
            
            for i in range(1, months_ahead + 1):
                # Apply trend and growth
                predicted = last_value * (1 + growth_rate * 0.5) * trend_factor
                
                # Add some seasonality (simplified)
                month_index = (len(spending_values) + i - 1) % 12
                seasonal_factor = 1.0 + (0.1 if month_index in [11, 0, 3, 4] else 0)  # Higher in Dec, Jan, Apr, May
                
                predicted *= seasonal_factor
                predictions.append(round(predicted, 2))
                last_value = predicted
            
            # Predict by category
            category_predictions = {}
            for category, monthly_cat_data in category_monthly.items():
                cat_values = [monthly_cat_data.get(month, 0) for month, _ in sorted_months]
                if cat_values:
                    cat_avg = np.mean(cat_values[-3:]) if len(cat_values) >= 3 else np.mean(cat_values)
                    category_predictions[category] = round(cat_avg, 2)
            
            # Generate prediction dates
            last_date = datetime.strptime(sorted_months[-1][0], "%Y-%m")
            prediction_months = []
            for i in range(1, months_ahead + 1):
                future_date = last_date + timedelta(days=30 * i)
                prediction_months.append(future_date.strftime("%Y-%m"))
            
            return {
                "predictions": [
                    {"month": month, "predicted_spending": amount}
                    for month, amount in zip(prediction_months, predictions)
                ],
                "total_predicted": round(sum(predictions), 2),
                "average_predicted": round(np.mean(predictions), 2),
                "trend": "increasing" if growth_rate > 0.05 else "decreasing" if growth_rate < -0.05 else "stable",
                "growth_rate": round(growth_rate * 100, 2),
                "confidence": "high" if len(spending_values) >= 6 else "medium" if len(spending_values) >= 3 else "low",
                "category_predictions": category_predictions
            }
        else:
            # Not enough data, use simple average
            avg_spending = np.mean(spending_values)
            predictions = [round(avg_spending, 2)] * months_ahead
            
            return {
                "predictions": [
                    {"month": f"Month {i+1}", "predicted_spending": amount}
                    for i, amount in enumerate(predictions)
                ],
                "total_predicted": round(sum(predictions), 2),
                "average_predicted": round(avg_spending, 2),
                "trend": "stable",
                "growth_rate": 0,
                "confidence": "low",
                "category_predictions": {}
            }
    
    def suggest_optimal_budget(
        self,
        income: float,
        current_spending: Dict[str, float],
        financial_goals: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Suggest optimal budget allocation based on income and goals
        Uses the 50/30/20 rule as baseline with AI adjustments
        """
        if income <= 0:
            return {"error": "Invalid income"}
        
        # Calculate current allocation
        total_spending = sum(current_spending.values())
        current_allocation = {
            cat: (amount / total_spending * 100) if total_spending > 0 else 0
            for cat, amount in current_spending.items()
        }
        
        # Define category types
        needs_categories = ["Rent", "Groceries", "Utilities", "Healthcare", "Transportation", "Insurance"]
        wants_categories = ["Entertainment", "Dining", "Shopping", "Travel", "Hobbies"]
        savings_categories = ["Savings", "Investments", "Emergency Fund"]
        
        # Calculate current needs/wants/savings
        current_needs = sum(current_spending.get(cat, 0) for cat in needs_categories)
        current_wants = sum(current_spending.get(cat, 0) for cat in wants_categories)
        current_savings = income - total_spending
        
        # Optimal allocation (50/30/20 rule)
        optimal_needs = income * 0.50
        optimal_wants = income * 0.30
        optimal_savings = income * 0.20
        
        # Adjust based on financial goals
        if financial_goals:
            total_goal_amount = sum(goal.get("target_amount", 0) for goal in financial_goals)
            months_to_goal = min(goal.get("months_remaining", 12) for goal in financial_goals) if financial_goals else 12
            
            if months_to_goal > 0:
                monthly_goal_savings = total_goal_amount / months_to_goal
                if monthly_goal_savings > optimal_savings:
                    # Increase savings, reduce wants
                    optimal_savings = min(monthly_goal_savings, income * 0.40)
                    optimal_wants = income - optimal_needs - optimal_savings
        
        # Generate category-wise recommendations
        recommendations = {}
        
        for category, current_amount in current_spending.items():
            if category in needs_categories:
                target = (current_amount / current_needs * optimal_needs) if current_needs > 0 else optimal_needs / len(needs_categories)
            elif category in wants_categories:
                target = (current_amount / current_wants * optimal_wants) if current_wants > 0 else optimal_wants / len(wants_categories)
            else:
                target = current_amount
            
            difference = target - current_amount
            recommendations[category] = {
                "current": round(current_amount, 2),
                "recommended": round(target, 2),
                "difference": round(difference, 2),
                "action": "reduce" if difference < 0 else "increase" if difference > 0 else "maintain"
            }
        
        # Add savings recommendation
        recommendations["Savings"] = {
            "current": round(current_savings, 2),
            "recommended": round(optimal_savings, 2),
            "difference": round(optimal_savings - current_savings, 2),
            "action": "increase" if optimal_savings > current_savings else "maintain"
        }
        
        # Calculate savings potential
        overspending_categories = [
            cat for cat, rec in recommendations.items()
            if rec["action"] == "reduce"
        ]
        
        potential_savings = sum(
            abs(recommendations[cat]["difference"])
            for cat in overspending_categories
        )
        
        # Generate insights
        insights = []
        
        if current_needs > optimal_needs:
            insights.append({
                "type": "warning",
                "category": "Needs",
                "message": f"Your essential expenses (₹{current_needs:,.0f}) exceed the recommended 50% of income. Consider ways to reduce fixed costs."
            })
        
        if current_wants > optimal_wants:
            insights.append({
                "type": "warning",
                "category": "Wants",
                "message": f"Your discretionary spending (₹{current_wants:,.0f}) is above the recommended 30%. Look for areas to cut back."
            })
        
        if current_savings < optimal_savings:
            insights.append({
                "type": "alert",
                "category": "Savings",
                "message": f"You're saving ₹{current_savings:,.0f}/month. Aim for ₹{optimal_savings:,.0f} (20% of income) to build financial security."
            })
        else:
            insights.append({
                "type": "success",
                "category": "Savings",
                "message": f"Great job! You're saving ₹{current_savings:,.0f}/month, which exceeds the recommended 20% target."
            })
        
        if potential_savings > 0:
            insights.append({
                "type": "opportunity",
                "category": "Optimization",
                "message": f"By optimizing your budget, you could save an additional ₹{potential_savings:,.0f}/month."
            })
        
        return {
            "income": round(income, 2),
            "current_allocation": {
                "needs": round(current_needs, 2),
                "wants": round(current_wants, 2),
                "savings": round(current_savings, 2)
            },
            "current_percentages": {
                "needs": round(current_needs / income * 100, 1) if income > 0 else 0,
                "wants": round(current_wants / income * 100, 1) if income > 0 else 0,
                "savings": round(current_savings / income * 100, 1) if income > 0 else 0
            },
            "optimal_allocation": {
                "needs": round(optimal_needs, 2),
                "wants": round(optimal_wants, 2),
                "savings": round(optimal_savings, 2)
            },
            "optimal_percentages": {
                "needs": 50,
                "wants": 30,
                "savings": 20
            },
            "recommendations": recommendations,
            "potential_monthly_savings": round(potential_savings, 2),
            "potential_annual_savings": round(potential_savings * 12, 2),
            "insights": insights,
            "optimization_score": round(min(100, (current_savings / optimal_savings * 100)) if optimal_savings > 0 else 0, 1)
        }
    
    def auto_categorize_transaction(self, description: str, amount: float) -> str:
        """
        Auto-categorize a transaction using keyword matching
        """
        description_lower = description.lower()
        
        # Category keywords
        categories = {
            "Groceries": ["grocery", "supermarket", "food", "vegetables", "fruits", "market"],
            "Dining": ["restaurant", "cafe", "coffee", "pizza", "burger", "food delivery", "zomato", "swiggy"],
            "Transportation": ["uber", "ola", "taxi", "fuel", "petrol", "diesel", "metro", "bus", "train"],
            "Utilities": ["electricity", "water", "gas", "internet", "broadband", "phone", "mobile"],
            "Entertainment": ["movie", "cinema", "netflix", "spotify", "prime", "gaming", "concert"],
            "Shopping": ["amazon", "flipkart", "mall", "store", "shop", "clothing", "fashion"],
            "Healthcare": ["hospital", "doctor", "pharmacy", "medicine", "clinic", "health"],
            "Insurance": ["insurance", "premium", "policy"],
            "Rent": ["rent", "lease", "housing"],
            "Education": ["school", "college", "course", "book", "tuition"],
            "Travel": ["flight", "hotel", "booking", "airbnb", "vacation"],
            "Investments": ["mutual fund", "stock", "sip", "investment", "trading"],
            "Savings": ["savings", "deposit", "fd", "fixed deposit"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        
        return "Other"
    
    def generate_savings_plan(
        self,
        current_savings: float,
        target_amount: float,
        months: int,
        current_monthly_savings: float
    ) -> Dict[str, Any]:
        """
        Generate a personalized savings plan to reach a financial goal
        """
        if months <= 0:
            return {"error": "Invalid time period"}
        
        remaining_amount = target_amount - current_savings
        required_monthly_savings = remaining_amount / months
        
        # Calculate if goal is achievable
        is_achievable = required_monthly_savings <= current_monthly_savings * 1.5
        
        # Generate milestones
        milestones = []
        for i in range(1, months + 1):
            milestone_amount = current_savings + (required_monthly_savings * i)
            milestones.append({
                "month": i,
                "target_amount": round(milestone_amount, 2),
                "monthly_savings_needed": round(required_monthly_savings, 2)
            })
        
        # Generate recommendations
        recommendations = []
        
        if required_monthly_savings > current_monthly_savings:
            gap = required_monthly_savings - current_monthly_savings
            recommendations.append({
                "type": "increase_savings",
                "message": f"Increase monthly savings by ₹{gap:,.0f} to reach your goal",
                "priority": "high"
            })
        
        if not is_achievable:
            recommendations.append({
                "type": "extend_timeline",
                "message": f"Consider extending your timeline to {int(remaining_amount / current_monthly_savings)} months for a more realistic goal",
                "priority": "medium"
            })
        
        recommendations.append({
            "type": "automate",
            "message": "Set up automatic transfers to your savings account on payday",
            "priority": "high"
        })
        
        recommendations.append({
            "type": "reduce_expenses",
            "message": "Review discretionary spending and redirect savings to this goal",
            "priority": "medium"
        })
        
        return {
            "goal_amount": round(target_amount, 2),
            "current_savings": round(current_savings, 2),
            "remaining_amount": round(remaining_amount, 2),
            "months_to_goal": months,
            "required_monthly_savings": round(required_monthly_savings, 2),
            "current_monthly_savings": round(current_monthly_savings, 2),
            "is_achievable": is_achievable,
            "completion_percentage": round(current_savings / target_amount * 100, 1) if target_amount > 0 else 0,
            "milestones": milestones[:6],  # Show first 6 months
            "recommendations": recommendations,
            "projected_completion_date": (datetime.now() + timedelta(days=30 * months)).strftime("%B %Y")
        }


# Singleton instance
budget_optimizer = BudgetOptimizer()
