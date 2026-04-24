"""
Behavior Analyzer
Analyze financial behavior and habits
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import statistics


class BehaviorAnalyzer:
    """Analyze financial behavior patterns and habits"""
    
    def __init__(self):
        self.behavior_categories = [
            "discipline",
            "consistency",
            "planning",
            "risk_tolerance",
            "savings_habit",
            "spending_control"
        ]
    
    def analyze_behavior(
        self,
        financial_data: Dict,
        historical_data: List[Dict] = None,
        transactions: List[Dict] = None
    ) -> Dict:
        """
        Comprehensive behavior analysis
        
        Args:
            financial_data: Current financial data
            historical_data: Historical financial data
            transactions: Transaction history
            
        Returns:
            Behavior analysis results
        """
        analysis = {
            "overall_score": 0,
            "category_scores": {},
            "strengths": [],
            "weaknesses": [],
            "habits": [],
            "recommendations": [],
            "behavior_profile": ""
        }
        
        # Calculate category scores
        analysis["category_scores"]["discipline"] = self._calculate_discipline_score(
            financial_data, historical_data
        )
        analysis["category_scores"]["consistency"] = self._calculate_consistency_score(
            historical_data
        )
        analysis["category_scores"]["planning"] = self._calculate_planning_score(
            financial_data
        )
        analysis["category_scores"]["risk_tolerance"] = self._calculate_risk_tolerance(
            financial_data
        )
        analysis["category_scores"]["savings_habit"] = self._calculate_savings_habit(
            financial_data, historical_data
        )
        analysis["category_scores"]["spending_control"] = self._calculate_spending_control(
            financial_data, historical_data
        )
        
        # Calculate overall score
        scores = list(analysis["category_scores"].values())
        analysis["overall_score"] = round(sum(scores) / len(scores), 1) if scores else 0
        
        # Identify strengths and weaknesses
        for category, score in analysis["category_scores"].items():
            if score >= 75:
                analysis["strengths"].append({
                    "category": category,
                    "score": score,
                    "message": self._get_strength_message(category, score)
                })
            elif score < 50:
                analysis["weaknesses"].append({
                    "category": category,
                    "score": score,
                    "message": self._get_weakness_message(category, score)
                })
        
        # Detect habits
        if transactions:
            analysis["habits"] = self._detect_habits(transactions, financial_data)
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_behavior_recommendations(
            analysis["category_scores"],
            analysis["weaknesses"]
        )
        
        # Determine behavior profile
        analysis["behavior_profile"] = self._determine_behavior_profile(
            analysis["category_scores"]
        )
        
        return analysis
    
    def _calculate_discipline_score(
        self,
        financial_data: Dict,
        historical_data: List[Dict] = None
    ) -> float:
        """Calculate financial discipline score (0-100)"""
        score = 50  # Base score
        
        # Budget adherence
        budget = financial_data.get("budget", {})
        expenses_by_category = financial_data.get("expenses_by_category", {})
        
        if budget:
            adherence_count = 0
            total_categories = 0
            
            for category, limit in budget.items():
                actual = expenses_by_category.get(category, 0)
                if limit > 0:
                    total_categories += 1
                    if actual <= limit:
                        adherence_count += 1
                    elif actual <= limit * 1.1:  # Within 10% over
                        adherence_count += 0.5
            
            if total_categories > 0:
                adherence_rate = adherence_count / total_categories
                score += adherence_rate * 30  # Up to +30 points
        
        # Savings rate
        income = financial_data.get("total_income", 0)
        expenses = financial_data.get("total_expenses", 0)
        
        if income > 0:
            savings_rate = ((income - expenses) / income) * 100
            if savings_rate >= 30:
                score += 20
            elif savings_rate >= 20:
                score += 15
            elif savings_rate >= 10:
                score += 10
            elif savings_rate < 5:
                score -= 10
        
        # Debt management
        debt_payments = financial_data.get("debt_payments", 0)
        if income > 0 and debt_payments > 0:
            payment_ratio = (debt_payments / income) * 100
            if payment_ratio < 20:
                score += 10
            elif payment_ratio > 40:
                score -= 15
        
        return max(0, min(100, score))
    
    def _calculate_consistency_score(self, historical_data: List[Dict] = None) -> float:
        """Calculate financial consistency score (0-100)"""
        if not historical_data or len(historical_data) < 3:
            return 50  # Insufficient data
        
        score = 50
        
        # Income consistency
        incomes = [d.get("total_income", 0) for d in historical_data[-6:]]
        if len(incomes) > 1 and statistics.mean(incomes) > 0:
            cv = (statistics.stdev(incomes) / statistics.mean(incomes)) * 100
            if cv < 10:
                score += 20
            elif cv < 20:
                score += 10
            elif cv > 40:
                score -= 10
        
        # Expense consistency
        expenses = [d.get("total_expenses", 0) for d in historical_data[-6:]]
        if len(expenses) > 1 and statistics.mean(expenses) > 0:
            cv = (statistics.stdev(expenses) / statistics.mean(expenses)) * 100
            if cv < 15:
                score += 15
            elif cv < 25:
                score += 10
            elif cv > 50:
                score -= 10
        
        # Savings consistency
        savings = [
            d.get("total_income", 0) - d.get("total_expenses", 0)
            for d in historical_data[-6:]
        ]
        positive_savings_months = sum(1 for s in savings if s > 0)
        consistency_rate = positive_savings_months / len(savings)
        
        if consistency_rate >= 0.9:
            score += 15
        elif consistency_rate >= 0.7:
            score += 10
        elif consistency_rate < 0.5:
            score -= 15
        
        return max(0, min(100, score))
    
    def _calculate_planning_score(self, financial_data: Dict) -> float:
        """Calculate financial planning score (0-100)"""
        score = 30  # Base score
        
        # Has budget
        if financial_data.get("budget"):
            score += 20
        
        # Has goals
        goals = financial_data.get("goals", [])
        if goals:
            score += 15
            
            # Goals with deadlines
            goals_with_deadlines = sum(1 for g in goals if g.get("deadline"))
            if goals_with_deadlines == len(goals):
                score += 10
        
        # Has emergency fund
        emergency_fund = financial_data.get("emergency_fund", 0)
        monthly_expenses = financial_data.get("total_expenses", 0)
        
        if monthly_expenses > 0:
            months_covered = emergency_fund / monthly_expenses
            if months_covered >= 6:
                score += 15
            elif months_covered >= 3:
                score += 10
            elif months_covered < 1:
                score -= 10
        
        # Has investments
        investments = financial_data.get("investments", {})
        if investments and sum(investments.values()) > 0:
            score += 10
        
        return max(0, min(100, score))
    
    def _calculate_risk_tolerance(self, financial_data: Dict) -> float:
        """Calculate risk tolerance score (0-100, higher = more risk-tolerant)"""
        score = 50  # Base score (moderate)
        
        investments = financial_data.get("investments", {})
        total_invested = sum(investments.values())
        
        if total_invested > 0:
            # Equity allocation
            equity = investments.get("equity", 0)
            equity_pct = (equity / total_invested) * 100
            
            if equity_pct > 70:
                score += 20  # High risk tolerance
            elif equity_pct > 50:
                score += 10  # Moderate-high
            elif equity_pct < 20:
                score -= 20  # Low risk tolerance
            elif equity_pct < 40:
                score -= 10  # Moderate-low
            
            # Diversification
            num_asset_classes = sum(1 for v in investments.values() if v > 0)
            if num_asset_classes >= 4:
                score += 10  # Well diversified
            elif num_asset_classes <= 1:
                score -= 10  # Poor diversification
        
        # Emergency fund (affects risk capacity)
        emergency_fund = financial_data.get("emergency_fund", 0)
        monthly_expenses = financial_data.get("total_expenses", 0)
        
        if monthly_expenses > 0:
            months_covered = emergency_fund / monthly_expenses
            if months_covered >= 6:
                score += 10  # Can afford more risk
            elif months_covered < 3:
                score -= 10  # Should be more conservative
        
        return max(0, min(100, score))
    
    def _calculate_savings_habit(
        self,
        financial_data: Dict,
        historical_data: List[Dict] = None
    ) -> float:
        """Calculate savings habit score (0-100)"""
        score = 40  # Base score
        
        # Current savings rate
        income = financial_data.get("total_income", 0)
        expenses = financial_data.get("total_expenses", 0)
        
        if income > 0:
            savings_rate = ((income - expenses) / income) * 100
            
            if savings_rate >= 30:
                score += 30
            elif savings_rate >= 20:
                score += 20
            elif savings_rate >= 10:
                score += 10
            elif savings_rate < 5:
                score -= 20
        
        # Savings consistency
        if historical_data and len(historical_data) >= 3:
            savings_history = [
                d.get("total_income", 0) - d.get("total_expenses", 0)
                for d in historical_data[-6:]
            ]
            
            positive_months = sum(1 for s in savings_history if s > 0)
            consistency = positive_months / len(savings_history)
            
            if consistency >= 0.9:
                score += 20
            elif consistency >= 0.7:
                score += 10
            elif consistency < 0.5:
                score -= 10
        
        # Investment habit
        investments = financial_data.get("investments", {})
        if sum(investments.values()) > 0:
            score += 10
        
        return max(0, min(100, score))
    
    def _calculate_spending_control(
        self,
        financial_data: Dict,
        historical_data: List[Dict] = None
    ) -> float:
        """Calculate spending control score (0-100)"""
        score = 50  # Base score
        
        # Expense-to-income ratio
        income = financial_data.get("total_income", 0)
        expenses = financial_data.get("total_expenses", 0)
        
        if income > 0:
            expense_ratio = (expenses / income) * 100
            
            if expense_ratio < 50:
                score += 25
            elif expense_ratio < 70:
                score += 15
            elif expense_ratio < 80:
                score += 5
            elif expense_ratio > 90:
                score -= 20
        
        # Spending trend
        if historical_data and len(historical_data) >= 2:
            current_expenses = expenses
            prev_expenses = historical_data[-1].get("total_expenses", 0)
            
            if prev_expenses > 0:
                change = ((current_expenses - prev_expenses) / prev_expenses) * 100
                
                if change < -5:  # Reduced spending
                    score += 15
                elif change > 15:  # Increased spending significantly
                    score -= 15
        
        # Discretionary spending
        expenses_by_category = financial_data.get("expenses_by_category", {})
        discretionary = (
            expenses_by_category.get("entertainment", 0) +
            expenses_by_category.get("dining", 0) +
            expenses_by_category.get("shopping", 0)
        )
        
        if expenses > 0:
            discretionary_pct = (discretionary / expenses) * 100
            
            if discretionary_pct < 20:
                score += 10
            elif discretionary_pct > 40:
                score -= 10
        
        return max(0, min(100, score))
    
    def _detect_habits(
        self,
        transactions: List[Dict],
        financial_data: Dict
    ) -> List[Dict]:
        """Detect financial habits from transactions"""
        habits = []
        
        # Analyze transaction patterns
        if not transactions:
            return habits
        
        # Regular savings habit
        savings_transactions = [
            t for t in transactions
            if t.get("category") == "savings" or "save" in t.get("description", "").lower()
        ]
        
        if len(savings_transactions) >= 3:
            habits.append({
                "type": "regular_savings",
                "frequency": "monthly" if len(savings_transactions) >= 6 else "occasional",
                "description": "Regular savings deposits",
                "impact": "positive"
            })
        
        # Impulse spending
        large_discretionary = [
            t for t in transactions
            if t.get("amount", 0) > 5000 and
            t.get("category") in ["entertainment", "shopping", "dining"]
        ]
        
        if len(large_discretionary) > 5:
            habits.append({
                "type": "impulse_spending",
                "frequency": "frequent",
                "description": "Frequent large discretionary purchases",
                "impact": "negative"
            })
        
        # Bill payment habit
        bill_payments = [
            t for t in transactions
            if t.get("category") in ["utilities", "rent", "insurance"]
        ]
        
        if bill_payments:
            # Check if payments are on time (simplified)
            habits.append({
                "type": "bill_payment",
                "frequency": "regular",
                "description": "Regular bill payments",
                "impact": "positive"
            })
        
        # Investment habit
        investment_transactions = [
            t for t in transactions
            if t.get("category") == "investment"
        ]
        
        if len(investment_transactions) >= 3:
            habits.append({
                "type": "regular_investing",
                "frequency": "consistent",
                "description": "Consistent investment contributions",
                "impact": "positive"
            })
        
        return habits
    
    def _get_strength_message(self, category: str, score: float) -> str:
        """Get message for strength"""
        messages = {
            "discipline": "You show excellent financial discipline",
            "consistency": "Your financial behavior is very consistent",
            "planning": "You have strong financial planning habits",
            "risk_tolerance": "You have a well-balanced risk approach",
            "savings_habit": "You have excellent savings habits",
            "spending_control": "You have great spending control"
        }
        return messages.get(category, f"Strong {category}")
    
    def _get_weakness_message(self, category: str, score: float) -> str:
        """Get message for weakness"""
        messages = {
            "discipline": "Work on improving financial discipline",
            "consistency": "Try to be more consistent with finances",
            "planning": "Develop better financial planning habits",
            "risk_tolerance": "Review your risk management approach",
            "savings_habit": "Focus on building better savings habits",
            "spending_control": "Improve spending control"
        }
        return messages.get(category, f"Improve {category}")
    
    def _generate_behavior_recommendations(
        self,
        scores: Dict[str, float],
        weaknesses: List[Dict]
    ) -> List[str]:
        """Generate behavior improvement recommendations"""
        recommendations = []
        
        for weakness in weaknesses[:3]:  # Top 3 weaknesses
            category = weakness["category"]
            
            if category == "discipline":
                recommendations.append("Set up automatic transfers to savings on payday")
                recommendations.append("Use the 50/30/20 budgeting rule")
            elif category == "consistency":
                recommendations.append("Create a monthly financial review routine")
                recommendations.append("Set up automatic bill payments")
            elif category == "planning":
                recommendations.append("Set SMART financial goals with deadlines")
                recommendations.append("Build a 6-month emergency fund")
            elif category == "savings_habit":
                recommendations.append("Start with saving 10% of income, increase gradually")
                recommendations.append("Use the 'pay yourself first' principle")
            elif category == "spending_control":
                recommendations.append("Track all expenses for one month")
                recommendations.append("Implement a 24-hour rule for large purchases")
        
        return recommendations[:5]  # Return top 5
    
    def _determine_behavior_profile(self, scores: Dict[str, float]) -> str:
        """Determine overall behavior profile"""
        avg_score = sum(scores.values()) / len(scores)
        
        discipline = scores.get("discipline", 50)
        planning = scores.get("planning", 50)
        risk_tolerance = scores.get("risk_tolerance", 50)
        
        if avg_score >= 75:
            if risk_tolerance > 60:
                return "Disciplined Investor"
            else:
                return "Conservative Planner"
        elif avg_score >= 60:
            if planning > 60:
                return "Developing Planner"
            else:
                return "Moderate Saver"
        elif avg_score >= 40:
            if discipline < 50:
                return "Needs Discipline"
            else:
                return "Inconsistent Manager"
        else:
            return "Needs Improvement"


# Global instance
behavior_analyzer = BehaviorAnalyzer()
