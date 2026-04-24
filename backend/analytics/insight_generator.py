"""
Insight Generator
Generate actionable insights from financial patterns and data
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import statistics


class InsightGenerator:
    """Generate actionable financial insights"""
    
    def __init__(self):
        self.insight_templates = {
            "spending_increase": "Your {category} spending increased by {change}% this month",
            "spending_decrease": "Great job! You reduced {category} spending by {change}%",
            "recurring_high": "You have {count} recurring expenses totaling ₹{amount}/month",
            "savings_opportunity": "You could save ₹{amount}/month by optimizing {category}",
            "goal_progress": "You're {progress}% towards your {goal_name} goal",
            "income_growth": "Your income grew by {change}% compared to last month",
            "expense_ratio": "You're spending {ratio}% of your income",
            "emergency_fund": "Your emergency fund covers {months} months of expenses",
            "debt_burden": "Debt payments are {ratio}% of your income",
            "investment_growth": "Your investments grew by {change}% this month"
        }
    
    def generate_insights(
        self,
        financial_data: Dict,
        patterns: Dict = None,
        historical_data: List[Dict] = None
    ) -> List[Dict]:
        """
        Generate comprehensive insights
        
        Args:
            financial_data: Current financial data
            patterns: Detected patterns
            historical_data: Historical financial data
            
        Returns:
            List of insights with priority and actions
        """
        insights = []
        
        # Spending insights
        insights.extend(self._generate_spending_insights(financial_data, historical_data))
        
        # Income insights
        insights.extend(self._generate_income_insights(financial_data, historical_data))
        
        # Savings insights
        insights.extend(self._generate_savings_insights(financial_data))
        
        # Goal insights
        insights.extend(self._generate_goal_insights(financial_data))
        
        # Investment insights
        insights.extend(self._generate_investment_insights(financial_data, historical_data))
        
        # Debt insights
        insights.extend(self._generate_debt_insights(financial_data))
        
        # Pattern-based insights
        if patterns:
            insights.extend(self._generate_pattern_insights(patterns))
        
        # Sort by priority
        insights.sort(key=lambda x: x.get("priority", 5), reverse=True)
        
        return insights[:15]  # Return top 15 insights
    
    def _generate_spending_insights(
        self,
        financial_data: Dict,
        historical_data: List[Dict] = None
    ) -> List[Dict]:
        """Generate spending-related insights"""
        insights = []
        
        current_expenses = financial_data.get("total_expenses", 0)
        expenses_by_category = financial_data.get("expenses_by_category", {})
        
        # Compare with previous month
        if historical_data and len(historical_data) > 0:
            prev_expenses = historical_data[-1].get("total_expenses", 0)
            
            if prev_expenses > 0:
                change = ((current_expenses - prev_expenses) / prev_expenses) * 100
                
                if abs(change) > 10:
                    insights.append({
                        "type": "spending_trend",
                        "title": "Spending Change Alert",
                        "message": f"Your total spending {'increased' if change > 0 else 'decreased'} by {abs(change):.1f}% this month",
                        "priority": 8 if change > 0 else 6,
                        "category": "expenses",
                        "impact": "high" if abs(change) > 20 else "medium",
                        "action": "Review your expenses and identify the cause" if change > 0 else "Keep up the good work!",
                        "value": change
                    })
        
        # Category-specific insights
        for category, amount in expenses_by_category.items():
            if amount > current_expenses * 0.3:  # Category is >30% of total
                insights.append({
                    "type": "category_dominance",
                    "title": f"High {category.title()} Spending",
                    "message": f"{category.title()} expenses are {(amount/current_expenses)*100:.1f}% of your total spending",
                    "priority": 7,
                    "category": category,
                    "impact": "medium",
                    "action": f"Consider ways to reduce {category} expenses",
                    "value": amount
                })
        
        # Expense ratio insight
        income = financial_data.get("total_income", 0)
        if income > 0:
            expense_ratio = (current_expenses / income) * 100
            
            if expense_ratio > 80:
                insights.append({
                    "type": "expense_ratio",
                    "title": "High Expense Ratio",
                    "message": f"You're spending {expense_ratio:.1f}% of your income",
                    "priority": 9,
                    "category": "budget",
                    "impact": "high",
                    "action": "Try to reduce expenses or increase income",
                    "value": expense_ratio
                })
            elif expense_ratio < 50:
                insights.append({
                    "type": "expense_ratio",
                    "title": "Excellent Savings Rate",
                    "message": f"You're only spending {expense_ratio:.1f}% of your income",
                    "priority": 5,
                    "category": "budget",
                    "impact": "positive",
                    "action": "Consider investing the surplus",
                    "value": expense_ratio
                })
        
        return insights
    
    def _generate_income_insights(
        self,
        financial_data: Dict,
        historical_data: List[Dict] = None
    ) -> List[Dict]:
        """Generate income-related insights"""
        insights = []
        
        current_income = financial_data.get("total_income", 0)
        
        # Compare with previous month
        if historical_data and len(historical_data) > 0:
            prev_income = historical_data[-1].get("total_income", 0)
            
            if prev_income > 0:
                change = ((current_income - prev_income) / prev_income) * 100
                
                if abs(change) > 5:
                    insights.append({
                        "type": "income_trend",
                        "title": "Income Change",
                        "message": f"Your income {'increased' if change > 0 else 'decreased'} by {abs(change):.1f}% this month",
                        "priority": 7 if change < 0 else 5,
                        "category": "income",
                        "impact": "high" if change < 0 else "positive",
                        "action": "Adjust your budget accordingly" if change < 0 else "Great progress!",
                        "value": change
                    })
        
        # Income stability
        if historical_data and len(historical_data) >= 3:
            recent_incomes = [d.get("total_income", 0) for d in historical_data[-3:]]
            if len(recent_incomes) > 1:
                std_dev = statistics.stdev(recent_incomes)
                mean_income = statistics.mean(recent_incomes)
                
                if mean_income > 0:
                    cv = (std_dev / mean_income) * 100  # Coefficient of variation
                    
                    if cv > 20:
                        insights.append({
                            "type": "income_stability",
                            "title": "Variable Income",
                            "message": "Your income varies significantly month-to-month",
                            "priority": 6,
                            "category": "income",
                            "impact": "medium",
                            "action": "Build a larger emergency fund for stability",
                            "value": cv
                        })
        
        return insights
    
    def _generate_savings_insights(self, financial_data: Dict) -> List[Dict]:
        """Generate savings-related insights"""
        insights = []
        
        income = financial_data.get("total_income", 0)
        expenses = financial_data.get("total_expenses", 0)
        savings = income - expenses
        
        if income > 0:
            savings_rate = (savings / income) * 100
            
            if savings_rate < 10:
                insights.append({
                    "type": "low_savings",
                    "title": "Low Savings Rate",
                    "message": f"You're only saving {savings_rate:.1f}% of your income",
                    "priority": 9,
                    "category": "savings",
                    "impact": "high",
                    "action": "Aim to save at least 20% of your income",
                    "value": savings_rate
                })
            elif savings_rate > 30:
                insights.append({
                    "type": "high_savings",
                    "title": "Excellent Savings Rate",
                    "message": f"You're saving {savings_rate:.1f}% of your income",
                    "priority": 5,
                    "category": "savings",
                    "impact": "positive",
                    "action": "Consider investing for long-term growth",
                    "value": savings_rate
                })
        
        # Emergency fund
        monthly_expenses = expenses
        emergency_fund = financial_data.get("emergency_fund", 0)
        
        if monthly_expenses > 0:
            months_covered = emergency_fund / monthly_expenses
            
            if months_covered < 3:
                insights.append({
                    "type": "emergency_fund",
                    "title": "Build Emergency Fund",
                    "message": f"Your emergency fund covers only {months_covered:.1f} months",
                    "priority": 8,
                    "category": "savings",
                    "impact": "high",
                    "action": "Aim for 6 months of expenses in emergency fund",
                    "value": months_covered
                })
            elif months_covered >= 6:
                insights.append({
                    "type": "emergency_fund",
                    "title": "Strong Emergency Fund",
                    "message": f"Your emergency fund covers {months_covered:.1f} months",
                    "priority": 4,
                    "category": "savings",
                    "impact": "positive",
                    "action": "Well done! Consider investing surplus funds",
                    "value": months_covered
                })
        
        return insights
    
    def _generate_goal_insights(self, financial_data: Dict) -> List[Dict]:
        """Generate goal-related insights"""
        insights = []
        
        goals = financial_data.get("goals", [])
        
        for goal in goals:
            target = goal.get("target_amount", 0)
            current = goal.get("current_amount", 0)
            deadline = goal.get("deadline")
            name = goal.get("name", "Goal")
            
            if target > 0:
                progress = (current / target) * 100
                
                # Calculate required monthly savings
                if deadline:
                    try:
                        deadline_date = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
                        months_remaining = max(1, (deadline_date - datetime.now()).days / 30)
                        remaining_amount = target - current
                        monthly_required = remaining_amount / months_remaining
                        
                        if progress < 50 and months_remaining < 12:
                            insights.append({
                                "type": "goal_behind",
                                "title": f"{name} - Behind Schedule",
                                "message": f"You need to save ₹{monthly_required:,.0f}/month to reach this goal",
                                "priority": 7,
                                "category": "goals",
                                "impact": "medium",
                                "action": "Increase monthly contributions or extend deadline",
                                "value": progress
                            })
                        elif progress > 80:
                            insights.append({
                                "type": "goal_near",
                                "title": f"{name} - Almost There!",
                                "message": f"You're {progress:.1f}% towards your goal",
                                "priority": 5,
                                "category": "goals",
                                "impact": "positive",
                                "action": "Keep up the momentum!",
                                "value": progress
                            })
                    except:
                        pass
        
        return insights
    
    def _generate_investment_insights(
        self,
        financial_data: Dict,
        historical_data: List[Dict] = None
    ) -> List[Dict]:
        """Generate investment-related insights"""
        insights = []
        
        investments = financial_data.get("investments", {})
        total_invested = sum(investments.values())
        net_worth = financial_data.get("net_worth", 0)
        
        # Investment allocation
        if net_worth > 0:
            investment_ratio = (total_invested / net_worth) * 100
            
            if investment_ratio < 20:
                insights.append({
                    "type": "low_investment",
                    "title": "Low Investment Allocation",
                    "message": f"Only {investment_ratio:.1f}% of your net worth is invested",
                    "priority": 7,
                    "category": "investment",
                    "impact": "medium",
                    "action": "Consider increasing investments for wealth growth",
                    "value": investment_ratio
                })
        
        # Investment growth
        if historical_data and len(historical_data) > 0:
            prev_investments = sum(historical_data[-1].get("investments", {}).values())
            
            if prev_investments > 0:
                growth = ((total_invested - prev_investments) / prev_investments) * 100
                
                if growth > 5:
                    insights.append({
                        "type": "investment_growth",
                        "title": "Investment Growth",
                        "message": f"Your investments grew by {growth:.1f}% this month",
                        "priority": 5,
                        "category": "investment",
                        "impact": "positive",
                        "action": "Continue your investment strategy",
                        "value": growth
                    })
        
        return insights
    
    def _generate_debt_insights(self, financial_data: Dict) -> List[Dict]:
        """Generate debt-related insights"""
        insights = []
        
        total_debt = financial_data.get("total_debt", 0)
        income = financial_data.get("total_income", 0)
        debt_payments = financial_data.get("debt_payments", 0)
        
        # Debt-to-income ratio
        if income > 0 and total_debt > 0:
            dti_ratio = (total_debt / (income * 12)) * 100
            
            if dti_ratio > 40:
                insights.append({
                    "type": "high_debt",
                    "title": "High Debt Burden",
                    "message": f"Your debt is {dti_ratio:.1f}% of your annual income",
                    "priority": 9,
                    "category": "debt",
                    "impact": "high",
                    "action": "Focus on debt reduction strategies",
                    "value": dti_ratio
                })
        
        # Debt payment ratio
        if income > 0 and debt_payments > 0:
            payment_ratio = (debt_payments / income) * 100
            
            if payment_ratio > 30:
                insights.append({
                    "type": "high_debt_payments",
                    "title": "High Debt Payments",
                    "message": f"Debt payments are {payment_ratio:.1f}% of your income",
                    "priority": 8,
                    "category": "debt",
                    "impact": "high",
                    "action": "Consider debt consolidation or refinancing",
                    "value": payment_ratio
                })
        
        return insights
    
    def _generate_pattern_insights(self, patterns: Dict) -> List[Dict]:
        """Generate insights from detected patterns"""
        insights = []
        
        # Recurring expenses
        recurring = patterns.get("recurring_transactions", [])
        if recurring:
            total_recurring = sum(t.get("amount", 0) for t in recurring)
            insights.append({
                "type": "recurring_expenses",
                "title": "Recurring Expenses",
                "message": f"You have {len(recurring)} recurring expenses totaling ₹{total_recurring:,.0f}/month",
                "priority": 6,
                "category": "expenses",
                "impact": "medium",
                "action": "Review subscriptions and cancel unused services",
                "value": total_recurring
            })
        
        # Unusual activity
        unusual = patterns.get("unusual_activity", [])
        if unusual:
            insights.append({
                "type": "unusual_activity",
                "title": "Unusual Transactions Detected",
                "message": f"Found {len(unusual)} unusual transactions",
                "priority": 7,
                "category": "security",
                "impact": "medium",
                "action": "Review these transactions for accuracy",
                "value": len(unusual)
            })
        
        # Lifestyle indicators
        lifestyle = patterns.get("lifestyle_indicators", {})
        if lifestyle.get("dining_out_frequency") == "high":
            insights.append({
                "type": "lifestyle",
                "title": "Frequent Dining Out",
                "message": "You dine out frequently",
                "priority": 5,
                "category": "lifestyle",
                "impact": "medium",
                "action": "Consider cooking at home more often to save money",
                "value": 0
            })
        
        return insights
    
    def generate_trend_analysis(
        self,
        historical_data: List[Dict],
        metric: str = "net_worth"
    ) -> Dict:
        """
        Analyze trends in financial metrics
        
        Args:
            historical_data: Historical financial data
            metric: Metric to analyze
            
        Returns:
            Trend analysis results
        """
        if not historical_data or len(historical_data) < 2:
            return {"trend": "insufficient_data"}
        
        values = [d.get(metric, 0) for d in historical_data]
        
        # Calculate trend
        if len(values) >= 3:
            # Simple linear regression
            n = len(values)
            x = list(range(n))
            x_mean = sum(x) / n
            y_mean = sum(values) / n
            
            numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
            denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
            
            if denominator != 0:
                slope = numerator / denominator
                
                # Determine trend
                if slope > 0:
                    trend = "increasing"
                elif slope < 0:
                    trend = "decreasing"
                else:
                    trend = "stable"
                
                # Calculate percentage change
                if values[0] != 0:
                    total_change = ((values[-1] - values[0]) / values[0]) * 100
                else:
                    total_change = 0
                
                return {
                    "trend": trend,
                    "slope": slope,
                    "total_change_pct": round(total_change, 2),
                    "current_value": values[-1],
                    "previous_value": values[0],
                    "data_points": n
                }
        
        return {"trend": "insufficient_data"}


# Global instance
insight_generator = InsightGenerator()
