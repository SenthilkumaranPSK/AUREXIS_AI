"""
AUREXIS AI — Explainable Recommendations System
Transparent AI recommendations with clear reasoning and confidence scores
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger("aurexis")


class ExplainableRecommendation:
    """A recommendation with full explanation and reasoning"""
    
    def __init__(
        self,
        title: str,
        category: str,
        priority: str,
        action: str,
        reasoning: List[str],
        confidence: float,
        impact: str,
        effort: str,
        timeline: str,
        expected_outcome: str,
        alternatives: Optional[List[Dict]] = None,
        data_sources: Optional[List[str]] = None
    ):
        self.title = title
        self.category = category
        self.priority = priority
        self.action = action
        self.reasoning = reasoning
        self.confidence = confidence
        self.impact = impact
        self.effort = effort
        self.timeline = timeline
        self.expected_outcome = expected_outcome
        self.alternatives = alternatives or []
        self.data_sources = data_sources or []
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "title": self.title,
            "category": self.category,
            "priority": self.priority,
            "action": self.action,
            "reasoning": self.reasoning,
            "confidence": round(self.confidence, 2),
            "impact": self.impact,
            "effort": self.effort,
            "timeline": self.timeline,
            "expected_outcome": self.expected_outcome,
            "alternatives": self.alternatives,
            "data_sources": self.data_sources,
            "created_at": self.created_at,
            "explanation": self._generate_explanation()
        }
    
    def _generate_explanation(self) -> str:
        """Generate human-readable explanation"""
        explanation = f"Based on our analysis, we recommend: {self.title}.\n\n"
        explanation += "Here's why:\n"
        for i, reason in enumerate(self.reasoning, 1):
            explanation += f"{i}. {reason}\n"
        explanation += f"\nThis recommendation has a {self.confidence*100:.0f}% confidence level "
        explanation += f"and is expected to have {self.impact} impact on your financial health."
        return explanation


class ExplainableRecommendationEngine:
    """Generate recommendations with full explanations"""
    
    def generate_recommendations(
        self,
        financial_data: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> List[ExplainableRecommendation]:
        """Generate explainable recommendations"""
        
        recommendations = []
        
        # Analyze different aspects
        recommendations.extend(self._analyze_savings(financial_data))
        recommendations.extend(self._analyze_spending(financial_data))
        recommendations.extend(self._analyze_debt(financial_data))
        recommendations.extend(self._analyze_investments(financial_data))
        recommendations.extend(self._analyze_credit(financial_data))
        recommendations.extend(self._analyze_goals(financial_data))
        
        # Sort by priority and confidence
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommendations.sort(
            key=lambda x: (priority_order.get(x.priority, 4), -x.confidence)
        )
        
        return recommendations
    
    def _analyze_savings(self, data: Dict) -> List[ExplainableRecommendation]:
        """Analyze savings and generate recommendations"""
        recommendations = []
        
        monthly_income = data.get("monthly_income", 0)
        monthly_expense = data.get("monthly_expense", 0)
        monthly_savings = monthly_income - monthly_expense
        savings_rate = (monthly_savings / monthly_income * 100) if monthly_income > 0 else 0
        
        # Low savings rate
        if savings_rate < 10:
            reasoning = [
                f"Your current savings rate is {savings_rate:.1f}%, which is below the recommended 20%",
                f"You're saving only ₹{monthly_savings:,.0f} per month",
                "Building savings is crucial for financial security and achieving goals",
                "Even small increases in savings rate compound significantly over time"
            ]
            
            alternatives = [
                {
                    "option": "Aggressive Savings",
                    "description": "Save 30% of income",
                    "pros": ["Faster goal achievement", "Better financial security"],
                    "cons": ["Requires significant lifestyle changes"],
                    "monthly_amount": monthly_income * 0.30
                },
                {
                    "option": "Moderate Savings",
                    "description": "Save 20% of income",
                    "pros": ["Balanced approach", "Sustainable long-term"],
                    "cons": ["Slower progress than aggressive"],
                    "monthly_amount": monthly_income * 0.20
                },
                {
                    "option": "Conservative Savings",
                    "description": "Save 15% of income",
                    "pros": ["Easier to maintain", "Less restrictive"],
                    "cons": ["Slower wealth building"],
                    "monthly_amount": monthly_income * 0.15
                }
            ]
            
            rec = ExplainableRecommendation(
                title="Increase Your Savings Rate",
                category="Savings",
                priority="high",
                action=f"Increase monthly savings from ₹{monthly_savings:,.0f} to ₹{monthly_income*0.20:,.0f} (20% of income)",
                reasoning=reasoning,
                confidence=0.95,
                impact="high",
                effort="medium",
                timeline="Start immediately, see results in 3-6 months",
                expected_outcome=f"Build ₹{monthly_income*0.20*12:,.0f} in savings over the next year",
                alternatives=alternatives,
                data_sources=["Monthly income analysis", "Expense tracking", "Financial best practices"]
            )
            recommendations.append(rec)
        
        # Good savings rate - reinforce
        elif savings_rate >= 25:
            reasoning = [
                f"Excellent! You're saving {savings_rate:.1f}% of your income",
                f"This is above the recommended 20% threshold",
                "Your disciplined saving habits will compound significantly",
                "Consider optimizing where these savings are invested"
            ]
            
            rec = ExplainableRecommendation(
                title="Optimize Your Savings Strategy",
                category="Savings",
                priority="low",
                action="Consider high-yield savings accounts or investment options for better returns",
                reasoning=reasoning,
                confidence=0.85,
                impact="medium",
                effort="low",
                timeline="Review options this month",
                expected_outcome="Potentially earn 2-3% more on your savings annually",
                alternatives=[
                    {
                        "option": "High-Yield Savings Account",
                        "description": "7-8% annual returns",
                        "pros": ["Safe", "Liquid", "Guaranteed returns"],
                        "cons": ["Lower than investment returns"]
                    },
                    {
                        "option": "Debt Mutual Funds",
                        "description": "8-10% annual returns",
                        "pros": ["Better returns", "Tax efficient"],
                        "cons": ["Market risk", "Lock-in period"]
                    }
                ],
                data_sources=["Savings rate analysis", "Investment options research"]
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _analyze_spending(self, data: Dict) -> List[ExplainableRecommendation]:
        """Analyze spending patterns"""
        recommendations = []
        
        transactions = data.get("fetch_bank_transactions", {}).get("transactions", [])
        
        # Calculate category spending
        category_spending = {}
        total_spending = 0
        
        for txn in transactions:
            if txn.get("type") == "debit":
                category = txn.get("category", "Other")
                amount = abs(float(txn.get("amount", 0)))
                category_spending[category] = category_spending.get(category, 0) + amount
                total_spending += amount
        
        # Find high spending categories
        for category, amount in category_spending.items():
            percentage = (amount / total_spending * 100) if total_spending > 0 else 0
            
            if percentage > 30 and category not in ["Rent", "EMI"]:
                reasoning = [
                    f"{category} accounts for {percentage:.1f}% of your total spending",
                    f"You're spending ₹{amount:,.0f} per month on {category}",
                    "This is significantly higher than the recommended allocation",
                    "Reducing this category could free up substantial funds for savings"
                ]
                
                potential_savings = amount * 0.20  # 20% reduction
                
                rec = ExplainableRecommendation(
                    title=f"Reduce {category} Spending",
                    category="Spending",
                    priority="medium",
                    action=f"Aim to reduce {category} spending by 20% (₹{potential_savings:,.0f}/month)",
                    reasoning=reasoning,
                    confidence=0.80,
                    impact="medium",
                    effort="medium",
                    timeline="Implement over next 2-3 months",
                    expected_outcome=f"Save ₹{potential_savings*12:,.0f} annually",
                    alternatives=[
                        {
                            "option": "Aggressive Reduction (30%)",
                            "savings": amount * 0.30,
                            "difficulty": "high"
                        },
                        {
                            "option": "Moderate Reduction (20%)",
                            "savings": amount * 0.20,
                            "difficulty": "medium"
                        },
                        {
                            "option": "Conservative Reduction (10%)",
                            "savings": amount * 0.10,
                            "difficulty": "low"
                        }
                    ],
                    data_sources=["Transaction history", "Category analysis"]
                )
                recommendations.append(rec)
        
        return recommendations
    
    def _analyze_debt(self, data: Dict) -> List[ExplainableRecommendation]:
        """Analyze debt situation"""
        recommendations = []
        
        net_worth_data = data.get("fetch_net_worth", {})
        total_liabilities = net_worth_data.get("totalLiabilities", 0)
        monthly_income = data.get("monthly_income", 80000)
        
        if total_liabilities > 0:
            debt_to_income = (total_liabilities / (monthly_income * 12)) * 100
            
            if debt_to_income > 40:
                reasoning = [
                    f"Your total debt is ₹{total_liabilities:,.0f}",
                    f"This represents {debt_to_income:.1f}% of your annual income",
                    "High debt levels can limit financial flexibility",
                    "Reducing debt should be a priority to improve financial health"
                ]
                
                rec = ExplainableRecommendation(
                    title="Create Debt Repayment Plan",
                    category="Debt",
                    priority="high",
                    action="Focus on paying off high-interest debt first (avalanche method)",
                    reasoning=reasoning,
                    confidence=0.90,
                    impact="high",
                    effort="high",
                    timeline="12-24 months depending on debt amount",
                    expected_outcome="Reduce debt burden and improve credit score",
                    alternatives=[
                        {
                            "method": "Avalanche Method",
                            "description": "Pay highest interest rate first",
                            "pros": ["Saves most on interest"],
                            "cons": ["May take longer to see progress"]
                        },
                        {
                            "method": "Snowball Method",
                            "description": "Pay smallest balance first",
                            "pros": ["Quick wins", "Motivating"],
                            "cons": ["May pay more interest"]
                        }
                    ],
                    data_sources=["Liability analysis", "Debt management best practices"]
                )
                recommendations.append(rec)
        
        return recommendations
    
    def _analyze_investments(self, data: Dict) -> List[ExplainableRecommendation]:
        """Analyze investment portfolio"""
        recommendations = []
        
        mf_data = data.get("fetch_mf_transactions", {}).get("mfTransactions", [])
        stock_data = data.get("fetch_stock_transactions", {}).get("stockTransactions", [])
        
        total_invested = 0
        for scheme in mf_data:
            for txn in scheme.get("txns", []):
                if len(txn) >= 4:
                    total_invested += txn[3]
        
        net_worth = data.get("fetch_net_worth", {}).get("totalAssets", 0)
        investment_percentage = (total_invested / net_worth * 100) if net_worth > 0 else 0
        
        if investment_percentage < 20:
            reasoning = [
                f"Only {investment_percentage:.1f}% of your assets are invested",
                "Recommended allocation is 30-40% for long-term wealth building",
                "Investments typically outperform savings accounts over time",
                "Starting early allows compound growth to work in your favor"
            ]
            
            rec = ExplainableRecommendation(
                title="Increase Investment Allocation",
                category="Investment",
                priority="medium",
                action="Gradually increase investment allocation to 30% of assets",
                reasoning=reasoning,
                confidence=0.85,
                impact="high",
                effort="medium",
                timeline="Build up over 12-18 months",
                expected_outcome="Potential 10-12% annual returns vs 6-7% in savings",
                alternatives=[
                    {
                        "option": "Equity Mutual Funds",
                        "risk": "Medium-High",
                        "returns": "12-15% annually",
                        "suitable_for": "Long-term goals (5+ years)"
                    },
                    {
                        "option": "Balanced Funds",
                        "risk": "Medium",
                        "returns": "10-12% annually",
                        "suitable_for": "Medium-term goals (3-5 years)"
                    },
                    {
                        "option": "Debt Funds",
                        "risk": "Low",
                        "returns": "7-9% annually",
                        "suitable_for": "Short-term goals (1-3 years)"
                    }
                ],
                data_sources=["Portfolio analysis", "Investment research"]
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _analyze_credit(self, data: Dict) -> List[ExplainableRecommendation]:
        """Analyze credit score"""
        recommendations = []
        
        credit_report = data.get("fetch_credit_report", {}).get("creditReport", {})
        credit_score = credit_report.get("score", 750)
        
        if credit_score < 750:
            reasoning = [
                f"Your current credit score is {credit_score}",
                "A score above 750 qualifies for better loan rates",
                "Improving your score can save thousands in interest",
                "Good credit opens doors to better financial products"
            ]
            
            rec = ExplainableRecommendation(
                title="Improve Credit Score",
                category="Credit",
                priority="medium",
                action="Focus on timely payments and reducing credit utilization below 30%",
                reasoning=reasoning,
                confidence=0.88,
                impact="medium",
                effort="low",
                timeline="6-12 months to see significant improvement",
                expected_outcome=f"Increase score from {credit_score} to 750+",
                alternatives=[
                    {
                        "action": "Pay all bills on time",
                        "impact": "35% of score",
                        "difficulty": "Easy"
                    },
                    {
                        "action": "Reduce credit utilization",
                        "impact": "30% of score",
                        "difficulty": "Medium"
                    },
                    {
                        "action": "Don't close old accounts",
                        "impact": "15% of score",
                        "difficulty": "Easy"
                    }
                ],
                data_sources=["Credit report analysis", "Credit scoring factors"]
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _analyze_goals(self, data: Dict) -> List[ExplainableRecommendation]:
        """Analyze financial goals"""
        recommendations = []
        
        # This would integrate with actual goals data
        # For now, provide general goal-setting recommendation
        
        reasoning = [
            "Clear financial goals provide direction and motivation",
            "Goals help prioritize spending and saving decisions",
            "Tracking progress keeps you accountable",
            "Achieving goals builds confidence and momentum"
        ]
        
        rec = ExplainableRecommendation(
            title="Set Clear Financial Goals",
            category="Goals",
            priority="low",
            action="Define 3-5 specific, measurable financial goals with timelines",
            reasoning=reasoning,
            confidence=0.75,
            impact="medium",
            effort="low",
            timeline="Set goals this week, review monthly",
            expected_outcome="Clear roadmap for financial success",
            alternatives=[
                {
                    "goal_type": "Emergency Fund",
                    "target": "6 months expenses",
                    "priority": "High"
                },
                {
                    "goal_type": "Retirement",
                    "target": "₹2-3 crores by age 60",
                    "priority": "High"
                },
                {
                    "goal_type": "Major Purchase",
                    "target": "House/Car down payment",
                    "priority": "Medium"
                }
            ],
            data_sources=["Financial planning best practices"]
        )
        recommendations.append(rec)
        
        return recommendations


# Singleton instance
explainable_recommendation_engine = ExplainableRecommendationEngine()
