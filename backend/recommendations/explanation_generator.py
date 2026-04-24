"""
Explanation Generator
Generate human-readable explanations for recommendations
"""

from typing import Dict, Any


class ExplanationGenerator:
    """Generate explanations for recommendations"""
    
    def generate(
        self,
        recommendation: Dict[str, Any],
        financial_data: Dict[str, Any]
    ) -> str:
        """
        Generate explanation for a recommendation
        
        Args:
            recommendation: Recommendation dictionary
            financial_data: User's financial data
            
        Returns:
            Human-readable explanation
        """
        category = recommendation.get("category", "")
        
        if category == "savings":
            return self._explain_savings(recommendation, financial_data)
        elif category == "expenses":
            return self._explain_expenses(recommendation, financial_data)
        elif category == "investment":
            return self._explain_investment(recommendation, financial_data)
        elif category == "debt":
            return self._explain_debt(recommendation, financial_data)
        elif category == "goals":
            return self._explain_goals(recommendation, financial_data)
        else:
            return self._generic_explanation(recommendation)
    
    def _explain_savings(self, rec: Dict, data: Dict) -> str:
        """Explain savings recommendation"""
        monthly_income = data.get("monthly_income", 0)
        monthly_expense = data.get("monthly_expense", 0)
        monthly_savings = monthly_income - monthly_expense
        savings_rate = (monthly_savings / monthly_income * 100) if monthly_income > 0 else 0
        
        explanation = f"**Why this matters:** "
        
        if savings_rate < 10:
            explanation += f"Your current savings rate of {savings_rate:.1f}% is below the recommended 20% minimum. "
            explanation += "This puts you at risk of not having enough for emergencies or future goals. "
        elif savings_rate < 20:
            explanation += f"While your {savings_rate:.1f}% savings rate is decent, increasing it to 20-30% "
            explanation += "will significantly improve your financial security and help you reach goals faster. "
        
        explanation += f"\n\n**Expected outcome:** {rec.get('expected_benefit', 'Improved financial health')}"
        explanation += f"\n\n**How to do it:** {rec.get('action', 'Increase monthly savings')}"
        
        return explanation
    
    def _explain_expenses(self, rec: Dict, data: Dict) -> str:
        """Explain expense recommendation"""
        monthly_income = data.get("monthly_income", 0)
        monthly_expense = data.get("monthly_expense", 0)
        expense_ratio = (monthly_expense / monthly_income * 100) if monthly_income > 0 else 0
        
        explanation = f"**Why this matters:** "
        
        if expense_ratio > 80:
            explanation += f"You're spending {expense_ratio:.1f}% of your income, leaving very little for savings. "
            explanation += "This is financially risky and unsustainable long-term. "
        else:
            explanation += "Reducing expenses in high-spending categories can free up significant funds "
            explanation += "for savings and investments without drastically changing your lifestyle. "
        
        explanation += f"\n\n**Expected outcome:** {rec.get('expected_benefit', 'More money for savings')}"
        explanation += f"\n\n**Action steps:** {rec.get('action', 'Review and reduce expenses')}"
        
        return explanation
    
    def _explain_investment(self, rec: Dict, data: Dict) -> str:
        """Explain investment recommendation"""
        monthly_savings = data.get("monthly_income", 0) - data.get("monthly_expense", 0)
        net_worth = data.get("net_worth", 0)
        
        explanation = f"**Why this matters:** "
        
        if monthly_savings > 0 and net_worth < 500000:
            explanation += "You have positive cash flow but limited investments. "
            explanation += "Investing early allows compound interest to work in your favor. "
            explanation += "Even small monthly investments can grow significantly over time. "
        else:
            explanation += "Proper asset allocation based on your age and risk tolerance "
            explanation += "can significantly improve your long-term returns while managing risk. "
        
        explanation += f"\n\n**Expected outcome:** {rec.get('expected_benefit', 'Higher returns')}"
        explanation += f"\n\n**Next steps:** {rec.get('action', 'Start investing')}"
        
        return explanation
    
    def _explain_debt(self, rec: Dict, data: Dict) -> str:
        """Explain debt recommendation"""
        explanation = f"**Why this matters:** "
        explanation += "High debt levels can severely impact your financial health. "
        explanation += "Interest payments reduce your ability to save and invest. "
        explanation += "Reducing debt improves credit score and financial flexibility. "
        
        explanation += f"\n\n**Expected outcome:** {rec.get('expected_benefit', 'Reduced debt burden')}"
        explanation += f"\n\n**Strategy:** {rec.get('action', 'Create repayment plan')}"
        
        return explanation
    
    def _explain_goals(self, rec: Dict, data: Dict) -> str:
        """Explain goal recommendation"""
        monthly_savings = data.get("monthly_income", 0) - data.get("monthly_expense", 0)
        
        explanation = f"**Why this matters:** "
        
        if monthly_savings > 0:
            explanation += "Having clear financial goals gives purpose to your savings "
            explanation += "and helps you stay motivated. Goals also help you prioritize "
            explanation += "spending and make better financial decisions. "
        else:
            explanation += "Setting realistic goals helps you understand what's achievable "
            explanation += "with your current financial situation and motivates positive changes. "
        
        explanation += f"\n\n**Expected outcome:** {rec.get('expected_benefit', 'Better financial planning')}"
        explanation += f"\n\n**Action:** {rec.get('action', 'Set financial goals')}"
        
        return explanation
    
    def _generic_explanation(self, rec: Dict) -> str:
        """Generic explanation"""
        explanation = f"**Why this matters:** {rec.get('description', 'This will improve your financial health.')}"
        explanation += f"\n\n**Expected outcome:** {rec.get('expected_benefit', 'Positive financial impact')}"
        explanation += f"\n\n**Action:** {rec.get('action', 'Follow the recommendation')}"
        
        return explanation


# Global instance
explanation_generator = ExplanationGenerator()
