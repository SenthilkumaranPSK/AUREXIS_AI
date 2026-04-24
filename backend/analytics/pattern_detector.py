"""
Pattern Detector
Detect spending patterns and financial behaviors
"""

import numpy as np
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict


class PatternDetector:
    """Detect patterns in financial data"""
    
    def detect_patterns(self, financial_data: Dict[str, Any]) -> Dict:
        """
        Detect all patterns in financial data
        
        Args:
            financial_data: User's financial data
            
        Returns:
            Dictionary with detected patterns
        """
        transactions = financial_data.get("fetch_bank_transactions", {}).get("transactions", [])
        
        return {
            "spending_patterns": self._detect_spending_patterns(transactions),
            "income_patterns": self._detect_income_patterns(transactions),
            "recurring_transactions": self._detect_recurring_transactions(transactions),
            "seasonal_patterns": self._detect_seasonal_patterns(transactions),
            "unusual_activity": self._detect_unusual_activity(transactions),
            "lifestyle_indicators": self._detect_lifestyle_indicators(transactions)
        }
    
    def _detect_spending_patterns(self, transactions: List[Dict]) -> Dict:
        """Detect spending patterns"""
        if not transactions:
            return {"pattern": "insufficient_data"}
        
        # Group by category
        category_spending = defaultdict(float)
        category_counts = defaultdict(int)
        
        for txn in transactions:
            if txn.get("type") == "debit":
                category = txn.get("category", "Other")
                amount = abs(float(txn.get("amount", 0)))
                category_spending[category] += amount
                category_counts[category] += 1
        
        # Find dominant categories
        total_spending = sum(category_spending.values())
        dominant_categories = []
        
        for category, amount in sorted(category_spending.items(), key=lambda x: x[1], reverse=True)[:3]:
            percentage = (amount / total_spending * 100) if total_spending > 0 else 0
            dominant_categories.append({
                "category": category,
                "amount": amount,
                "percentage": round(percentage, 1),
                "frequency": category_counts[category]
            })
        
        # Detect spending behavior
        amounts = [abs(float(txn.get("amount", 0))) for txn in transactions if txn.get("type") == "debit"]
        
        if amounts:
            avg_transaction = np.mean(amounts)
            std_transaction = np.std(amounts)
            cv = std_transaction / avg_transaction if avg_transaction > 0 else 0
            
            if cv > 0.8:
                behavior = "highly_variable"
            elif cv > 0.4:
                behavior = "moderately_variable"
            else:
                behavior = "consistent"
        else:
            behavior = "no_data"
        
        return {
            "dominant_categories": dominant_categories,
            "spending_behavior": behavior,
            "average_transaction": float(np.mean(amounts)) if amounts else 0,
            "total_transactions": len([t for t in transactions if t.get("type") == "debit"])
        }
    
    def _detect_income_patterns(self, transactions: List[Dict]) -> Dict:
        """Detect income patterns"""
        income_txns = [t for t in transactions if t.get("type") == "credit"]
        
        if not income_txns:
            return {"pattern": "no_income_data"}
        
        # Group by month
        monthly_income = defaultdict(float)
        
        for txn in income_txns:
            date_str = txn.get("date", "")
            if date_str:
                month = date_str[:7]  # YYYY-MM
                amount = float(txn.get("amount", 0))
                monthly_income[month] += amount
        
        # Calculate statistics
        income_values = list(monthly_income.values())
        
        if income_values:
            avg_income = np.mean(income_values)
            std_income = np.std(income_values)
            cv = std_income / avg_income if avg_income > 0 else 0
            
            if cv < 0.1:
                stability = "very_stable"
            elif cv < 0.2:
                stability = "stable"
            elif cv < 0.4:
                stability = "moderately_stable"
            else:
                stability = "variable"
        else:
            stability = "unknown"
            avg_income = 0
        
        return {
            "stability": stability,
            "average_monthly_income": float(avg_income) if income_values else 0,
            "income_sources": len(set(txn.get("description", "") for txn in income_txns)),
            "months_tracked": len(monthly_income)
        }
    
    def _detect_recurring_transactions(self, transactions: List[Dict]) -> List[Dict]:
        """Detect recurring transactions (subscriptions, EMIs, etc.)"""
        # Group by description
        description_groups = defaultdict(list)
        
        for txn in transactions:
            desc = txn.get("description", "").lower()
            if desc:
                description_groups[desc].append(txn)
        
        recurring = []
        
        for desc, txns in description_groups.items():
            if len(txns) >= 2:
                amounts = [abs(float(t.get("amount", 0))) for t in txns]
                avg_amount = np.mean(amounts)
                std_amount = np.std(amounts)
                
                # If amounts are similar, likely recurring
                if std_amount < avg_amount * 0.1:
                    recurring.append({
                        "description": desc,
                        "frequency": len(txns),
                        "average_amount": float(avg_amount),
                        "type": txns[0].get("type", ""),
                        "category": txns[0].get("category", ""),
                        "likely_subscription": "subscription" in desc or "emi" in desc or "premium" in desc
                    })
        
        # Sort by frequency
        recurring.sort(key=lambda x: x["frequency"], reverse=True)
        
        return recurring[:10]  # Top 10 recurring
    
    def _detect_seasonal_patterns(self, transactions: List[Dict]) -> Dict:
        """Detect seasonal spending patterns"""
        # Group by month
        monthly_spending = defaultdict(float)
        
        for txn in transactions:
            if txn.get("type") == "debit":
                date_str = txn.get("date", "")
                if date_str and len(date_str) >= 7:
                    month_num = int(date_str[5:7])  # Extract month number
                    amount = abs(float(txn.get("amount", 0)))
                    monthly_spending[month_num] += amount
        
        if not monthly_spending:
            return {"pattern": "insufficient_data"}
        
        # Find peak months
        peak_months = sorted(monthly_spending.items(), key=lambda x: x[1], reverse=True)[:3]
        
        month_names = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December"
        }
        
        peak_info = [
            {
                "month": month_names.get(month, "Unknown"),
                "spending": amount
            }
            for month, amount in peak_months
        ]
        
        return {
            "peak_spending_months": peak_info,
            "has_seasonal_pattern": len(set(monthly_spending.values())) > 1
        }
    
    def _detect_unusual_activity(self, transactions: List[Dict]) -> List[Dict]:
        """Detect unusual transactions"""
        if not transactions:
            return []
        
        # Calculate baseline
        amounts = [abs(float(t.get("amount", 0))) for t in transactions if t.get("type") == "debit"]
        
        if not amounts:
            return []
        
        mean_amount = np.mean(amounts)
        std_amount = np.std(amounts)
        
        unusual = []
        
        for txn in transactions:
            if txn.get("type") == "debit":
                amount = abs(float(txn.get("amount", 0)))
                z_score = (amount - mean_amount) / std_amount if std_amount > 0 else 0
                
                if abs(z_score) > 2.5:  # More than 2.5 standard deviations
                    unusual.append({
                        "date": txn.get("date", ""),
                        "description": txn.get("description", ""),
                        "amount": amount,
                        "category": txn.get("category", ""),
                        "z_score": float(z_score),
                        "severity": "high" if abs(z_score) > 3 else "medium"
                    })
        
        # Sort by z-score
        unusual.sort(key=lambda x: abs(x["z_score"]), reverse=True)
        
        return unusual[:5]  # Top 5 unusual transactions
    
    def _detect_lifestyle_indicators(self, transactions: List[Dict]) -> Dict:
        """Detect lifestyle indicators from spending"""
        category_spending = defaultdict(float)
        
        for txn in transactions:
            if txn.get("type") == "debit":
                category = txn.get("category", "Other")
                amount = abs(float(txn.get("amount", 0)))
                category_spending[category] += amount
        
        total = sum(category_spending.values())
        
        if total == 0:
            return {"lifestyle": "unknown"}
        
        # Calculate percentages
        percentages = {cat: (amt / total * 100) for cat, amt in category_spending.items()}
        
        # Determine lifestyle
        lifestyle_indicators = []
        
        if percentages.get("Dining", 0) > 15:
            lifestyle_indicators.append("foodie")
        
        if percentages.get("Shopping", 0) > 20:
            lifestyle_indicators.append("shopper")
        
        if percentages.get("Travel", 0) > 10:
            lifestyle_indicators.append("traveler")
        
        if percentages.get("Entertainment", 0) > 10:
            lifestyle_indicators.append("entertainment_lover")
        
        if percentages.get("Health", 0) > 8:
            lifestyle_indicators.append("health_conscious")
        
        # Determine financial personality
        if percentages.get("Savings", 0) > 20:
            personality = "saver"
        elif percentages.get("Investment", 0) > 15:
            personality = "investor"
        elif sum(percentages.get(cat, 0) for cat in ["Dining", "Shopping", "Entertainment"]) > 40:
            personality = "spender"
        else:
            personality = "balanced"
        
        return {
            "lifestyle_indicators": lifestyle_indicators,
            "financial_personality": personality,
            "top_spending_categories": sorted(
                [{"category": cat, "percentage": round(pct, 1)} 
                 for cat, pct in percentages.items()],
                key=lambda x: x["percentage"],
                reverse=True
            )[:5]
        }


# Global instance
pattern_detector = PatternDetector()
