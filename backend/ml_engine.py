import os
import pickle
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel

# Scikit-Learn Imports
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.model_selection import train_test_split

class RiskInput(BaseModel):
    income: float
    total_expense: float
    savings: float
    expense_ratio: float
    savings_ratio: float
    spending_variability: float

class ForecastInput(BaseModel):
    time_steps: List[int]
    expenses: List[float]
    next_month: int

class MLEngine:
    def __init__(self):
        self.models_dir = os.path.join(os.path.dirname(__file__), "ml", "saved_models")
        os.makedirs(self.models_dir, exist_ok=True)
        
        self.risk_model_path = os.path.join(self.models_dir, "risk_rf_model.pkl")
        self.forecast_model_path = os.path.join(self.models_dir, "forecast_lr_model.pkl")
        self.cluster_model_path = os.path.join(self.models_dir, "recommender_kmeans.pkl")
        
        # In-memory models
        self.risk_model = self._load_model(self.risk_model_path)
        self.forecast_model = self._load_model(self.forecast_model_path)
        self.cluster_model = self._load_model(self.cluster_model_path)

    def _load_model(self, path):
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)
        return None
        
    def _save_model(self, model, path):
        with open(path, 'wb') as f:
            pickle.dump(model, f)

    def generate_synthetic_data(self):
        """Generate synthetic financial data to train models"""
        # Generate 1000 random samples
        np.random.seed(42)
        n_samples = 1000
        
        incomes = np.random.normal(50000, 15000, n_samples)
        expenses = incomes * np.random.uniform(0.3, 0.95, n_samples)
        savings = incomes - expenses
        expense_ratios = expenses / incomes
        savings_ratios = savings / incomes
        variabilities = np.random.uniform(0.05, 0.4, n_samples)
        
        X = np.column_stack((incomes, expenses, savings, expense_ratios, savings_ratios, variabilities))
        
        # Generate labels (0: Low Risk, 1: Medium Risk, 2: High Risk)
        y = []
        for i in range(n_samples):
            score = (expense_ratios[i] * 0.6) + (1 - savings_ratios[i]) * 0.4 + (variabilities[i] * 0.2)
            if score > 0.8:
                y.append(2) # High
            elif score > 0.5:
                y.append(1) # Medium
            else:
                y.append(0) # Low
                
        return X, np.array(y)

    def train_models(self) -> Dict[str, Any]:
        """Train all Machine Learning models and return evaluation metrics"""
        X, y = self.generate_synthetic_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 1. Classification (Risk Prediction)
        self.risk_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.risk_model.fit(X_train, y_train)
        y_pred_risk = self.risk_model.predict(X_test)
        risk_accuracy = accuracy_score(y_test, y_pred_risk)
        self._save_model(self.risk_model, self.risk_model_path)

        # 2. Regression (Forecasting)
        # Synthetic time-series data
        time_steps = np.arange(100).reshape(-1, 1)
        expenses_trend = 1000 + time_steps * 10 + np.random.normal(0, 50, (100, 1))
        
        X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(time_steps, expenses_trend, test_size=0.2, random_state=42)
        
        self.forecast_model = LinearRegression()
        self.forecast_model.fit(X_train_f, y_train_f)
        y_pred_forecast = self.forecast_model.predict(X_test_f)
        forecast_mae = mean_absolute_error(y_test_f, y_pred_forecast)
        self._save_model(self.forecast_model, self.forecast_model_path)

        # 3. Clustering (Recommendation Engine)
        self.cluster_model = KMeans(n_clusters=3, random_state=42, n_init=10)
        # Cluster based on expense ratio and savings ratio
        clustering_features = np.column_stack((X[:, 3], X[:, 4])) 
        self.cluster_model.fit(clustering_features)
        self._save_model(self.cluster_model, self.cluster_model_path)

        return {
            "status": "success",
            "message": "Models trained successfully",
            "metrics": {
                "risk_classification_accuracy": round(risk_accuracy, 4),
                "forecasting_mae": round(forecast_mae, 4)
            }
        }

    def predict_risk(self, data: RiskInput) -> Dict[str, str]:
        """Predict financial risk using Random Forest"""
        if self.risk_model is None:
            self.train_models()
            
        features = np.array([[
            data.income,
            data.total_expense,
            data.savings,
            data.expense_ratio,
            data.savings_ratio,
            data.spending_variability
        ]])
        
        prediction = self.risk_model.predict(features)[0]
        
        labels = {0: "Low", 1: "Medium", 2: "High"}
        return {
            "risk_label": labels[prediction]
        }

    def forecast_expenses(self, data: ForecastInput) -> Dict[str, float]:
        """Forecast future expense using Linear Regression"""
        if self.forecast_model is None:
            self.train_models()
            
        # Fit a new model specific to this user's data if provided
        if len(data.time_steps) > 1 and len(data.expenses) > 1:
            X = np.array(data.time_steps).reshape(-1, 1)
            y = np.array(data.expenses).reshape(-1, 1)
            model = LinearRegression()
            model.fit(X, y)
            future_val = model.predict([[data.next_month]])[0][0]
        else:
            future_val = self.forecast_model.predict([[data.next_month]])[0][0]
            
        return {
            "predicted_expense": round(float(future_val), 2)
        }

    def get_recommendation(self, expense_ratio: float, savings_ratio: float) -> str:
        """Get smart recommendation based on clustering"""
        if self.cluster_model is None:
            self.train_models()
            
        features = np.array([[expense_ratio, savings_ratio]])
        cluster = self.cluster_model.predict(features)[0]
        
        # Simple scoring fallback if clusters are ambiguous
        score = (expense_ratio * 0.5) + (1 - savings_ratio) * 0.5
        
        if score > 0.7:
            return "High risk: Reduce discretionary spending immediately."
        elif score > 0.4:
            return "Moderate: Optimize savings and review budget allocations."
        else:
            return "Good financial health: Maintain current financial habits."

ml_engine = MLEngine()
