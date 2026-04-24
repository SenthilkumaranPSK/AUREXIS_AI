"""
Ensemble Forecasting
Combines multiple forecasting models for better accuracy
"""

import numpy as np
from typing import List, Dict, Tuple
from datetime import datetime, timedelta


class EnsembleForecaster:
    """Ensemble forecasting using multiple models"""
    
    def __init__(self):
        self.models = ["arima", "lstm", "prophet", "linear"]
        self.weights = {
            "arima": 0.3,
            "lstm": 0.3,
            "prophet": 0.25,
            "linear": 0.15
        }
    
    def forecast(
        self,
        historical_data: List[float],
        steps: int = 6,
        include_confidence: bool = True
    ) -> Dict:
        """
        Generate ensemble forecast
        
        Args:
            historical_data: Historical values
            steps: Number of steps to forecast
            include_confidence: Include confidence intervals
            
        Returns:
            Dictionary with forecast and metadata
        """
        if len(historical_data) < 3:
            return self._fallback_forecast(historical_data, steps)
        
        # Generate forecasts from each model
        forecasts = {}
        forecasts["arima"] = self._arima_forecast(historical_data, steps)
        forecasts["lstm"] = self._lstm_forecast(historical_data, steps)
        forecasts["prophet"] = self._prophet_forecast(historical_data, steps)
        forecasts["linear"] = self._linear_forecast(historical_data, steps)
        
        # Combine forecasts using weighted average
        ensemble_forecast = self._weighted_average(forecasts)
        
        # Calculate confidence intervals
        if include_confidence:
            lower_bound, upper_bound = self._calculate_confidence_intervals(
                forecasts, ensemble_forecast
            )
        else:
            lower_bound = upper_bound = None
        
        # Calculate model agreement
        agreement_score = self._calculate_agreement(forecasts)
        
        return {
            "forecast": ensemble_forecast,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "confidence": agreement_score,
            "models_used": list(self.models),
            "model_weights": self.weights,
            "steps": steps
        }
    
    def _arima_forecast(self, data: List[float], steps: int) -> List[float]:
        """ARIMA-based forecast"""
        # Simplified ARIMA (in production, use statsmodels)
        if len(data) < 2:
            return [data[-1]] * steps
        
        # Calculate trend
        trend = (data[-1] - data[0]) / len(data)
        
        # Generate forecast
        forecast = []
        last_value = data[-1]
        for i in range(steps):
            next_value = last_value + trend
            forecast.append(next_value)
            last_value = next_value
        
        return forecast
    
    def _lstm_forecast(self, data: List[float], steps: int) -> List[float]:
        """LSTM-based forecast (simplified)"""
        # Simplified LSTM (in production, use TensorFlow/PyTorch)
        if len(data) < 3:
            return [data[-1]] * steps
        
        # Use exponential smoothing as proxy
        alpha = 0.3
        forecast = []
        last_value = data[-1]
        
        for i in range(steps):
            # Exponential smoothing
            next_value = alpha * last_value + (1 - alpha) * np.mean(data[-3:])
            forecast.append(next_value)
            last_value = next_value
        
        return forecast
    
    def _prophet_forecast(self, data: List[float], steps: int) -> List[float]:
        """Prophet-based forecast (simplified)"""
        # Simplified Prophet (in production, use fbprophet)
        if len(data) < 2:
            return [data[-1]] * steps
        
        # Detect seasonality and trend
        mean_value = np.mean(data)
        trend = (data[-1] - data[0]) / len(data)
        
        forecast = []
        last_value = data[-1]
        
        for i in range(steps):
            # Add trend and mean reversion
            next_value = last_value + trend * 0.5 + (mean_value - last_value) * 0.1
            forecast.append(next_value)
            last_value = next_value
        
        return forecast
    
    def _linear_forecast(self, data: List[float], steps: int) -> List[float]:
        """Linear regression forecast"""
        if len(data) < 2:
            return [data[-1]] * steps
        
        # Simple linear regression
        x = np.arange(len(data))
        y = np.array(data)
        
        # Calculate slope and intercept
        slope = np.cov(x, y)[0, 1] / np.var(x) if np.var(x) > 0 else 0
        intercept = np.mean(y) - slope * np.mean(x)
        
        # Generate forecast
        forecast = []
        for i in range(steps):
            next_x = len(data) + i
            next_value = slope * next_x + intercept
            forecast.append(next_value)
        
        return forecast
    
    def _weighted_average(self, forecasts: Dict[str, List[float]]) -> List[float]:
        """Calculate weighted average of forecasts"""
        steps = len(forecasts["arima"])
        ensemble = []
        
        for i in range(steps):
            weighted_sum = sum(
                forecasts[model][i] * self.weights[model]
                for model in self.models
            )
            ensemble.append(weighted_sum)
        
        return ensemble
    
    def _calculate_confidence_intervals(
        self,
        forecasts: Dict[str, List[float]],
        ensemble: List[float]
    ) -> Tuple[List[float], List[float]]:
        """Calculate confidence intervals"""
        steps = len(ensemble)
        lower_bound = []
        upper_bound = []
        
        for i in range(steps):
            # Get all model predictions for this step
            predictions = [forecasts[model][i] for model in self.models]
            
            # Calculate standard deviation
            std = np.std(predictions)
            
            # 95% confidence interval (±1.96 * std)
            lower = ensemble[i] - 1.96 * std
            upper = ensemble[i] + 1.96 * std
            
            lower_bound.append(lower)
            upper_bound.append(upper)
        
        return lower_bound, upper_bound
    
    def _calculate_agreement(self, forecasts: Dict[str, List[float]]) -> float:
        """Calculate model agreement score (0-1)"""
        steps = len(forecasts["arima"])
        agreement_scores = []
        
        for i in range(steps):
            predictions = [forecasts[model][i] for model in self.models]
            
            # Calculate coefficient of variation
            mean_pred = np.mean(predictions)
            std_pred = np.std(predictions)
            
            if mean_pred != 0:
                cv = std_pred / abs(mean_pred)
                # Convert to agreement score (lower CV = higher agreement)
                agreement = max(0, 1 - cv)
            else:
                agreement = 1.0
            
            agreement_scores.append(agreement)
        
        # Return average agreement
        return float(np.mean(agreement_scores))
    
    def _fallback_forecast(self, data: List[float], steps: int) -> Dict:
        """Fallback forecast for insufficient data"""
        if not data:
            forecast = [0] * steps
        else:
            forecast = [data[-1]] * steps
        
        return {
            "forecast": forecast,
            "lower_bound": forecast,
            "upper_bound": forecast,
            "confidence": 0.5,
            "models_used": ["fallback"],
            "model_weights": {"fallback": 1.0},
            "steps": steps
        }
    
    def evaluate_accuracy(
        self,
        historical_data: List[float],
        actual_values: List[float]
    ) -> Dict:
        """Evaluate forecast accuracy"""
        if len(historical_data) < 3 or len(actual_values) == 0:
            return {"error": "Insufficient data for evaluation"}
        
        # Generate forecast
        forecast_result = self.forecast(historical_data, len(actual_values), False)
        predicted = forecast_result["forecast"]
        
        # Calculate metrics
        mae = np.mean(np.abs(np.array(predicted) - np.array(actual_values)))
        mse = np.mean((np.array(predicted) - np.array(actual_values)) ** 2)
        rmse = np.sqrt(mse)
        
        # Calculate MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((np.array(actual_values) - np.array(predicted)) / np.array(actual_values))) * 100
        
        return {
            "mae": float(mae),
            "mse": float(mse),
            "rmse": float(rmse),
            "mape": float(mape),
            "accuracy": max(0, 100 - mape)
        }


# Global instance
ensemble_forecaster = EnsembleForecaster()
