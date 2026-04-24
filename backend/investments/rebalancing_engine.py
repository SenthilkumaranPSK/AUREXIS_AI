"""
Rebalancing Engine
Generate portfolio rebalancing recommendations
"""

from typing import Dict, List, Tuple
from datetime import datetime, timedelta


class RebalancingEngine:
    """Generate portfolio rebalancing recommendations"""
    
    def __init__(self):
        self.rebalancing_threshold = 5.0  # 5% deviation triggers rebalancing
        self.min_trade_amount = 1000  # Minimum trade amount
    
    def analyze_rebalancing_need(
        self,
        current_allocation: Dict[str, float],
        target_allocation: Dict[str, float],
        portfolio_value: float
    ) -> Dict:
        """
        Analyze if rebalancing is needed
        
        Args:
            current_allocation: Current allocation percentages
            target_allocation: Target allocation percentages
            portfolio_value: Total portfolio value
            
        Returns:
            Rebalancing analysis
        """
        # Calculate deviations
        deviations = {}
        max_deviation = 0
        
        for asset in target_allocation.keys():
            current = current_allocation.get(asset, 0)
            target = target_allocation.get(asset, 0)
            deviation = current - target
            deviations[asset] = deviation
            max_deviation = max(max_deviation, abs(deviation))
        
        # Determine if rebalancing is needed
        needs_rebalancing = max_deviation > self.rebalancing_threshold
        
        # Generate recommendations
        recommendations = []
        if needs_rebalancing:
            recommendations = self._generate_rebalancing_trades(
                current_allocation,
                target_allocation,
                portfolio_value,
                deviations
            )
        
        # Calculate rebalancing benefit
        benefit = self._estimate_rebalancing_benefit(deviations, portfolio_value)
        
        return {
            "needs_rebalancing": needs_rebalancing,
            "max_deviation": round(max_deviation, 2),
            "deviations": {k: round(v, 2) for k, v in deviations.items()},
            "recommendations": recommendations,
            "estimated_benefit": benefit,
            "urgency": self._determine_urgency(max_deviation)
        }
    
    def _generate_rebalancing_trades(
        self,
        current_allocation: Dict[str, float],
        target_allocation: Dict[str, float],
        portfolio_value: float,
        deviations: Dict[str, float]
    ) -> List[Dict]:
        """Generate specific rebalancing trade recommendations"""
        trades = []
        
        # Calculate current and target amounts
        current_amounts = {
            asset: portfolio_value * (pct / 100)
            for asset, pct in current_allocation.items()
        }
        
        target_amounts = {
            asset: portfolio_value * (pct / 100)
            for asset, pct in target_allocation.items()
        }
        
        # Identify assets to sell (overweight) and buy (underweight)
        for asset in target_allocation.keys():
            current_amt = current_amounts.get(asset, 0)
            target_amt = target_amounts.get(asset, 0)
            difference = target_amt - current_amt
            
            if abs(difference) >= self.min_trade_amount:
                action = "buy" if difference > 0 else "sell"
                amount = abs(difference)
                
                trades.append({
                    "asset": asset,
                    "action": action,
                    "amount": round(amount, 2),
                    "current_allocation": round(current_allocation.get(asset, 0), 2),
                    "target_allocation": round(target_allocation.get(asset, 0), 2),
                    "deviation": round(deviations.get(asset, 0), 2),
                    "priority": self._calculate_trade_priority(deviations.get(asset, 0))
                })
        
        # Sort by priority
        trades.sort(key=lambda x: x["priority"], reverse=True)
        
        return trades
    
    def _calculate_trade_priority(self, deviation: float) -> int:
        """Calculate trade priority based on deviation"""
        abs_dev = abs(deviation)
        
        if abs_dev > 15:
            return 5  # Critical
        elif abs_dev > 10:
            return 4  # High
        elif abs_dev > 7:
            return 3  # Medium
        elif abs_dev > 5:
            return 2  # Low
        else:
            return 1  # Very low
    
    def _estimate_rebalancing_benefit(
        self,
        deviations: Dict[str, float],
        portfolio_value: float
    ) -> Dict:
        """Estimate the benefit of rebalancing"""
        # Calculate total deviation
        total_deviation = sum(abs(d) for d in deviations.values())
        
        # Estimate risk reduction (simplified)
        risk_reduction = min(total_deviation * 0.1, 5.0)  # Up to 5% risk reduction
        
        # Estimate return improvement (simplified)
        return_improvement = min(total_deviation * 0.05, 2.0)  # Up to 2% return improvement
        
        # Calculate potential value impact
        value_impact = portfolio_value * (return_improvement / 100)
        
        return {
            "risk_reduction_pct": round(risk_reduction, 2),
            "return_improvement_pct": round(return_improvement, 2),
            "estimated_value_impact": round(value_impact, 2),
            "benefit_level": "high" if total_deviation > 30 else "medium" if total_deviation > 15 else "low"
        }
    
    def _determine_urgency(self, max_deviation: float) -> str:
        """Determine rebalancing urgency"""
        if max_deviation > 15:
            return "high"
        elif max_deviation > 10:
            return "medium"
        elif max_deviation > 5:
            return "low"
        else:
            return "none"
    
    def generate_rebalancing_schedule(
        self,
        risk_tolerance: str,
        portfolio_volatility: float
    ) -> Dict:
        """
        Generate recommended rebalancing schedule
        
        Args:
            risk_tolerance: Risk tolerance level
            portfolio_volatility: Portfolio volatility
            
        Returns:
            Rebalancing schedule recommendation
        """
        # Determine frequency based on risk and volatility
        if risk_tolerance == "high" or portfolio_volatility > 15:
            frequency = "quarterly"
            months = 3
        elif risk_tolerance == "moderate":
            frequency = "semi-annual"
            months = 6
        else:
            frequency = "annual"
            months = 12
        
        # Calculate next rebalancing date
        next_date = datetime.now() + timedelta(days=30 * months)
        
        return {
            "recommended_frequency": frequency,
            "months_between": months,
            "next_rebalancing_date": next_date.strftime("%Y-%m-%d"),
            "rationale": self._get_frequency_rationale(frequency, risk_tolerance, portfolio_volatility)
        }
    
    def _get_frequency_rationale(
        self,
        frequency: str,
        risk_tolerance: str,
        volatility: float
    ) -> str:
        """Get rationale for rebalancing frequency"""
        if frequency == "quarterly":
            return f"Quarterly rebalancing recommended due to {'high risk tolerance' if risk_tolerance == 'high' else 'high portfolio volatility'}"
        elif frequency == "semi-annual":
            return "Semi-annual rebalancing provides good balance between costs and benefits"
        else:
            return "Annual rebalancing is sufficient for conservative portfolios"
    
    def calculate_tax_efficient_rebalancing(
        self,
        current_allocation: Dict[str, float],
        target_allocation: Dict[str, float],
        portfolio_value: float,
        cost_basis: Dict[str, float] = None,
        holding_period: Dict[str, int] = None
    ) -> Dict:
        """
        Generate tax-efficient rebalancing recommendations
        
        Args:
            current_allocation: Current allocation
            target_allocation: Target allocation
            portfolio_value: Portfolio value
            cost_basis: Cost basis for each asset
            holding_period: Holding period in months
            
        Returns:
            Tax-efficient rebalancing plan
        """
        # Standard rebalancing analysis
        standard_analysis = self.analyze_rebalancing_need(
            current_allocation,
            target_allocation,
            portfolio_value
        )
        
        if not standard_analysis["needs_rebalancing"]:
            return {
                "needs_rebalancing": False,
                "strategy": "no_action",
                "recommendations": []
            }
        
        # Tax-efficient strategies
        strategies = []
        
        # Strategy 1: Use new contributions
        strategies.append({
            "name": "new_contributions",
            "description": "Direct new contributions to underweight assets",
            "tax_impact": "none",
            "priority": 1
        })
        
        # Strategy 2: Rebalance in tax-advantaged accounts first
        strategies.append({
            "name": "tax_advantaged_first",
            "description": "Rebalance within retirement accounts to avoid taxes",
            "tax_impact": "none",
            "priority": 2
        })
        
        # Strategy 3: Harvest losses
        if cost_basis:
            loss_harvest_opportunities = []
            for asset, current_pct in current_allocation.items():
                current_value = portfolio_value * (current_pct / 100)
                basis = cost_basis.get(asset, current_value)
                
                if current_value < basis:
                    loss = basis - current_value
                    loss_harvest_opportunities.append({
                        "asset": asset,
                        "loss_amount": round(loss, 2)
                    })
            
            if loss_harvest_opportunities:
                strategies.append({
                    "name": "tax_loss_harvesting",
                    "description": "Sell assets with losses to offset gains",
                    "tax_impact": "beneficial",
                    "priority": 3,
                    "opportunities": loss_harvest_opportunities
                })
        
        # Strategy 4: Wait for long-term capital gains
        if holding_period:
            short_term_holdings = [
                asset for asset, months in holding_period.items()
                if months < 12
            ]
            
            if short_term_holdings:
                strategies.append({
                    "name": "wait_for_ltcg",
                    "description": f"Wait for long-term status on: {', '.join(short_term_holdings)}",
                    "tax_impact": "reduced",
                    "priority": 4
                })
        
        return {
            "needs_rebalancing": True,
            "strategy": "tax_efficient",
            "standard_recommendations": standard_analysis["recommendations"],
            "tax_efficient_strategies": strategies,
            "recommended_approach": "Use new contributions and tax-advantaged accounts first"
        }
    
    def simulate_rebalancing_impact(
        self,
        current_allocation: Dict[str, float],
        target_allocation: Dict[str, float],
        expected_returns: Dict[str, float],
        years: int = 5
    ) -> Dict:
        """
        Simulate the impact of rebalancing vs not rebalancing
        
        Args:
            current_allocation: Current allocation
            target_allocation: Target allocation
            expected_returns: Expected annual returns for each asset
            years: Simulation period
            
        Returns:
            Simulation results
        """
        initial_value = 100000  # Base amount
        
        # Simulate with rebalancing
        rebalanced_value = initial_value
        for year in range(years):
            # Apply returns based on target allocation
            year_return = sum(
                (target_allocation.get(asset, 0) / 100) * expected_returns.get(asset, 0)
                for asset in target_allocation.keys()
            )
            rebalanced_value *= (1 + year_return / 100)
        
        # Simulate without rebalancing
        unrebalanced_value = initial_value
        current_alloc = current_allocation.copy()
        for year in range(years):
            # Apply returns and let allocation drift
            year_return = sum(
                (current_alloc.get(asset, 0) / 100) * expected_returns.get(asset, 0)
                for asset in current_alloc.keys()
            )
            unrebalanced_value *= (1 + year_return / 100)
            
            # Update allocation based on different growth rates (simplified)
            total = sum(current_alloc.values())
            if total > 0:
                for asset in current_alloc.keys():
                    growth = 1 + expected_returns.get(asset, 0) / 100
                    current_alloc[asset] = (current_alloc[asset] * growth) / (total * growth / 100)
        
        # Calculate difference
        difference = rebalanced_value - unrebalanced_value
        difference_pct = (difference / unrebalanced_value) * 100
        
        return {
            "simulation_years": years,
            "initial_value": initial_value,
            "rebalanced_final_value": round(rebalanced_value, 2),
            "unrebalanced_final_value": round(unrebalanced_value, 2),
            "difference": round(difference, 2),
            "difference_pct": round(difference_pct, 2),
            "recommendation": "Rebalancing recommended" if difference > 0 else "Current allocation acceptable"
        }


# Global instance
rebalancing_engine = RebalancingEngine()
