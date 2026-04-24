"""
Portfolio Optimizer
Modern Portfolio Theory based optimization
"""

import numpy as np
from typing import Dict, List, Tuple, Any


class PortfolioOptimizer:
    """Optimize portfolio allocation using MPT"""
    
    def __init__(self):
        # Expected returns (annual %)
        self.expected_returns = {
            "equity": 12.0,
            "debt": 7.0,
            "gold": 8.0,
            "real_estate": 10.0,
            "cash": 4.0
        }
        
        # Risk (standard deviation %)
        self.risk = {
            "equity": 18.0,
            "debt": 5.0,
            "gold": 15.0,
            "real_estate": 12.0,
            "cash": 1.0
        }
        
        # Correlation matrix (simplified)
        self.correlations = {
            ("equity", "debt"): 0.2,
            ("equity", "gold"): 0.3,
            ("equity", "real_estate"): 0.6,
            ("debt", "gold"): 0.1,
            ("debt", "real_estate"): 0.3,
            ("gold", "real_estate"): 0.2
        }
    
    def optimize_portfolio(
        self,
        risk_tolerance: str,
        investment_amount: float,
        age: int,
        goals: List[Dict] = None
    ) -> Dict:
        """
        Optimize portfolio allocation
        
        Args:
            risk_tolerance: Risk tolerance level
            investment_amount: Amount to invest
            age: Investor age
            goals: Financial goals
            
        Returns:
            Optimized portfolio allocation
        """
        # Determine target allocation based on risk tolerance and age
        target_allocation = self._get_target_allocation(risk_tolerance, age)
        
        # Calculate expected portfolio metrics
        portfolio_return = self._calculate_portfolio_return(target_allocation)
        portfolio_risk = self._calculate_portfolio_risk(target_allocation)
        sharpe_ratio = self._calculate_sharpe_ratio(portfolio_return, portfolio_risk)
        
        # Generate allocation amounts
        allocation_amounts = {
            asset: investment_amount * (pct / 100)
            for asset, pct in target_allocation.items()
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            target_allocation,
            risk_tolerance,
            age
        )
        
        return {
            "target_allocation": target_allocation,
            "allocation_amounts": allocation_amounts,
            "expected_return": round(portfolio_return, 2),
            "expected_risk": round(portfolio_risk, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "recommendations": recommendations,
            "rebalancing_frequency": "quarterly"
        }
    
    def _get_target_allocation(self, risk_tolerance: str, age: int) -> Dict[str, float]:
        """Get target allocation based on risk tolerance and age"""
        # Rule of thumb: equity allocation = 100 - age (adjusted for risk tolerance)
        base_equity = max(20, min(80, 100 - age))
        
        # Adjust for risk tolerance
        if risk_tolerance == "very_low":
            equity_pct = base_equity * 0.5
        elif risk_tolerance == "low":
            equity_pct = base_equity * 0.7
        elif risk_tolerance == "moderate":
            equity_pct = base_equity
        else:  # high
            equity_pct = min(80, base_equity * 1.2)
        
        # Allocate remaining to other assets
        remaining = 100 - equity_pct
        
        allocation = {
            "equity": round(equity_pct, 1),
            "debt": round(remaining * 0.5, 1),
            "gold": round(remaining * 0.2, 1),
            "real_estate": round(remaining * 0.2, 1),
            "cash": round(remaining * 0.1, 1)
        }
        
        # Ensure total is 100%
        total = sum(allocation.values())
        if total != 100:
            allocation["debt"] += (100 - total)
        
        return allocation
    
    def _calculate_portfolio_return(self, allocation: Dict[str, float]) -> float:
        """Calculate expected portfolio return"""
        return sum(
            (allocation.get(asset, 0) / 100) * self.expected_returns.get(asset, 0)
            for asset in allocation.keys()
        )
    
    def _calculate_portfolio_risk(self, allocation: Dict[str, float]) -> float:
        """Calculate portfolio risk (standard deviation)"""
        # Simplified calculation (in production, use covariance matrix)
        variance = sum(
            ((allocation.get(asset, 0) / 100) * self.risk.get(asset, 0)) ** 2
            for asset in allocation.keys()
        )
        
        # Add correlation effects (simplified)
        assets = list(allocation.keys())
        for i, asset1 in enumerate(assets):
            for asset2 in assets[i+1:]:
                w1 = allocation.get(asset1, 0) / 100
                w2 = allocation.get(asset2, 0) / 100
                corr = self.correlations.get((asset1, asset2), 0) or self.correlations.get((asset2, asset1), 0)
                variance += 2 * w1 * w2 * self.risk.get(asset1, 0) * self.risk.get(asset2, 0) * corr / 100
        
        return np.sqrt(variance)
    
    def _calculate_sharpe_ratio(self, return_pct: float, risk_pct: float, risk_free_rate: float = 4.0) -> float:
        """Calculate Sharpe ratio"""
        if risk_pct == 0:
            return 0
        return (return_pct - risk_free_rate) / risk_pct
    
    def _generate_recommendations(
        self,
        allocation: Dict[str, float],
        risk_tolerance: str,
        age: int
    ) -> List[str]:
        """Generate investment recommendations"""
        recommendations = []
        
        equity_pct = allocation.get("equity", 0)
        
        if equity_pct > 60:
            recommendations.append("Consider diversified equity mutual funds or index funds")
            recommendations.append("Include both large-cap and mid-cap funds for balance")
        elif equity_pct > 40:
            recommendations.append("Balanced allocation - mix of equity and debt funds")
            recommendations.append("Consider hybrid funds for automatic rebalancing")
        else:
            recommendations.append("Conservative allocation - focus on debt and stable instruments")
            recommendations.append("Consider debt mutual funds and fixed deposits")
        
        if allocation.get("gold", 0) > 0:
            recommendations.append("Invest in gold through Gold ETFs or Sovereign Gold Bonds")
        
        if age < 35:
            recommendations.append("You have time on your side - stay invested for long term")
        elif age > 50:
            recommendations.append("Gradually shift to more stable investments as you near retirement")
        
        return recommendations
    
    def calculate_efficient_frontier(
        self,
        min_return: float = 5.0,
        max_return: float = 15.0,
        steps: int = 10
    ) -> List[Dict]:
        """Calculate efficient frontier points"""
        frontier = []
        
        for target_return in np.linspace(min_return, max_return, steps):
            # Find allocation that achieves target return with minimum risk
            # Simplified - in production, use optimization library
            
            # Estimate equity allocation needed for target return
            equity_pct = (target_return - self.expected_returns["debt"]) / \
                        (self.expected_returns["equity"] - self.expected_returns["debt"]) * 100
            
            equity_pct = max(0, min(100, equity_pct))
            
            allocation = {
                "equity": equity_pct,
                "debt": 100 - equity_pct,
                "gold": 0,
                "real_estate": 0,
                "cash": 0
            }
            
            portfolio_return = self._calculate_portfolio_return(allocation)
            portfolio_risk = self._calculate_portfolio_risk(allocation)
            
            frontier.append({
                "return": round(portfolio_return, 2),
                "risk": round(portfolio_risk, 2),
                "allocation": allocation
            })
        
        return frontier


# Global instance
portfolio_optimizer = PortfolioOptimizer()
