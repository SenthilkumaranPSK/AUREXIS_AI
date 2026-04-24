"""
AUREXIS AI — Tax Planning & Optimization
Smart tax planning, deduction recommendations, and tax-saving strategies
"""

import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger("aurexis")


class TaxPlanner:
    """Intelligent tax planning and optimization"""
    
    # Indian Income Tax Slabs 2026-27 (New Regime)
    TAX_SLABS_NEW = [
        (300000, 0),      # Up to 3L - 0%
        (600000, 5),      # 3L to 6L - 5%
        (900000, 10),     # 6L to 9L - 10%
        (1200000, 15),    # 9L to 12L - 15%
        (1500000, 20),    # 12L to 15L - 20%
        (float('inf'), 30) # Above 15L - 30%
    ]
    
    # Old Regime (with deductions)
    TAX_SLABS_OLD = [
        (250000, 0),      # Up to 2.5L - 0%
        (500000, 5),      # 2.5L to 5L - 5%
        (1000000, 20),    # 5L to 10L - 20%
        (float('inf'), 30) # Above 10L - 30%
    ]
    
    def calculate_tax_liability(
        self,
        annual_income: float,
        regime: str = "new",
        deductions: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Calculate tax liability under new or old regime
        """
        if regime == "new":
            taxable_income = annual_income
            slabs = self.TAX_SLABS_NEW
            standard_deduction = 50000  # Standard deduction in new regime
        else:
            # Old regime with deductions
            total_deductions = sum(deductions.values()) if deductions else 0
            taxable_income = max(0, annual_income - total_deductions)
            slabs = self.TAX_SLABS_OLD
            standard_deduction = 50000
        
        # Apply standard deduction
        taxable_income = max(0, taxable_income - standard_deduction)
        
        # Calculate tax
        tax = 0
        previous_limit = 0
        
        for limit, rate in slabs:
            if taxable_income > previous_limit:
                taxable_in_slab = min(taxable_income, limit) - previous_limit
                tax += taxable_in_slab * (rate / 100)
                previous_limit = limit
            else:
                break
        
        # Add cess (4%)
        cess = tax * 0.04
        total_tax = tax + cess
        
        # Calculate effective tax rate
        effective_rate = (total_tax / annual_income * 100) if annual_income > 0 else 0
        
        return {
            "annual_income": round(annual_income, 2),
            "taxable_income": round(taxable_income, 2),
            "standard_deduction": standard_deduction,
            "total_deductions": round(sum(deductions.values()) if deductions else 0, 2),
            "tax_before_cess": round(tax, 2),
            "cess": round(cess, 2),
            "total_tax": round(total_tax, 2),
            "effective_tax_rate": round(effective_rate, 2),
            "monthly_tax": round(total_tax / 12, 2),
            "take_home_annual": round(annual_income - total_tax, 2),
            "take_home_monthly": round((annual_income - total_tax) / 12, 2)
        }
    
    def compare_tax_regimes(
        self,
        annual_income: float,
        potential_deductions: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Compare tax liability between old and new regime
        """
        # Calculate under new regime
        new_regime = self.calculate_tax_liability(annual_income, regime="new")
        
        # Calculate under old regime with deductions
        old_regime = self.calculate_tax_liability(
            annual_income,
            regime="old",
            deductions=potential_deductions
        )
        
        # Calculate savings
        savings = old_regime["total_tax"] - new_regime["total_tax"]
        better_regime = "new" if savings > 0 else "old"
        
        return {
            "annual_income": annual_income,
            "new_regime": new_regime,
            "old_regime": old_regime,
            "tax_savings": abs(round(savings, 2)),
            "better_regime": better_regime,
            "recommendation": self._generate_regime_recommendation(
                annual_income,
                new_regime,
                old_regime,
                potential_deductions
            )
        }
    
    def suggest_tax_saving_investments(
        self,
        annual_income: float,
        current_investments: Dict[str, float],
        risk_profile: str = "moderate"
    ) -> Dict[str, Any]:
        """
        Suggest tax-saving investment options under Section 80C, 80D, etc.
        """
        # Maximum deduction limits
        section_80c_limit = 150000
        section_80d_limit = 25000  # Health insurance
        section_80ccd1b_limit = 50000  # NPS additional
        
        # Current investments
        current_80c = current_investments.get("80C", 0)
        current_80d = current_investments.get("80D", 0)
        current_nps = current_investments.get("NPS", 0)
        
        # Calculate remaining capacity
        remaining_80c = max(0, section_80c_limit - current_80c)
        remaining_80d = max(0, section_80d_limit - current_80d)
        remaining_nps = max(0, section_80ccd1b_limit - current_nps)
        
        # Generate recommendations based on risk profile
        recommendations = []
        
        if remaining_80c > 0:
            if risk_profile == "conservative":
                recommendations.append({
                    "section": "80C",
                    "instrument": "PPF (Public Provident Fund)",
                    "amount": min(remaining_80c, 150000),
                    "returns": "7.1% (tax-free)",
                    "lock_in": "15 years",
                    "risk": "Very Low",
                    "tax_saved": round(min(remaining_80c, 150000) * 0.30, 2)
                })
            elif risk_profile == "moderate":
                recommendations.append({
                    "section": "80C",
                    "instrument": "ELSS (Equity Linked Savings Scheme)",
                    "amount": min(remaining_80c, 150000),
                    "returns": "12-15% (expected)",
                    "lock_in": "3 years",
                    "risk": "Medium",
                    "tax_saved": round(min(remaining_80c, 150000) * 0.30, 2)
                })
            else:  # aggressive
                recommendations.append({
                    "section": "80C",
                    "instrument": "ELSS + NPS Mix",
                    "amount": min(remaining_80c, 150000),
                    "returns": "13-16% (expected)",
                    "lock_in": "3 years (ELSS)",
                    "risk": "Medium-High",
                    "tax_saved": round(min(remaining_80c, 150000) * 0.30, 2)
                })
        
        if remaining_80d > 0:
            recommendations.append({
                "section": "80D",
                "instrument": "Health Insurance Premium",
                "amount": min(remaining_80d, 25000),
                "returns": "Health coverage + tax benefit",
                "lock_in": "Annual renewal",
                "risk": "None",
                "tax_saved": round(min(remaining_80d, 25000) * 0.30, 2)
            })
        
        if remaining_nps > 0:
            recommendations.append({
                "section": "80CCD(1B)",
                "instrument": "NPS (National Pension System)",
                "amount": min(remaining_nps, 50000),
                "returns": "10-12% (expected)",
                "lock_in": "Till retirement",
                "risk": "Low-Medium",
                "tax_saved": round(min(remaining_nps, 50000) * 0.30, 2)
            })
        
        # Calculate total potential savings
        total_investment_needed = remaining_80c + remaining_80d + remaining_nps
        total_tax_savings = sum(rec["tax_saved"] for rec in recommendations)
        
        return {
            "current_investments": current_investments,
            "remaining_capacity": {
                "80C": remaining_80c,
                "80D": remaining_80d,
                "80CCD(1B)": remaining_nps
            },
            "recommendations": recommendations,
            "total_investment_needed": round(total_investment_needed, 2),
            "total_tax_savings": round(total_tax_savings, 2),
            "monthly_investment": round(total_investment_needed / 12, 2),
            "roi_on_tax_savings": round((total_tax_savings / total_investment_needed * 100) if total_investment_needed > 0 else 0, 2)
        }
    
    def calculate_advance_tax(
        self,
        annual_income: float,
        regime: str = "new"
    ) -> Dict[str, Any]:
        """
        Calculate advance tax payment schedule
        """
        tax_liability = self.calculate_tax_liability(annual_income, regime)
        total_tax = tax_liability["total_tax"]
        
        # Advance tax schedule
        schedule = [
            {"due_date": "15-Jun-2026", "percentage": 15, "amount": round(total_tax * 0.15, 2)},
            {"due_date": "15-Sep-2026", "percentage": 45, "amount": round(total_tax * 0.45, 2)},
            {"due_date": "15-Dec-2026", "percentage": 75, "amount": round(total_tax * 0.75, 2)},
            {"due_date": "15-Mar-2027", "percentage": 100, "amount": round(total_tax, 2)},
        ]
        
        return {
            "total_tax_liability": round(total_tax, 2),
            "advance_tax_schedule": schedule,
            "interest_if_not_paid": "1% per month under Section 234B/234C",
            "exemption": "Not required if tax liability < ₹10,000"
        }
    
    def analyze_tax_efficiency(
        self,
        financial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze overall tax efficiency and provide optimization suggestions
        """
        # Extract income
        transactions = financial_data.get("fetch_bank_transactions", {}).get("transactions", [])
        
        # Calculate annual income
        monthly_income = 0
        income_count = 0
        for txn in transactions:
            if txn.get("type") == "credit" and txn.get("category") == "Salary":
                monthly_income += float(txn.get("amount", 0))
                income_count += 1
        
        if income_count > 0:
            monthly_income = monthly_income / income_count
        else:
            monthly_income = 80000  # Default
        
        annual_income = monthly_income * 12
        
        # Get current investments
        epf = financial_data.get("fetch_epf_details", {}).get("epfDetails", {})
        epf_contribution = epf.get("employeeContribution", 0) * 12
        
        current_investments = {
            "80C": epf_contribution,
            "80D": 0,
            "NPS": 0
        }
        
        # Calculate current tax
        current_tax = self.calculate_tax_liability(annual_income, regime="new")
        
        # Calculate optimized tax
        suggestions = self.suggest_tax_saving_investments(
            annual_income,
            current_investments,
            risk_profile="moderate"
        )
        
        # Calculate tax after optimization
        optimized_deductions = {
            "80C": 150000,
            "80D": 25000,
            "NPS": 50000
        }
        optimized_tax = self.calculate_tax_liability(
            annual_income,
            regime="old",
            deductions=optimized_deductions
        )
        
        # Calculate savings
        potential_savings = current_tax["total_tax"] - optimized_tax["total_tax"]
        
        return {
            "annual_income": round(annual_income, 2),
            "current_tax_liability": current_tax,
            "optimized_tax_liability": optimized_tax,
            "potential_tax_savings": round(potential_savings, 2),
            "tax_efficiency_score": round((1 - optimized_tax["effective_tax_rate"] / 100) * 100, 1),
            "investment_suggestions": suggestions,
            "quick_wins": self._generate_quick_wins(annual_income, current_investments)
        }
    
    def _generate_regime_recommendation(
        self,
        annual_income: float,
        new_regime: Dict,
        old_regime: Dict,
        deductions: Dict[str, float]
    ) -> str:
        """Generate recommendation for which regime to choose"""
        savings = old_regime["total_tax"] - new_regime["total_tax"]
        
        if savings > 50000:
            return f"Choose OLD regime. You'll save ₹{abs(savings):,.0f} with your current deductions."
        elif savings < -50000:
            return f"Choose NEW regime. You'll save ₹{abs(savings):,.0f} even without deductions."
        else:
            return "Both regimes are similar. Choose NEW regime for simplicity unless you plan to maximize deductions."
    
    def _generate_quick_wins(
        self,
        annual_income: float,
        current_investments: Dict[str, float]
    ) -> List[Dict[str, str]]:
        """Generate quick tax-saving wins"""
        quick_wins = []
        
        # 80C quick win
        if current_investments.get("80C", 0) < 150000:
            quick_wins.append({
                "action": "Maximize Section 80C",
                "investment": "₹1,50,000 in ELSS/PPF",
                "tax_saved": "₹45,000",
                "effort": "Low"
            })
        
        # 80D quick win
        if current_investments.get("80D", 0) < 25000:
            quick_wins.append({
                "action": "Buy Health Insurance",
                "investment": "₹25,000 premium",
                "tax_saved": "₹7,500",
                "effort": "Low"
            })
        
        # NPS quick win
        if current_investments.get("NPS", 0) < 50000:
            quick_wins.append({
                "action": "Invest in NPS",
                "investment": "₹50,000 additional",
                "tax_saved": "₹15,000",
                "effort": "Medium"
            })
        
        # HRA quick win
        quick_wins.append({
            "action": "Claim HRA Exemption",
            "investment": "Submit rent receipts",
            "tax_saved": "Up to ₹60,000",
            "effort": "Low"
        })
        
        return quick_wins


# Singleton instance
tax_planner = TaxPlanner()
