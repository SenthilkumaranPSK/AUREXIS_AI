"""
AUREXIS AI — Fraud Detection System
Real-time fraud detection using ML and pattern analysis
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger("aurexis")


class FraudDetector:
    """ML-powered fraud detection and prevention"""
    
    def __init__(self):
        self.risk_threshold = 0.7  # 70% confidence for fraud alert
        self.velocity_limits = {
            "transactions_per_hour": 10,
            "transactions_per_day": 50,
            "amount_per_hour": 100000,
            "amount_per_day": 500000
        }
    
    def analyze_transaction(
        self,
        transaction: Dict[str, Any],
        user_history: List[Dict[str, Any]],
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a single transaction for fraud indicators
        """
        risk_score = 0.0
        risk_factors = []
        
        # Extract transaction details
        amount = abs(float(transaction.get("amount", 0)))
        category = transaction.get("category", "Other")
        location = transaction.get("location", "Unknown")
        timestamp = transaction.get("date", datetime.now().isoformat())
        merchant = transaction.get("description", "Unknown")
        
        # 1. Amount-based analysis
        amount_risk, amount_factors = self._analyze_amount(amount, user_history)
        risk_score += amount_risk
        risk_factors.extend(amount_factors)
        
        # 2. Velocity check
        velocity_risk, velocity_factors = self._check_velocity(transaction, user_history)
        risk_score += velocity_risk
        risk_factors.extend(velocity_factors)
        
        # 3. Location analysis
        location_risk, location_factors = self._analyze_location(location, user_history)
        risk_score += location_risk
        risk_factors.extend(location_factors)
        
        # 4. Time-based analysis
        time_risk, time_factors = self._analyze_time_pattern(timestamp, user_history)
        risk_score += time_risk
        risk_factors.extend(time_factors)
        
        # 5. Merchant analysis
        merchant_risk, merchant_factors = self._analyze_merchant(merchant, user_history)
        risk_score += merchant_risk
        risk_factors.extend(merchant_factors)
        
        # 6. Category analysis
        category_risk, category_factors = self._analyze_category(category, amount, user_history)
        risk_score += category_risk
        risk_factors.extend(category_factors)
        
        # Normalize risk score (0-1)
        risk_score = min(1.0, risk_score / 6.0)
        
        # Determine risk level
        if risk_score >= 0.8:
            risk_level = "critical"
            action = "block"
        elif risk_score >= 0.6:
            risk_level = "high"
            action = "review"
        elif risk_score >= 0.4:
            risk_level = "medium"
            action = "monitor"
        else:
            risk_level = "low"
            action = "allow"
        
        return {
            "transaction_id": transaction.get("id", "unknown"),
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommended_action": action,
            "risk_factors": risk_factors,
            "is_fraudulent": risk_score >= self.risk_threshold,
            "confidence": round(risk_score * 100, 1),
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _analyze_amount(
        self,
        amount: float,
        history: List[Dict[str, Any]]
    ) -> Tuple[float, List[Dict[str, str]]]:
        """Analyze transaction amount for anomalies"""
        risk = 0.0
        factors = []
        
        if not history:
            return 0.0, []
        
        # Calculate average and std dev
        amounts = [abs(float(t.get("amount", 0))) for t in history if t.get("type") == "debit"]
        if not amounts:
            return 0.0, []
        
        avg_amount = np.mean(amounts)
        std_amount = np.std(amounts)
        max_amount = np.max(amounts)
        
        # Check if amount is unusually high
        if amount > avg_amount + (3 * std_amount):
            risk += 0.8
            factors.append({
                "factor": "Unusually High Amount",
                "severity": "high",
                "description": f"₹{amount:,.0f} is {round(amount/avg_amount, 1)}x your average transaction"
            })
        elif amount > avg_amount + (2 * std_amount):
            risk += 0.5
            factors.append({
                "factor": "Above Average Amount",
                "severity": "medium",
                "description": f"₹{amount:,.0f} is significantly higher than usual"
            })
        
        # Check for round numbers (common in fraud)
        if amount >= 10000 and amount % 10000 == 0:
            risk += 0.3
            factors.append({
                "factor": "Round Number Transaction",
                "severity": "low",
                "description": f"₹{amount:,.0f} is a suspiciously round number"
            })
        
        return risk, factors
    
    def _check_velocity(
        self,
        transaction: Dict[str, Any],
        history: List[Dict[str, Any]]
    ) -> Tuple[float, List[Dict[str, str]]]:
        """Check transaction velocity (frequency and volume)"""
        risk = 0.0
        factors = []
        
        try:
            current_time = datetime.fromisoformat(transaction.get("date", datetime.now().isoformat()))
        except:
            current_time = datetime.now()
        
        # Count recent transactions
        hour_ago = current_time - timedelta(hours=1)
        day_ago = current_time - timedelta(days=1)
        
        recent_hour_count = 0
        recent_hour_amount = 0
        recent_day_count = 0
        recent_day_amount = 0
        
        for txn in history:
            try:
                txn_time = datetime.fromisoformat(txn.get("date", ""))
                amount = abs(float(txn.get("amount", 0)))
                
                if txn_time >= hour_ago:
                    recent_hour_count += 1
                    recent_hour_amount += amount
                
                if txn_time >= day_ago:
                    recent_day_count += 1
                    recent_day_amount += amount
            except:
                continue
        
        # Check hourly velocity
        if recent_hour_count > self.velocity_limits["transactions_per_hour"]:
            risk += 0.9
            factors.append({
                "factor": "High Transaction Frequency",
                "severity": "critical",
                "description": f"{recent_hour_count} transactions in last hour (limit: {self.velocity_limits['transactions_per_hour']})"
            })
        
        if recent_hour_amount > self.velocity_limits["amount_per_hour"]:
            risk += 0.8
            factors.append({
                "factor": "High Transaction Volume",
                "severity": "high",
                "description": f"₹{recent_hour_amount:,.0f} spent in last hour"
            })
        
        # Check daily velocity
        if recent_day_count > self.velocity_limits["transactions_per_day"]:
            risk += 0.6
            factors.append({
                "factor": "Unusual Daily Activity",
                "severity": "medium",
                "description": f"{recent_day_count} transactions today"
            })
        
        return risk, factors
    
    def _analyze_location(
        self,
        location: str,
        history: List[Dict[str, Any]]
    ) -> Tuple[float, List[Dict[str, str]]]:
        """Analyze transaction location for anomalies"""
        risk = 0.0
        factors = []
        
        # Get common locations from history
        location_counts = defaultdict(int)
        for txn in history[-50:]:  # Last 50 transactions
            loc = txn.get("location", "Unknown")
            location_counts[loc] += 1
        
        # Check if location is new
        if location not in location_counts and location != "Unknown":
            risk += 0.4
            factors.append({
                "factor": "New Location",
                "severity": "medium",
                "description": f"First transaction from {location}"
            })
        
        # Check for international transactions (if applicable)
        international_keywords = ["international", "foreign", "overseas", "USD", "EUR", "GBP"]
        if any(keyword in location.lower() for keyword in international_keywords):
            risk += 0.5
            factors.append({
                "factor": "International Transaction",
                "severity": "medium",
                "description": f"Transaction from {location}"
            })
        
        return risk, factors
    
    def _analyze_time_pattern(
        self,
        timestamp: str,
        history: List[Dict[str, Any]]
    ) -> Tuple[float, List[Dict[str, str]]]:
        """Analyze transaction time for unusual patterns"""
        risk = 0.0
        factors = []
        
        try:
            txn_time = datetime.fromisoformat(timestamp)
            hour = txn_time.hour
            
            # Check for unusual hours (2 AM - 5 AM)
            if 2 <= hour <= 5:
                risk += 0.5
                factors.append({
                    "factor": "Unusual Time",
                    "severity": "medium",
                    "description": f"Transaction at {hour}:00 (unusual hour)"
                })
            
            # Analyze historical time patterns
            hour_counts = defaultdict(int)
            for txn in history:
                try:
                    hist_time = datetime.fromisoformat(txn.get("date", ""))
                    hour_counts[hist_time.hour] += 1
                except:
                    continue
            
            # If this hour has very few historical transactions
            if hour_counts[hour] < 2 and len(history) > 20:
                risk += 0.3
                factors.append({
                    "factor": "Atypical Time Pattern",
                    "severity": "low",
                    "description": f"Rarely transact at {hour}:00"
                })
        
        except:
            pass
        
        return risk, factors
    
    def _analyze_merchant(
        self,
        merchant: str,
        history: List[Dict[str, Any]]
    ) -> Tuple[float, List[Dict[str, str]]]:
        """Analyze merchant for fraud indicators"""
        risk = 0.0
        factors = []
        
        # Check for suspicious keywords
        suspicious_keywords = [
            "crypto", "bitcoin", "gambling", "casino", "lottery",
            "wire transfer", "money transfer", "gift card"
        ]
        
        merchant_lower = merchant.lower()
        for keyword in suspicious_keywords:
            if keyword in merchant_lower:
                risk += 0.6
                factors.append({
                    "factor": "High-Risk Merchant Category",
                    "severity": "high",
                    "description": f"Transaction with {merchant} (high-risk category)"
                })
                break
        
        # Check if merchant is new
        merchant_history = [t.get("description", "") for t in history]
        if merchant not in merchant_history and merchant != "Unknown":
            risk += 0.2
            factors.append({
                "factor": "New Merchant",
                "severity": "low",
                "description": f"First transaction with {merchant}"
            })
        
        return risk, factors
    
    def _analyze_category(
        self,
        category: str,
        amount: float,
        history: List[Dict[str, Any]]
    ) -> Tuple[float, List[Dict[str, str]]]:
        """Analyze transaction category for anomalies"""
        risk = 0.0
        factors = []
        
        # Calculate average amount per category
        category_amounts = defaultdict(list)
        for txn in history:
            cat = txn.get("category", "Other")
            amt = abs(float(txn.get("amount", 0)))
            category_amounts[cat].append(amt)
        
        # Check if amount is unusual for this category
        if category in category_amounts and len(category_amounts[category]) > 3:
            avg_cat_amount = np.mean(category_amounts[category])
            std_cat_amount = np.std(category_amounts[category])
            
            if amount > avg_cat_amount + (2 * std_cat_amount):
                risk += 0.4
                factors.append({
                    "factor": "Unusual Amount for Category",
                    "severity": "medium",
                    "description": f"₹{amount:,.0f} is unusually high for {category}"
                })
        
        return risk, factors
    
    def detect_account_takeover(
        self,
        recent_activity: List[Dict[str, Any]],
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Detect potential account takeover attempts"""
        risk_score = 0.0
        indicators = []
        
        if not recent_activity:
            return {"risk_score": 0.0, "indicators": [], "is_takeover": False}
        
        # Check for sudden behavior changes
        recent_locations = set(t.get("location", "") for t in recent_activity[-10:])
        if len(recent_locations) > 5:
            risk_score += 0.6
            indicators.append("Multiple new locations in short time")
        
        # Check for password changes
        # (In real system, would check auth logs)
        
        # Check for unusual transaction patterns
        recent_amounts = [abs(float(t.get("amount", 0))) for t in recent_activity[-10:]]
        if recent_amounts:
            avg_recent = np.mean(recent_amounts)
            if avg_recent > 50000:
                risk_score += 0.5
                indicators.append("Sudden increase in transaction amounts")
        
        # Check for failed login attempts
        # (Would integrate with auth system)
        
        is_takeover = risk_score >= 0.7
        
        return {
            "risk_score": round(risk_score, 3),
            "indicators": indicators,
            "is_takeover": is_takeover,
            "recommended_action": "lock_account" if is_takeover else "monitor",
            "confidence": round(risk_score * 100, 1)
        }
    
    def generate_fraud_report(
        self,
        transactions: List[Dict[str, Any]],
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive fraud analysis report"""
        
        total_transactions = len(transactions)
        flagged_transactions = []
        risk_distribution = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        
        # Analyze each transaction
        for txn in transactions:
            analysis = self.analyze_transaction(txn, transactions, user_profile)
            
            if analysis["risk_level"] != "low":
                flagged_transactions.append({
                    "transaction": txn,
                    "analysis": analysis
                })
            
            risk_distribution[analysis["risk_level"]] += 1
        
        # Calculate overall risk score
        if total_transactions > 0:
            overall_risk = (
                risk_distribution["critical"] * 1.0 +
                risk_distribution["high"] * 0.7 +
                risk_distribution["medium"] * 0.4 +
                risk_distribution["low"] * 0.1
            ) / total_transactions
        else:
            overall_risk = 0.0
        
        # Check for account takeover
        takeover_analysis = self.detect_account_takeover(transactions[-20:], user_profile)
        
        return {
            "summary": {
                "total_transactions": total_transactions,
                "flagged_transactions": len(flagged_transactions),
                "overall_risk_score": round(overall_risk, 3),
                "risk_distribution": risk_distribution
            },
            "flagged_transactions": flagged_transactions[:10],  # Top 10
            "account_takeover_risk": takeover_analysis,
            "recommendations": self._generate_security_recommendations(
                overall_risk,
                takeover_analysis,
                flagged_transactions
            ),
            "report_timestamp": datetime.now().isoformat()
        }
    
    def _generate_security_recommendations(
        self,
        overall_risk: float,
        takeover_analysis: Dict,
        flagged_transactions: List
    ) -> List[Dict[str, str]]:
        """Generate security recommendations"""
        recommendations = []
        
        if overall_risk > 0.6:
            recommendations.append({
                "priority": "high",
                "action": "Enable Two-Factor Authentication",
                "reason": "High fraud risk detected"
            })
        
        if takeover_analysis["is_takeover"]:
            recommendations.append({
                "priority": "critical",
                "action": "Change Password Immediately",
                "reason": "Potential account takeover detected"
            })
        
        if len(flagged_transactions) > 5:
            recommendations.append({
                "priority": "high",
                "action": "Review Recent Transactions",
                "reason": f"{len(flagged_transactions)} suspicious transactions found"
            })
        
        recommendations.append({
            "priority": "medium",
            "action": "Set Up Transaction Alerts",
            "reason": "Get notified of all transactions in real-time"
        })
        
        recommendations.append({
            "priority": "low",
            "action": "Review Connected Devices",
            "reason": "Ensure only your devices have access"
        })
        
        return recommendations


# Singleton instance
fraud_detector = FraudDetector()
