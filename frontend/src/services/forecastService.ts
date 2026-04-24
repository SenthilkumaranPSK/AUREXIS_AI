/**
 * Forecast Service
 * Handle ML forecasting operations
 */

import { api } from './api';

export interface ForecastData {
  month: string;
  actual?: number;
  forecast?: number;
  upper_bound?: number;
  lower_bound?: number;
}

export interface ForecastResponse {
  income_forecast: ForecastData[];
  expense_forecast: ForecastData[];
  savings_forecast: ForecastData[];
  confidence: number;
  model_version: string;
}

export interface ScenarioInput {
  scenario_type: 'salary_increase' | 'new_emi' | 'reduce_expenses' | 'emergency_expense' | 'custom';
  parameters: {
    income_change?: number;
    expense_change?: number;
    emi_amount?: number;
    emergency_amount?: number;
  };
}

export interface ScenarioResult {
  current: {
    monthly_income: number;
    monthly_expense: number;
    monthly_savings: number;
    health_score: number;
  };
  projected: {
    monthly_income: number;
    monthly_expense: number;
    monthly_savings: number;
    health_score: number;
  };
  impact: {
    income_diff: number;
    expense_diff: number;
    savings_diff: number;
    health_diff: number;
  };
}

export const forecastService = {
  /**
   * Get financial forecast
   */
  getForecast: async (months: number = 6): Promise<ForecastResponse> => {
    return api.get<ForecastResponse>('/api/forecast', {
      params: { months },
    });
  },

  /**
   * Get income forecast
   */
  getIncomeForecast: async (months: number = 6): Promise<ForecastData[]> => {
    return api.get<ForecastData[]>('/api/forecast/income', {
      params: { months },
    });
  },

  /**
   * Get expense forecast
   */
  getExpenseForecast: async (months: number = 6): Promise<ForecastData[]> => {
    return api.get<ForecastData[]>('/api/forecast/expenses', {
      params: { months },
    });
  },

  /**
   * Get savings forecast
   */
  getSavingsForecast: async (months: number = 6): Promise<ForecastData[]> => {
    return api.get<ForecastData[]>('/api/forecast/savings', {
      params: { months },
    });
  },

  /**
   * Run scenario simulation
   */
  runScenario: async (scenario: ScenarioInput): Promise<ScenarioResult> => {
    return api.post<ScenarioResult>('/api/forecast/scenario', scenario);
  },

  /**
   * Get goal timeline forecast
   */
  getGoalTimeline: async (goalId: string): Promise<{
    goal_id: string;
    estimated_completion: string;
    monthly_required: number;
    probability: number;
  }> => {
    return api.get(`/api/forecast/goal/${goalId}/timeline`);
  },
};

export default forecastService;
