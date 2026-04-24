"""
Confidence Interval Calculator
Statistical confidence intervals for predictions
"""

import numpy as np
from typing import List, Tuple, Dict
from scipy import stats


class ConfidenceIntervalCalculator:
    """Calculate confidence intervals for predictions"""
    
    def calculate(
        self,
        predictions: List[float],
        historical_errors: List[float] = None,
        confidence_level: float = 0.95
    ) -> Dict:
        """
        Calculate confidence intervals
        
        Args:
            predictions: Predicted values
            historical_errors: Historical prediction errors
            confidence_level: Confidence level (default 0.95 for 95% CI)
            
        Returns:
            Dictionary with lower and upper bounds
        """
        if not predictions:
            return {"lower": [], "upper": [], "width": []}
        
        if historical_errors and len(historical_errors) > 0:
            # Use historical errors to estimate uncertainty
            std_error = np.std(historical_errors)
        else:
            # Estimate from predictions
            std_error = np.std(predictions) * 0.1
        
        # Calculate z-score for confidence level
        z_score = stats.norm.ppf((1 + confidence_level) / 2)
        
        lower_bounds = []
        upper_bounds = []
        widths = []
        
        for i, pred in enumerate(predictions):
            # Increase uncertainty for future predictions
            uncertainty = std_error * (1 + i * 0.1)
            
            lower = pred - z_score * uncertainty
            upper = pred + z_score * uncertainty
            width = upper - lower
            
            lower_bounds.append(lower)
            upper_bounds.append(upper)
            widths.append(width)
        
        return {
            "lower": lower_bounds,
            "upper": upper_bounds,
            "width": widths,
            "confidence_level": confidence_level,
            "average_width": float(np.mean(widths))
        }
    
    def bootstrap_ci(
        self,
        data: List[float],
        statistic_func,
        n_bootstrap: int = 1000,
        confidence_level: float = 0.95
    ) -> Tuple[float, float]:
        """
        Calculate bootstrap confidence interval
        
        Args:
            data: Input data
            statistic_func: Function to calculate statistic
            n_bootstrap: Number of bootstrap samples
            confidence_level: Confidence level
            
        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        bootstrap_stats = []
        n = len(data)
        
        for _ in range(n_bootstrap):
            # Resample with replacement
            sample = np.random.choice(data, size=n, replace=True)
            stat = statistic_func(sample)
            bootstrap_stats.append(stat)
        
        # Calculate percentiles
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        lower = np.percentile(bootstrap_stats, lower_percentile)
        upper = np.percentile(bootstrap_stats, upper_percentile)
        
        return float(lower), float(upper)


# Global instance
confidence_calculator = ConfidenceIntervalCalculator()


# Global instance
confidence_interval_calculator = ConfidenceIntervalCalculator()
