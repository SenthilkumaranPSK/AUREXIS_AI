"""
Advanced Recommendation Engine
Multi-factor recommendation generation with explanations
"""

from typing import List, Dict, Any
from datetime import datetime
from .priority_scorer import PriorityScorer
from .explanation_generator import ExplanationGenerator


class AdvancedRecommendationEngine:
    """Generate advanced, explainable recommendations"""
    
    def __init__(self):
        self.priority_scorer = PriorityScorer()
        self.explanation_generator = ExplanationGenerator()
    
    def generate_recommendations(
        self,
        financial_data: Dict[str, Any],
        user_profile: Dict[str, Any],
        max_recommendations: int = 10
    ) -> List[Dict]:
        """
        Generate personalized recommendations
        
        Args:
            financial_data: User's financial data
            user_profile: User profile information
            max_recommendations: Maximum number of recommendations
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Extract key metrics
        monthly_income = financial_data.get("monthly_income", 0)
        monthly_expense = financial_data.get("monthly_expense", 0)
        monthly_savings = monthly_income - monthly_expense
        savings_rate = (monthly_savings / monthly_income * 100) if monthly_income > 0 else 0
        net_worth = financial_data.get("net_worth", 0)
        
        # Generate different types of recommendations
        recommendations.extend(self._savings_recommendations(
            savings_rate, monthly_income, monthly_savings
        ))
        
        recommendations.extend(self._expense_recommendations(
            financial_data, monthly_income, monthly_expense
        ))
        
        recommendations.extend(self._investment_recommendations(
            net_worth, monthly_savings, user_profile
        ))
        
        recommendations.extend(self._debt_recommendations(
            financial_data, monthly_income
        ))
        
        recommendations.extend(self._goal_recommendations(
            financial_data, monthly_savings
        ))
        
        # Score and prioritize
        for rec in recommendations:
            rec["priority_score"] = self.priority_scorer.calculate_score(rec, financial_data)
            rec["explanation"] = self.explanation_generator.generate(rec, financial_data)
        
        # Sort by priority
        recommendations.sort(key=lambda x: x["priority_score"], reverse=True)
        
        # Return top recommendations
        return recommendations[:max_recommendations]
    
    def _savings_recommendations(
        self,
        savings_rate: float,
        monthly_income: float,
        monthly_savings: float
    ) -> List[Dict]:
        """Generate savings-related recommendations"""
        recommendations = []
        
        if savings_rate < 10:
            recommendations.append({
                "category": "savings",
                "title": "Increase Your Savings Rate",
                "description": f"Your current savings rate is {savings_rate:.1f}%. Aim for at least 20%.",
                "action": f"Try to save an additional ₹{monthly_income * 0.1:,.0f} per month",
                "impact": "high",
                "difficulty": "medium",
                "expected_benefit": f"Save ₹{monthly_income * 0.1 * 12:,.0f} more annually",
                "timeframe": "immediate",
                "risk_if_ignored": "Insufficient emergency fund and delayed financial goals"
            })
        elif savings_rate < 20:
            recommendations.append({
                "category": "savings",
                "title": "Good Savings, But Room for Improvement",
                "description": f"You're saving {savings_rate:.1f}%, which is good. Aim for 20-30% for optimal financial health.",
                "action": f"Increase savings by ₹{monthly_income * 0.05:,.0f} per month",
                "impact": "medium",
                "difficulty": "low",
                "expected_benefit": f"Additional ₹{monthly_income * 0.05 * 12:,.0f} annually",
                "timeframe": "1-3 months",
                "risk_if_ignored": "Slower wealth accumulation"
            })
        
        if monthly_savings > 0 and monthly_savings < monthly_income * 0.5:
            recommendations.append({
                "category": "savings",
                "title": "Automate Your Savings",
                "description": "Set up automatic transfers to savings account on payday",
                "action": "Set up auto-transfer of ₹{:,.0f} on salary day".format(monthly_savings),
                "impact": "medium",
                "difficulty": "low",
                "expected_benefit": "Consistent savings without manual effort",
                "timeframe": "immediate",
                "risk_if_ignored": "Inconsistent savings behavior"
            })
        
        return recommendations
    
    def _expense_recommendations(
        self,
        financial_data: Dict,
        monthly_income: float,
        monthly_expense: float
    ) -> List[Dict]:
        """Generate expense-related recommendations"""
        recommendations = []
        
        expense_ratio = (monthly_expense / monthly_income * 100) if monthly_income > 0 else 0
        
        if expense_ratio > 80:
            recommendations.append({
                "category": "expenses",
                "title": "Reduce Monthly Expenses Urgently",
                "description": f"You're spending {expense_ratio:.1f}% of your income. This is unsustainable.",
                "action": f"Identify and cut ₹{monthly_expense * 0.2:,.0f} in non-essential expenses",
                "impact": "critical",
                "difficulty": "high",
                "expected_benefit": f"Free up ₹{monthly_expense * 0.2 * 12:,.0f} annually",
                "timeframe": "immediate",
                "risk_if_ignored": "Debt accumulation and financial stress"
            })
        
        # Analyze expense categories
        transactions = financial_data.get("fetch_bank_transactions", {}).get("transactions", [])
        category_totals = {}
        
        for txn in transactions:
            if txn.get("type") == "debit":
                category = txn.get("category", "Other")
                amount = abs(float(txn.get("amount", 0)))
                category_totals[category] = category_totals.get(category, 0) + amount
        
        # Find high-spending categories
        if category_totals:
            max_category = max(category_totals, key=category_totals.get)
            max_amount = category_totals[max_category]
            
            if max_amount > monthly_income * 0.3:
                recommendations.append({
                    "category": "expenses",
                    "title": f"High {max_category} Spending Detected",
                    "description": f"You're spending ₹{max_amount:,.0f} on {max_category}",
                    "action": f"Review and reduce {max_category} expenses by 15-20%",
                    "impact": "high",
                    "difficulty": "medium",
                    "expected_benefit": f"Save ₹{max_amount * 0.15:,.0f} monthly",
                    "timeframe": "1-2 months",
                    "risk_if_ignored": "Continued overspending in this category"
                })
        
        return recommendations
    
    def _investment_recommendations(
        self,
        net_worth: float,
        monthly_savings: float,
        user_profile: Dict
    ) -> List[Dict]:
        """Generate investment-related recommendations"""
        recommendations = []
        
        age = user_profile.get("age", 30)
        
        if monthly_savings > 5000 and net_worth < 500000:
            recommendations.append({
                "category": "investment",
                "title": "Start Investing for Long-term Growth",
                "description": "You have positive savings. Start investing for wealth creation.",
                "action": "Invest ₹{:,.0f} monthly in diversified mutual funds".format(monthly_savings * 0.3),
                "impact": "high",
                "difficulty": "low",
                "expected_benefit": "Potential 12-15% annual returns vs 4% in savings",
                "timeframe": "immediate",
                "risk_if_ignored": "Missed wealth creation opportunity"
            })
        
        if net_worth > 100000 and age < 40:
            recommendations.append({
                "category": "investment",
                "title": "Increase Equity Allocation",
                "description": f"At age {age}, you can take more risk for higher returns",
                "action": "Allocate 60-70% of investments to equity mutual funds",
                "impact": "high",
                "difficulty": "medium",
                "expected_benefit": "Higher long-term returns",
                "timeframe": "3-6 months",
                "risk_if_ignored": "Lower returns, inflation erosion"
            })
        
        return recommendations
    
    def _debt_recommendations(
        self,
        financial_data: Dict,
        monthly_income: float
    ) -> List[Dict]:
        """Generate debt-related recommendations"""
        recommendations = []
        
        # Check for loans/EMIs
        total_debt = 0
        emis = []
        
        # This would come from actual debt data
        # For now, using placeholder logic
        
        if total_debt > monthly_income * 6:
            recommendations.append({
                "category": "debt",
                "title": "High Debt Burden Detected",
                "description": f"Your total debt is {total_debt / monthly_income:.1f}x your monthly income",
                "action": "Create debt repayment plan, prioritize high-interest debt",
                "impact": "critical",
                "difficulty": "high",
                "expected_benefit": "Reduced interest payments, improved credit score",
                "timeframe": "6-12 months",
                "risk_if_ignored": "Debt spiral, credit score damage"
            })
        
        return recommendations
    
    def _goal_recommendations(
        self,
        financial_data: Dict,
        monthly_savings: float
    ) -> List[Dict]:
        """Generate goal-related recommendations"""
        recommendations = []
        
        # Check if user has goals
        goals = financial_data.get("goals", [])
        
        if not goals and monthly_savings > 0:
            recommendations.append({
                "category": "goals",
                "title": "Set Financial Goals",
                "description": "You're saving but don't have defined goals",
                "action": "Set 2-3 specific financial goals (emergency fund, vacation, etc.)",
                "impact": "medium",
                "difficulty": "low",
                "expected_benefit": "Better motivation and financial planning",
                "timeframe": "immediate",
                "risk_if_ignored": "Aimless saving, potential overspending"
            })
        
        # Check goal progress
        for goal in goals:
            target = goal.get("target", 0)
            current = goal.get("current", 0)
            deadline = goal.get("deadline", "")
            
            if target > 0 and current < target * 0.5:
                months_remaining = 12  # Simplified
                required_monthly = (target - current) / months_remaining
                
                if required_monthly > monthly_savings:
                    recommendations.append({
                        "category": "goals",
                        "title": f"Goal '{goal.get('name')}' May Be Unrealistic",
                        "description": f"Need ₹{required_monthly:,.0f}/month but saving ₹{monthly_savings:,.0f}",
                        "action": "Either extend deadline or increase savings",
                        "impact": "medium",
                        "difficulty": "medium",
                        "expected_benefit": "Achievable goal timeline",
                        "timeframe": "1-3 months",
                        "risk_if_ignored": "Goal failure, demotivation"
                    })
        
        return recommendations


# Global instance
advanced_recommendation_engine = AdvancedRecommendationEngine()
