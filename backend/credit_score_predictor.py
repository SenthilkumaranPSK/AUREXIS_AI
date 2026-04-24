"""
AUREXIS AI — Credit Score Predictor
ML-based credit score prediction and improvement recommendations
"""

import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger("aurexis")


class CreditScorePredictor:
    """ML-powered credit score prediction and analysis"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize pre-trained model with sample data"""
        # In production, this would be trained on real credit data
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Sample training data (features: payment_history, credit_utilization, credit_age, inquiries, accounts)
        X_train = np.array([
            [100, 10, 120, 0, 5],   # Excellent
            [98, 15, 100, 1, 4],    # Excellent
            [95, 20, 90, 1, 4],     # Good
            [90, 30, 80, 2, 3],     # Good
            [85, 40, 60, 3, 3],     # Fair
            [80, 50, 50, 4, 2],     # Fair
            [70, 60, 40, 5, 2],     # Poor
            [60, 80, 30, 6, 1],     # Poor
        ])
        y_train = np.array([850, 820, 780, 740, 680, 640, 580, 520])
        
        self.model.fit(X_train, y_train)
    
    def predict_credit_score(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict credit score based on financial behavior
        """
        # Extract features from financial data
        features = self._extract_features(financial_data)
        
        # Current credit score
        current_score = financial_data.get("fetch_credit_report", {}).get("creditReport", {}).get("score", 750)
        
        # Calculate payment history score (0-100)
        payment_history = self._calculate_payment_history(financial_data)
        
        # Calculate credit utilization (0-100)
        credit_utilization = self._calculate_credit_utilization(financial_data)
        
        # Calculate credit age in months
        credit_age = self._calculate_credit_age(financial_data)
        
        # Count recent inquiries
        recent_inquiries = self._count_recent_inquiries(financial_data)
        
        # Count active accounts
        active_accounts = self._count_active_accounts(financial_data)
        
        # Predict future score
        feature_vector = np.array([[
            payment_history,
            credit_utilization,
            credit_age,
            recent_inquiries,
            active_accounts
        ]])
        
        predicted_score = int(self.model.predict(feature_vector)[0])
        
        # Calculate score change
        score_change = predicted_score - current_score
        trend = "improving" if score_change > 0 else "declining" if score_change < 0 else "stable"
        
        # Generate score breakdown
        score_breakdown = {
            "payment_history": {
                "score": payment_history,
                "weight": 35,
                "impact": round(payment_history * 0.35, 1),
                "status": "excellent" if payment_history >= 95 else "good" if payment_history >= 85 else "fair"
            },
            "credit_utilization": {
                "score": 100 - credit_utilization,
                "weight": 30,
                "impact": round((100 - credit_utilization) * 0.30, 1),
                "status": "excellent" if credit_utilization <= 30 else "good" if credit_utilization <= 50 else "poor"
            },
            "credit_age": {
                "score": min(100, credit_age / 2),
                "weight": 15,
                "impact": round(min(100, credit_age / 2) * 0.15, 1),
                "status": "excellent" if credit_age >= 120 else "good" if credit_age >= 60 else "fair"
            },
            "credit_mix": {
                "score": min(100, active_accounts * 20),
                "weight": 10,
                "impact": round(min(100, active_accounts * 20) * 0.10, 1),
                "status": "excellent" if active_accounts >= 4 else "good" if active_accounts >= 2 else "fair"
            },
            "new_credit": {
                "score": max(0, 100 - (recent_inquiries * 20)),
                "weight": 10,
                "impact": round(max(0, 100 - (recent_inquiries * 20)) * 0.10, 1),
                "status": "excellent" if recent_inquiries <= 1 else "good" if recent_inquiries <= 3 else "poor"
            }
        }
        
        # Generate improvement recommendations
        recommendations = self._generate_improvement_recommendations(
            payment_history,
            credit_utilization,
            credit_age,
            recent_inquiries,
            active_accounts
        )
        
        # Calculate potential score increase
        potential_increase = self._calculate_potential_increase(
            payment_history,
            credit_utilization,
            recent_inquiries
        )
        
        return {
            "current_score": current_score,
            "predicted_score": predicted_score,
            "score_change": score_change,
            "trend": trend,
            "score_range": self._get_score_range(predicted_score),
            "score_breakdown": score_breakdown,
            "recommendations": recommendations,
            "potential_increase": potential_increase,
            "timeline_to_excellent": self._calculate_timeline_to_excellent(current_score),
            "risk_factors": self._identify_risk_factors(financial_data),
            "positive_factors": self._identify_positive_factors(financial_data)
        }
    
    def _extract_features(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract relevant features from financial data"""
        return {
            "payment_history": self._calculate_payment_history(financial_data),
            "credit_utilization": self._calculate_credit_utilization(financial_data),
            "credit_age": self._calculate_credit_age(financial_data),
            "inquiries": self._count_recent_inquiries(financial_data),
            "accounts": self._count_active_accounts(financial_data)
        }
    
    def _calculate_payment_history(self, financial_data: Dict[str, Any]) -> float:
        """Calculate payment history score (0-100)"""
        transactions = financial_data.get("fetch_bank_transactions", {}).get("transactions", [])
        
        if not transactions:
            return 85.0  # Default
        
        # Check for late payments or overdrafts
        late_payments = 0
        total_payments = 0
        
        for txn in transactions:
            if txn.get("type") == "debit":
                total_payments += 1
                # Simulate late payment detection (in real system, would check actual dates)
                if abs(float(txn.get("amount", 0))) > 50000:  # Large transactions
                    # Assume some might be late
                    if np.random.random() < 0.05:  # 5% chance
                        late_payments += 1
        
        if total_payments == 0:
            return 85.0
        
        on_time_percentage = ((total_payments - late_payments) / total_payments) * 100
        return round(on_time_percentage, 1)
    
    def _calculate_credit_utilization(self, financial_data: Dict[str, Any]) -> float:
        """Calculate credit utilization percentage"""
        credit_report = financial_data.get("fetch_credit_report", {}).get("creditReport", {})
        
        total_limit = credit_report.get("totalCreditLimit", 100000)
        used_credit = credit_report.get("usedCredit", 20000)
        
        if total_limit == 0:
            return 30.0  # Default safe value
        
        utilization = (used_credit / total_limit) * 100
        return round(utilization, 1)
    
    def _calculate_credit_age(self, financial_data: Dict[str, Any]) -> int:
        """Calculate average credit age in months"""
        credit_report = financial_data.get("fetch_credit_report", {}).get("creditReport", {})
        accounts = credit_report.get("accounts", [])
        
        if not accounts:
            return 60  # Default 5 years
        
        total_age = 0
        for account in accounts:
            opened_date = account.get("openedDate", "2020-01-01")
            try:
                opened = datetime.strptime(opened_date, "%Y-%m-%d")
                age_months = (datetime.now() - opened).days // 30
                total_age += age_months
            except:
                total_age += 60
        
        return total_age // len(accounts) if accounts else 60
    
    def _count_recent_inquiries(self, financial_data: Dict[str, Any]) -> int:
        """Count credit inquiries in last 6 months"""
        credit_report = financial_data.get("fetch_credit_report", {}).get("creditReport", {})
        inquiries = credit_report.get("inquiries", [])
        
        recent_count = 0
        six_months_ago = datetime.now() - timedelta(days=180)
        
        for inquiry in inquiries:
            inquiry_date = inquiry.get("date", "2026-01-01")
            try:
                inq_date = datetime.strptime(inquiry_date, "%Y-%m-%d")
                if inq_date >= six_months_ago:
                    recent_count += 1
            except:
                pass
        
        return recent_count
    
    def _count_active_accounts(self, financial_data: Dict[str, Any]) -> int:
        """Count active credit accounts"""
        credit_report = financial_data.get("fetch_credit_report", {}).get("creditReport", {})
        accounts = credit_report.get("accounts", [])
        
        active = sum(1 for acc in accounts if acc.get("status") == "active")
        return active if active > 0 else 3  # Default
    
    def _generate_improvement_recommendations(
        self,
        payment_history: float,
        credit_utilization: float,
        credit_age: int,
        inquiries: int,
        accounts: int
    ) -> List[Dict[str, Any]]:
        """Generate personalized recommendations to improve credit score"""
        recommendations = []
        
        # Payment history recommendations
        if payment_history < 95:
            recommendations.append({
                "category": "Payment History",
                "priority": "high",
                "action": "Set up automatic payments for all bills",
                "impact": "+50 to +100 points",
                "timeline": "6-12 months",
                "difficulty": "easy"
            })
        
        # Credit utilization recommendations
        if credit_utilization > 30:
            points_to_gain = int((credit_utilization - 30) * 2)
            recommendations.append({
                "category": "Credit Utilization",
                "priority": "high",
                "action": f"Reduce credit utilization from {credit_utilization}% to below 30%",
                "impact": f"+{points_to_gain} to +{points_to_gain + 30} points",
                "timeline": "1-3 months",
                "difficulty": "medium"
            })
        
        if credit_utilization > 50:
            recommendations.append({
                "category": "Credit Utilization",
                "priority": "critical",
                "action": "Pay down high-balance cards immediately",
                "impact": "+80 to +120 points",
                "timeline": "1-2 months",
                "difficulty": "hard"
            })
        
        # Credit age recommendations
        if credit_age < 60:
            recommendations.append({
                "category": "Credit Age",
                "priority": "medium",
                "action": "Keep old accounts open to increase average credit age",
                "impact": "+20 to +40 points",
                "timeline": "12-24 months",
                "difficulty": "easy"
            })
        
        # New credit recommendations
        if inquiries > 2:
            recommendations.append({
                "category": "New Credit",
                "priority": "medium",
                "action": "Avoid applying for new credit for 6 months",
                "impact": "+15 to +30 points",
                "timeline": "6 months",
                "difficulty": "easy"
            })
        
        # Credit mix recommendations
        if accounts < 3:
            recommendations.append({
                "category": "Credit Mix",
                "priority": "low",
                "action": "Consider adding a credit builder loan or secured card",
                "impact": "+10 to +25 points",
                "timeline": "6-12 months",
                "difficulty": "medium"
            })
        
        return recommendations
    
    def _calculate_potential_increase(
        self,
        payment_history: float,
        credit_utilization: float,
        inquiries: int
    ) -> Dict[str, Any]:
        """Calculate potential score increase with improvements"""
        potential = 0
        
        # Payment history improvement
        if payment_history < 100:
            potential += int((100 - payment_history) * 0.5)
        
        # Credit utilization improvement
        if credit_utilization > 30:
            potential += int((credit_utilization - 30) * 2)
        
        # Inquiry impact reduction
        if inquiries > 2:
            potential += (inquiries - 2) * 10
        
        return {
            "max_increase": potential,
            "timeframe": "6-12 months",
            "achievability": "high" if potential < 50 else "medium" if potential < 100 else "challenging",
            "monthly_increase": round(potential / 12, 1)
        }
    
    def _calculate_timeline_to_excellent(self, current_score: int) -> Dict[str, Any]:
        """Calculate timeline to reach excellent credit (800+)"""
        if current_score >= 800:
            return {
                "status": "already_excellent",
                "message": "You already have excellent credit!",
                "months": 0
            }
        
        points_needed = 800 - current_score
        
        # Estimate based on typical improvement rates
        if points_needed <= 50:
            months = 6
        elif points_needed <= 100:
            months = 12
        elif points_needed <= 150:
            months = 18
        else:
            months = 24
        
        return {
            "status": "achievable",
            "points_needed": points_needed,
            "months": months,
            "target_date": (datetime.now() + timedelta(days=30 * months)).strftime("%B %Y"),
            "monthly_improvement_needed": round(points_needed / months, 1)
        }
    
    def _identify_risk_factors(self, financial_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify factors negatively impacting credit score"""
        risk_factors = []
        
        credit_report = financial_data.get("fetch_credit_report", {}).get("creditReport", {})
        
        # High utilization
        utilization = self._calculate_credit_utilization(financial_data)
        if utilization > 50:
            risk_factors.append({
                "factor": "High Credit Utilization",
                "severity": "high",
                "description": f"Using {utilization}% of available credit (recommended: <30%)"
            })
        
        # Recent inquiries
        inquiries = self._count_recent_inquiries(financial_data)
        if inquiries > 3:
            risk_factors.append({
                "factor": "Multiple Credit Inquiries",
                "severity": "medium",
                "description": f"{inquiries} inquiries in last 6 months"
            })
        
        # Late payments
        if credit_report.get("latePayments", 0) > 0:
            risk_factors.append({
                "factor": "Late Payments",
                "severity": "high",
                "description": "Payment history shows late payments"
            })
        
        return risk_factors
    
    def _identify_positive_factors(self, financial_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify factors positively impacting credit score"""
        positive_factors = []
        
        # Good payment history
        payment_history = self._calculate_payment_history(financial_data)
        if payment_history >= 95:
            positive_factors.append({
                "factor": "Excellent Payment History",
                "impact": "high",
                "description": f"{payment_history}% on-time payments"
            })
        
        # Low utilization
        utilization = self._calculate_credit_utilization(financial_data)
        if utilization <= 30:
            positive_factors.append({
                "factor": "Low Credit Utilization",
                "impact": "high",
                "description": f"Only using {utilization}% of available credit"
            })
        
        # Long credit history
        credit_age = self._calculate_credit_age(financial_data)
        if credit_age >= 120:
            positive_factors.append({
                "factor": "Long Credit History",
                "impact": "medium",
                "description": f"Average account age: {credit_age // 12} years"
            })
        
        return positive_factors
    
    def _get_score_range(self, score: int) -> str:
        """Get credit score range category"""
        if score >= 800:
            return "Excellent (800-850)"
        elif score >= 740:
            return "Very Good (740-799)"
        elif score >= 670:
            return "Good (670-739)"
        elif score >= 580:
            return "Fair (580-669)"
        else:
            return "Poor (300-579)"


# Singleton instance
credit_score_predictor = CreditScorePredictor()
