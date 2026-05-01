"""
Forecast Service
Business logic for forecasting and predictions
"""

from typing import Dict, List
from user_manager_secure import UserManager
from forecasting import (
    compute_monthly_forecast,
    compute_net_worth_forecast,
    compute_goal_forecast,
    compute_expense_forecast,
    compute_savings_projection
)
from ml_forecasting import compute_ml_forecast
from analytics import compute_simulation


class ForecastService:
    """Forecasting business logic"""

    @staticmethod
    def get_monthly_forecast(user_id: str, months: int = 6) -> Dict:
        """Get monthly income/expense/savings forecast"""
        data = UserManager.get_all_user_data(user_id)
        return {
            "forecast": compute_monthly_forecast(data, months),
            "user_id": user_id,
            "months": months
        }

    @staticmethod
    def get_networth_forecast(user_id: str, years: int = 5) -> Dict:
        """Get multi-year net worth projection"""
        data = UserManager.get_all_user_data(user_id)
        return {
            "forecast": compute_net_worth_forecast(data, years),
            "user_id": user_id,
            "years": years
        }

    @staticmethod
    def get_goal_forecast(user_id: str) -> Dict:
        """Get goal completion timeline forecast"""
        data = UserManager.get_all_user_data(user_id)
        return {
            "goals": compute_goal_forecast(data),
            "user_id": user_id
        }

    @staticmethod
    def get_expense_forecast(user_id: str, months: int = 6) -> Dict:
        """Get category-wise expense trend forecast"""
        data = UserManager.get_all_user_data(user_id)
        return {
            "categories": compute_expense_forecast(data, months),
            "user_id": user_id,
            "months": months
        }

    @staticmethod
    def get_savings_projection(user_id: str) -> Dict:
        """Get savings projection at different rates"""
        data = UserManager.get_all_user_data(user_id)
        return compute_savings_projection(data)

    @staticmethod
    def get_ml_forecast(user_id: str, steps: int = 6) -> Dict:
        """Get ML-based forecast using multiple models"""
        data = UserManager.get_all_user_data(user_id)
        return compute_ml_forecast(data, steps)

    @staticmethod
    def run_scenario_simulation(
        user_id: str,
        new_loan: float = 0,
        salary_increase: float = 0,
        job_loss: bool = False,
        vacation_expense: float = 0,
        house_purchase: bool = False,
        car_purchase: bool = False,
        investment_increase: float = 0
    ) -> Dict:
        """Run what-if scenario simulation"""
        data = UserManager.get_all_user_data(user_id)
        return compute_simulation(
            data,
            new_loan=new_loan,
            salary_increase=salary_increase,
            job_loss=job_loss,
            vacation_expense=vacation_expense,
            house_purchase=house_purchase,
            car_purchase=car_purchase,
            investment_increase=investment_increase
        )
