"""
ML Forecasting Routes
API endpoints for ensemble forecasting and time series analysis
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List, Optional
from datetime import datetime

from auth.dependencies import get_current_user
from database_legacy import User
from models.financial import FinancialModel
from ml.ensemble_forecasting import ensemble_forecaster
from ml.time_series_analysis import time_series_analyzer
from ml.confidence_intervals import confidence_interval_calculator

router = APIRouter(prefix="/api/ml", tags=["ML Forecasting"])


@router.post("/ensemble-forecast")
async def ensemble_forecast(
    metric: str,
    steps: int = 6,
    include_confidence: bool = True,
    current_user: User = Depends(get_current_user)
):
    """
    Generate ensemble forecast
    
    Args:
        metric: Metric to forecast (net_worth, income, expenses)
        steps: Number of periods to forecast
        include_confidence: Include confidence intervals
        current_user: Authenticated user
        
    Returns:
        Ensemble forecast results
    """
    try:
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=24  # 2 years of data
        )
        
        if not historical_data or len(historical_data) < 6:
            raise HTTPException(
                status_code=400,
                detail="Insufficient historical data for forecasting (minimum 6 months required)"
            )
        
        # Extract metric values
        historical_values = [d.get(metric, 0) for d in historical_data]
        
        # Generate ensemble forecast
        forecast_result = ensemble_forecaster.forecast(
            historical_data=historical_values,
            steps=steps,
            include_confidence=include_confidence
        )
        
        return {
            "success": True,
            "metric": metric,
            "forecast": forecast_result,
            "historical_data_points": len(historical_values),
            "forecast_steps": steps,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/time-series-analysis")
async def analyze_time_series(
    metric: str,
    current_user: User = Depends(get_current_user)
):
    """
    Perform comprehensive time series analysis
    
    Args:
        metric: Metric to analyze
        current_user: Authenticated user
        
    Returns:
        Time series analysis results
    """
    try:
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=24
        )
        
        if not historical_data or len(historical_data) < 12:
            raise HTTPException(
                status_code=400,
                detail="Insufficient data for time series analysis (minimum 12 months required)"
            )
        
        # Extract metric values
        values = [d.get(metric, 0) for d in historical_data]
        
        # Perform analysis
        analysis = time_series_analyzer.analyze(values)
        
        return {
            "success": True,
            "metric": metric,
            "analysis": analysis,
            "data_points": len(values),
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forecast-accuracy")
async def evaluate_forecast_accuracy(
    metric: str,
    forecast_months: int = 3,
    current_user: User = Depends(get_current_user)
):
    """
    Evaluate forecast accuracy by comparing past forecasts with actual values
    
    Args:
        metric: Metric to evaluate
        forecast_months: Number of months to forecast
        current_user: Authenticated user
        
    Returns:
        Forecast accuracy metrics
    """
    try:
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=24
        )
        
        if not historical_data or len(historical_data) < 12 + forecast_months:
            raise HTTPException(
                status_code=400,
                detail="Insufficient data for accuracy evaluation"
            )
        
        # Split data: use older data for training, recent data for validation
        train_data = [d.get(metric, 0) for d in historical_data[forecast_months:]]
        actual_data = [d.get(metric, 0) for d in historical_data[:forecast_months]]
        
        # Generate forecast
        forecast_result = ensemble_forecaster.forecast(
            historical_data=train_data,
            steps=forecast_months,
            include_confidence=False
        )
        
        forecast_values = forecast_result.get("forecast", [])
        
        # Evaluate accuracy
        accuracy = ensemble_forecaster.evaluate_forecast_accuracy(
            actual=actual_data,
            predicted=forecast_values
        )
        
        return {
            "success": True,
            "metric": metric,
            "accuracy_metrics": accuracy,
            "forecast_months": forecast_months,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect-anomalies")
async def detect_anomalies(
    metric: str,
    threshold: float = 2.0,
    current_user: User = Depends(get_current_user)
):
    """
    Detect anomalies in financial data
    
    Args:
        metric: Metric to analyze
        threshold: Z-score threshold for anomaly detection
        current_user: Authenticated user
        
    Returns:
        Detected anomalies
    """
    try:
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=12
        )
        
        if not historical_data or len(historical_data) < 6:
            raise HTTPException(
                status_code=400,
                detail="Insufficient data for anomaly detection"
            )
        
        # Extract metric values
        values = [d.get(metric, 0) for d in historical_data]
        
        # Detect anomalies
        anomalies = time_series_analyzer.detect_anomalies(
            data=values,
            threshold=threshold
        )
        
        # Add dates to anomalies
        anomalies_with_dates = []
        for anomaly in anomalies:
            idx = anomaly["index"]
            if idx < len(historical_data):
                anomaly["date"] = historical_data[idx].get("date", "")
                anomalies_with_dates.append(anomaly)
        
        return {
            "success": True,
            "metric": metric,
            "anomalies": anomalies_with_dates,
            "total_anomalies": len(anomalies_with_dates),
            "threshold": threshold,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/decompose")
async def decompose_time_series(
    metric: str,
    period: int = 12,
    current_user: User = Depends(get_current_user)
):
    """
    Decompose time series into trend, seasonal, and residual components
    
    Args:
        metric: Metric to decompose
        period: Seasonal period (default 12 for monthly data)
        current_user: Authenticated user
        
    Returns:
        Decomposition results
    """
    try:
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=24
        )
        
        if not historical_data or len(historical_data) < period * 2:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient data for decomposition (minimum {period * 2} months required)"
            )
        
        # Extract metric values
        values = [d.get(metric, 0) for d in historical_data]
        
        # Decompose
        decomposition = time_series_analyzer.decompose(
            data=values,
            period=period
        )
        
        return {
            "success": True,
            "metric": metric,
            "decomposition": decomposition,
            "period": period,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/volatility-analysis")
async def analyze_volatility(
    metric: str,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze volatility of a financial metric
    
    Args:
        metric: Metric to analyze
        current_user: Authenticated user
        
    Returns:
        Volatility analysis
    """
    try:
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=12
        )
        
        if not historical_data or len(historical_data) < 6:
            raise HTTPException(
                status_code=400,
                detail="Insufficient data for volatility analysis"
            )
        
        # Extract metric values
        values = [d.get(metric, 0) for d in historical_data]
        
        # Analyze volatility
        volatility = time_series_analyzer.calculate_volatility(values)
        
        return {
            "success": True,
            "metric": metric,
            "volatility_analysis": volatility,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/confidence-intervals")
async def calculate_confidence_intervals(
    metric: str,
    steps: int = 6,
    confidence_level: float = 0.95,
    current_user: User = Depends(get_current_user)
):
    """
    Calculate confidence intervals for forecasts
    
    Args:
        metric: Metric to forecast
        steps: Number of periods to forecast
        confidence_level: Confidence level (0.90, 0.95, or 0.99)
        current_user: Authenticated user
        
    Returns:
        Forecast with confidence intervals
    """
    try:
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=24
        )
        
        if not historical_data or len(historical_data) < 6:
            raise HTTPException(
                status_code=400,
                detail="Insufficient data for confidence interval calculation"
            )
        
        # Extract metric values
        values = [d.get(metric, 0) for d in historical_data]
        
        # Generate forecast
        forecast_result = ensemble_forecaster.forecast(
            historical_data=values,
            steps=steps,
            include_confidence=True
        )
        
        # Calculate bootstrap confidence intervals
        bootstrap_ci = confidence_interval_calculator.bootstrap_confidence_interval(
            data=values,
            n_bootstrap=1000,
            confidence_level=confidence_level
        )
        
        return {
            "success": True,
            "metric": metric,
            "forecast": forecast_result.get("forecast", []),
            "confidence_intervals": {
                "lower_bound": forecast_result.get("lower_bound", []),
                "upper_bound": forecast_result.get("upper_bound", []),
                "confidence_level": confidence_level
            },
            "bootstrap_ci": bootstrap_ci,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forecast-comparison")
async def compare_forecasts(
    metric: str,
    steps: int = 6,
    current_user: User = Depends(get_current_user)
):
    """
    Compare individual model forecasts with ensemble
    
    Args:
        metric: Metric to forecast
        steps: Number of periods to forecast
        current_user: Authenticated user
        
    Returns:
        Comparison of all models
    """
    try:
        # Get historical data
        historical_data = await FinancialModel.get_historical_data(
            current_user.id,
            months=24
        )
        
        if not historical_data or len(historical_data) < 6:
            raise HTTPException(
                status_code=400,
                detail="Insufficient data for forecasting"
            )
        
        # Extract metric values
        values = [d.get(metric, 0) for d in historical_data]
        
        # Generate ensemble forecast
        ensemble_result = ensemble_forecaster.forecast(
            historical_data=values,
            steps=steps,
            include_confidence=False
        )
        
        # Get individual model forecasts
        individual_forecasts = ensemble_forecaster.get_individual_forecasts(
            historical_data=values,
            steps=steps
        )
        
        return {
            "success": True,
            "metric": metric,
            "ensemble_forecast": ensemble_result.get("forecast", []),
            "individual_forecasts": individual_forecasts,
            "model_weights": ensemble_forecaster.model_weights,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
