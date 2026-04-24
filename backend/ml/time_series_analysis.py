"""
Time Series Analysis
Advanced time series analysis and decomposition
"""

import numpy as np
from typing import List, Dict, Tuple
from datetime import datetime


class TimeSeriesAnalyzer:
    """Advanced time series analysis"""
    
    def analyze(self, data: List[float], dates: List[str] = None) -> Dict:
        """
        Comprehensive time series analysis
        
        Args:
            data: Time series data
            dates: Optional dates for the data
            
        Returns:
            Dictionary with analysis results
        """
        if len(data) < 3:
            return self._minimal_analysis(data)
        
        # Decompose time series
        trend, seasonal, residual = self._decompose(data)
        
        # Detect anomalies
        anomalies = self._detect_anomalies(data)
        
        # Calculate statistics
        stats = self._calculate_statistics(data)
        
        # Detect patterns
        patterns = self._detect_patterns(data)
        
        # Calculate volatility
        volatility = self._calculate_volatility(data)
        
        return {
            "trend": trend,
            "seasonal": seasonal,
            "residual": residual,
            "anomalies": anomalies,
            "statistics": stats,
            "patterns": patterns,
            "volatility": volatility,
            "data_quality": self._assess_data_quality(data)
        }
    
    def _decompose(self, data: List[float]) -> Tuple[List[float], List[float], List[float]]:
        """Decompose time series into trend, seasonal, and residual"""
        n = len(data)
        
        # Calculate trend using moving average
        window = min(max(3, n // 4), 12)
        trend = self._moving_average(data, window)
        
        # Pad trend to match data length
        pad_size = (n - len(trend)) // 2
        trend = [trend[0]] * pad_size + trend + [trend[-1]] * (n - len(trend) - pad_size)
        
        # Calculate detrended data
        detrended = [data[i] - trend[i] for i in range(n)]
        
        # Detect seasonality (simplified)
        seasonal = self._detect_seasonality(detrended)
        
        # Calculate residual
        residual = [detrended[i] - seasonal[i] for i in range(n)]
        
        return trend, seasonal, residual
    
    def _moving_average(self, data: List[float], window: int) -> List[float]:
        """Calculate moving average"""
        result = []
        for i in range(len(data) - window + 1):
            avg = sum(data[i:i+window]) / window
            result.append(avg)
        return result
    
    def _detect_seasonality(self, data: List[float]) -> List[float]:
        """Detect seasonal component (simplified)"""
        n = len(data)
        
        # Try common periods (7, 30, 12 for daily, monthly, yearly)
        periods = [7, 12, 30]
        best_period = 12
        
        # For simplicity, use mean as seasonal component
        mean_val = np.mean(data)
        seasonal = [0] * n
        
        # Add simple seasonal pattern
        for i in range(n):
            seasonal[i] = (data[i] - mean_val) * 0.1
        
        return seasonal
    
    def _detect_anomalies(self, data: List[float]) -> List[Dict]:
        """Detect anomalies using statistical methods"""
        if len(data) < 3:
            return []
        
        mean = np.mean(data)
        std = np.std(data)
        
        anomalies = []
        threshold = 2.5  # 2.5 standard deviations
        
        for i, value in enumerate(data):
            z_score = abs((value - mean) / std) if std > 0 else 0
            
            if z_score > threshold:
                anomalies.append({
                    "index": i,
                    "value": value,
                    "z_score": float(z_score),
                    "severity": "high" if z_score > 3 else "medium",
                    "type": "spike" if value > mean else "dip"
                })
        
        return anomalies
    
    def _calculate_statistics(self, data: List[float]) -> Dict:
        """Calculate comprehensive statistics"""
        return {
            "mean": float(np.mean(data)),
            "median": float(np.median(data)),
            "std": float(np.std(data)),
            "min": float(np.min(data)),
            "max": float(np.max(data)),
            "range": float(np.max(data) - np.min(data)),
            "q1": float(np.percentile(data, 25)),
            "q3": float(np.percentile(data, 75)),
            "iqr": float(np.percentile(data, 75) - np.percentile(data, 25)),
            "skewness": self._calculate_skewness(data),
            "kurtosis": self._calculate_kurtosis(data)
        }
    
    def _calculate_skewness(self, data: List[float]) -> float:
        """Calculate skewness"""
        n = len(data)
        mean = np.mean(data)
        std = np.std(data)
        
        if std == 0:
            return 0.0
        
        skewness = sum(((x - mean) / std) ** 3 for x in data) / n
        return float(skewness)
    
    def _calculate_kurtosis(self, data: List[float]) -> float:
        """Calculate kurtosis"""
        n = len(data)
        mean = np.mean(data)
        std = np.std(data)
        
        if std == 0:
            return 0.0
        
        kurtosis = sum(((x - mean) / std) ** 4 for x in data) / n - 3
        return float(kurtosis)
    
    def _detect_patterns(self, data: List[float]) -> Dict:
        """Detect patterns in time series"""
        if len(data) < 3:
            return {"trend": "insufficient_data"}
        
        # Detect overall trend
        first_half = np.mean(data[:len(data)//2])
        second_half = np.mean(data[len(data)//2:])
        
        if second_half > first_half * 1.1:
            trend = "increasing"
        elif second_half < first_half * 0.9:
            trend = "decreasing"
        else:
            trend = "stable"
        
        # Detect volatility pattern
        volatility = np.std(data)
        mean = np.mean(data)
        cv = volatility / mean if mean != 0 else 0
        
        if cv > 0.3:
            volatility_pattern = "high"
        elif cv > 0.15:
            volatility_pattern = "medium"
        else:
            volatility_pattern = "low"
        
        # Detect cycles
        has_cycles = self._detect_cycles(data)
        
        return {
            "trend": trend,
            "volatility": volatility_pattern,
            "has_cycles": has_cycles,
            "coefficient_of_variation": float(cv)
        }
    
    def _detect_cycles(self, data: List[float]) -> bool:
        """Detect if data has cyclical patterns"""
        if len(data) < 6:
            return False
        
        # Simple cycle detection using autocorrelation
        mean = np.mean(data)
        variance = np.var(data)
        
        if variance == 0:
            return False
        
        # Calculate autocorrelation at lag 1
        autocorr = sum((data[i] - mean) * (data[i-1] - mean) for i in range(1, len(data))) / (len(data) * variance)
        
        # If autocorrelation is significant, likely has cycles
        return abs(autocorr) > 0.3
    
    def _calculate_volatility(self, data: List[float]) -> Dict:
        """Calculate volatility metrics"""
        if len(data) < 2:
            return {"volatility": 0, "volatility_trend": "stable"}
        
        # Calculate returns (percentage changes)
        returns = [(data[i] - data[i-1]) / data[i-1] if data[i-1] != 0 else 0 
                   for i in range(1, len(data))]
        
        # Calculate volatility (standard deviation of returns)
        volatility = float(np.std(returns)) if returns else 0
        
        # Calculate volatility trend
        if len(returns) >= 4:
            first_half_vol = np.std(returns[:len(returns)//2])
            second_half_vol = np.std(returns[len(returns)//2:])
            
            if second_half_vol > first_half_vol * 1.2:
                vol_trend = "increasing"
            elif second_half_vol < first_half_vol * 0.8:
                vol_trend = "decreasing"
            else:
                vol_trend = "stable"
        else:
            vol_trend = "stable"
        
        return {
            "volatility": volatility,
            "volatility_trend": vol_trend,
            "max_drawdown": self._calculate_max_drawdown(data),
            "sharpe_ratio": self._calculate_sharpe_ratio(returns) if returns else 0
        }
    
    def _calculate_max_drawdown(self, data: List[float]) -> float:
        """Calculate maximum drawdown"""
        if len(data) < 2:
            return 0.0
        
        peak = data[0]
        max_dd = 0
        
        for value in data:
            if value > peak:
                peak = value
            dd = (peak - value) / peak if peak > 0 else 0
            if dd > max_dd:
                max_dd = dd
        
        return float(max_dd)
    
    def _calculate_sharpe_ratio(self, returns: List[float], risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio"""
        if not returns or np.std(returns) == 0:
            return 0.0
        
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        
        # Annualize (assuming monthly data)
        annual_return = mean_return * 12
        annual_std = std_return * np.sqrt(12)
        
        sharpe = (annual_return - risk_free_rate) / annual_std if annual_std > 0 else 0
        return float(sharpe)
    
    def _assess_data_quality(self, data: List[float]) -> Dict:
        """Assess data quality"""
        n = len(data)
        
        # Check for missing values (represented as 0 or None)
        missing_count = sum(1 for x in data if x == 0)
        missing_pct = (missing_count / n * 100) if n > 0 else 0
        
        # Check for outliers
        if n >= 3:
            q1 = np.percentile(data, 25)
            q3 = np.percentile(data, 75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = sum(1 for x in data if x < lower_bound or x > upper_bound)
            outlier_pct = (outliers / n * 100) if n > 0 else 0
        else:
            outlier_pct = 0
        
        # Overall quality score
        quality_score = max(0, 100 - missing_pct - outlier_pct)
        
        return {
            "sample_size": n,
            "missing_percentage": float(missing_pct),
            "outlier_percentage": float(outlier_pct),
            "quality_score": float(quality_score),
            "quality_rating": "excellent" if quality_score > 90 else "good" if quality_score > 70 else "fair" if quality_score > 50 else "poor"
        }
    
    def _minimal_analysis(self, data: List[float]) -> Dict:
        """Minimal analysis for insufficient data"""
        if not data:
            return {"error": "No data provided"}
        
        return {
            "trend": [data[-1]] if data else [],
            "seasonal": [0] * len(data),
            "residual": [0] * len(data),
            "anomalies": [],
            "statistics": {
                "mean": float(np.mean(data)),
                "std": 0.0,
                "min": float(min(data)),
                "max": float(max(data))
            },
            "patterns": {"trend": "insufficient_data"},
            "volatility": {"volatility": 0, "volatility_trend": "stable"},
            "data_quality": {"quality_rating": "insufficient"}
        }


# Global instance
time_series_analyzer = TimeSeriesAnalyzer()
