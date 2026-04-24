"""
Risk Calculator
Calculate investment risk metrics
"""

import numpy as np
from typing import Dict, List, Tuple


class RiskCalculator:
    """Calculate various risk metrics for investments"""
    
    def __init__(self):
        # Historical volatility data (annual %)
        self.asset_volatility = {
            "equity": 18.0,
            "debt": 5.0,
            "gold": 15.0,
            "real_estate": 12.0,
            "cash": 1.0
        }
        
        # Correlation matrix
        self.correlations = {
            ("equity", "debt"): 0.2,
            ("equity", "gold"): 0.3,
            ("equity", "real_estate"): 0.6,
            ("equity", "cash"): 0.0,
            ("debt", "gold"): 0.1,
            ("debt", "real_estate"): 0.3,
            ("debt", "cash"): 0.1,
            ("gold", "real_estate"): 0.2,
            ("gold", "cash"): 0.0,
            ("real_estate", "cash"): 0.0
        }
    
    def calculate_portfolio_risk(self, allocation: Dict[str, float]) -> Dict:
        """
        Calculate comprehensive portfolio risk metrics
        
        Args:
            allocation: Asset allocation percentages
            
        Returns:
            Risk metrics dictionary
        """
        # Portfolio volatility
        volatility = self._calculate_portfolio_volatility(allocation)
        
        # Value at Risk (VaR)
        var_95 = self._calculate_var(allocation, confidence=0.95)
        var_99 = self._calculate_var(allocation, confidence=0.99)
        
        # Diversification ratio
        diversification = self._calculate_diversification_ratio(allocation)
        
        # Risk concentration
        concentration = self._calculate_concentration_risk(allocation)
        
        # Maximum drawdown estimate
        max_drawdown = self._estimate_max_drawdown(allocation)
        
        return {
            "portfolio_volatility": round(volatility, 2),
            "var_95": round(var_95, 2),
            "var_99": round(var_99, 2),
            "diversification_ratio": round(diversification, 2),
            "concentration_risk": concentration,
            "estimated_max_drawdown": round(max_drawdown, 2),
            "risk_level": self._determine_risk_level(volatility)
        }
    
    def _calculate_portfolio_volatility(self, allocation: Dict[str, float]) -> float:
        """Calculate portfolio standard deviation"""
        # Convert percentages to weights
        weights = {asset: pct / 100 for asset, pct in allocation.items()}
        
        # Calculate variance
        variance = 0
        
        # Individual asset variances
        for asset, weight in weights.items():
            vol = self.asset_volatility.get(asset, 10.0)
            variance += (weight * vol) ** 2
        
        # Covariance terms
        assets = list(weights.keys())
        for i, asset1 in enumerate(assets):
            for asset2 in assets[i+1:]:
                w1 = weights[asset1]
                w2 = weights[asset2]
                vol1 = self.asset_volatility.get(asset1, 10.0)
                vol2 = self.asset_volatility.get(asset2, 10.0)
                
                # Get correlation
                corr = self.correlations.get((asset1, asset2), 0)
                if corr == 0:
                    corr = self.correlations.get((asset2, asset1), 0)
                
                variance += 2 * w1 * w2 * vol1 * vol2 * corr
        
        return np.sqrt(variance)
    
    def _calculate_var(
        self,
        allocation: Dict[str, float],
        confidence: float = 0.95,
        investment_amount: float = 100000
    ) -> float:
        """
        Calculate Value at Risk (VaR)
        
        Args:
            allocation: Asset allocation
            confidence: Confidence level (0.95 or 0.99)
            investment_amount: Portfolio value
            
        Returns:
            VaR amount (potential loss)
        """
        volatility = self._calculate_portfolio_volatility(allocation)
        
        # Z-score for confidence level
        z_scores = {0.95: 1.645, 0.99: 2.326}
        z = z_scores.get(confidence, 1.645)
        
        # VaR calculation (assuming normal distribution)
        var = investment_amount * (volatility / 100) * z / np.sqrt(12)  # Monthly VaR
        
        return var
    
    def _calculate_diversification_ratio(self, allocation: Dict[str, float]) -> float:
        """
        Calculate diversification ratio
        Higher is better (1.0 = no diversification, >1.0 = diversified)
        """
        weights = {asset: pct / 100 for asset, pct in allocation.items()}
        
        # Weighted average volatility
        weighted_vol = sum(
            weights[asset] * self.asset_volatility.get(asset, 10.0)
            for asset in weights.keys()
        )
        
        # Portfolio volatility
        portfolio_vol = self._calculate_portfolio_volatility(allocation)
        
        if portfolio_vol == 0:
            return 1.0
        
        return weighted_vol / portfolio_vol
    
    def _calculate_concentration_risk(self, allocation: Dict[str, float]) -> str:
        """Assess concentration risk"""
        max_allocation = max(allocation.values()) if allocation else 0
        
        # Count significant allocations (>10%)
        significant_assets = sum(1 for pct in allocation.values() if pct > 10)
        
        if max_allocation > 70:
            return "high"
        elif max_allocation > 50:
            return "medium-high"
        elif significant_assets >= 4:
            return "low"
        elif significant_assets >= 3:
            return "medium-low"
        else:
            return "medium"
    
    def _estimate_max_drawdown(self, allocation: Dict[str, float]) -> float:
        """Estimate maximum drawdown based on historical data"""
        # Historical max drawdowns (%)
        max_drawdowns = {
            "equity": -50.0,
            "debt": -10.0,
            "gold": -30.0,
            "real_estate": -35.0,
            "cash": 0.0
        }
        
        # Weighted average of max drawdowns
        weights = {asset: pct / 100 for asset, pct in allocation.items()}
        
        estimated_drawdown = sum(
            weights[asset] * max_drawdowns.get(asset, -20.0)
            for asset in weights.keys()
        )
        
        # Adjust for diversification benefit
        diversification_ratio = self._calculate_diversification_ratio(allocation)
        if diversification_ratio > 1.0:
            estimated_drawdown *= 0.8  # 20% reduction for diversification
        
        return estimated_drawdown
    
    def _determine_risk_level(self, volatility: float) -> str:
        """Determine risk level based on volatility"""
        if volatility < 5:
            return "very_low"
        elif volatility < 10:
            return "low"
        elif volatility < 15:
            return "moderate"
        elif volatility < 20:
            return "high"
        else:
            return "very_high"
    
    def calculate_risk_adjusted_return(
        self,
        expected_return: float,
        volatility: float,
        risk_free_rate: float = 4.0
    ) -> Dict:
        """
        Calculate risk-adjusted return metrics
        
        Args:
            expected_return: Expected annual return (%)
            volatility: Portfolio volatility (%)
            risk_free_rate: Risk-free rate (%)
            
        Returns:
            Risk-adjusted metrics
        """
        # Sharpe Ratio
        sharpe = (expected_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        # Sortino Ratio (simplified - using volatility as proxy for downside deviation)
        downside_vol = volatility * 0.7  # Approximate downside volatility
        sortino = (expected_return - risk_free_rate) / downside_vol if downside_vol > 0 else 0
        
        # Treynor Ratio (simplified - assuming beta = 1 for equity portion)
        treynor = expected_return - risk_free_rate
        
        return {
            "sharpe_ratio": round(sharpe, 2),
            "sortino_ratio": round(sortino, 2),
            "treynor_ratio": round(treynor, 2),
            "risk_adjusted_return": round(expected_return / volatility, 2) if volatility > 0 else 0
        }
    
    def assess_risk_capacity(
        self,
        age: int,
        income: float,
        expenses: float,
        dependents: int = 0,
        emergency_fund_months: float = 0
    ) -> Dict:
        """
        Assess investor's risk capacity
        
        Args:
            age: Investor age
            income: Monthly income
            expenses: Monthly expenses
            dependents: Number of dependents
            emergency_fund_months: Emergency fund coverage
            
        Returns:
            Risk capacity assessment
        """
        score = 50  # Base score
        
        # Age factor (younger = higher capacity)
        if age < 30:
            score += 20
        elif age < 40:
            score += 10
        elif age > 55:
            score -= 15
        elif age > 65:
            score -= 25
        
        # Income stability
        if income > expenses * 2:
            score += 15
        elif income < expenses * 1.2:
            score -= 15
        
        # Dependents
        score -= dependents * 5
        
        # Emergency fund
        if emergency_fund_months >= 6:
            score += 15
        elif emergency_fund_months >= 3:
            score += 5
        elif emergency_fund_months < 1:
            score -= 20
        
        # Normalize to 0-100
        score = max(0, min(100, score))
        
        # Determine capacity level
        if score >= 75:
            capacity = "high"
            recommendation = "You can afford to take higher investment risks"
        elif score >= 50:
            capacity = "moderate"
            recommendation = "A balanced approach to risk is suitable"
        elif score >= 25:
            capacity = "low"
            recommendation = "Focus on conservative investments"
        else:
            capacity = "very_low"
            recommendation = "Prioritize capital preservation and emergency fund"
        
        return {
            "risk_capacity_score": score,
            "capacity_level": capacity,
            "recommendation": recommendation,
            "factors": {
                "age_factor": "favorable" if age < 40 else "limiting",
                "income_factor": "strong" if income > expenses * 1.5 else "adequate",
                "emergency_fund": "adequate" if emergency_fund_months >= 3 else "insufficient"
            }
        }
    
    def calculate_beta(
        self,
        asset_returns: List[float],
        market_returns: List[float]
    ) -> float:
        """
        Calculate beta (systematic risk)
        
        Args:
            asset_returns: Asset return series
            market_returns: Market return series
            
        Returns:
            Beta value
        """
        if len(asset_returns) != len(market_returns) or len(asset_returns) < 2:
            return 1.0  # Default beta
        
        # Calculate covariance and variance
        asset_mean = np.mean(asset_returns)
        market_mean = np.mean(market_returns)
        
        covariance = np.mean([
            (asset_returns[i] - asset_mean) * (market_returns[i] - market_mean)
            for i in range(len(asset_returns))
        ])
        
        market_variance = np.var(market_returns)
        
        if market_variance == 0:
            return 1.0
        
        beta = covariance / market_variance
        return round(beta, 2)


# Global instance
risk_calculator = RiskCalculator()
