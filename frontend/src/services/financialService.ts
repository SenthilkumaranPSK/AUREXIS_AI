/**
 * Financial Service
 * Handle financial data operations
 */

import { api } from './api';

export interface FinancialHealthScore {
  overall_score: number;
  savings_score: number;
  debt_score: number;
  emergency_fund_score: number;
  investment_score: number;
  timestamp: string;
}

export interface Expense {
  id: string;
  date: string;
  amount: number;
  category: string;
  description: string;
  merchant?: string;
}

export interface Income {
  id: string;
  month: string;
  amount: number;
  source: string;
}

export interface Goal {
  id: string;
  name: string;
  target_amount: number;
  current_amount: number;
  deadline: string;
  category: string;
  monthly_required?: number;
  status: 'active' | 'completed' | 'paused';
}

export interface Alert {
  id: string;
  type: string;
  title: string;
  message: string;
  severity: 'critical' | 'warning' | 'info' | 'success';
  is_read: boolean;
  created_at: string;
}

export interface Recommendation {
  id: string;
  category: string;
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  impact?: string;
  status: 'pending' | 'applied' | 'dismissed';
}

export const financialService = {
  /**
   * Get financial health score
   */
  getHealthScore: async (): Promise<FinancialHealthScore> => {
    return api.get<FinancialHealthScore>('/api/financial/health-score');
  },

  /**
   * Get expenses
   */
  getExpenses: async (params?: {
    start_date?: string;
    end_date?: string;
    category?: string;
  }): Promise<Expense[]> => {
    return api.get<Expense[]>('/api/financial/expenses', { params });
  },

  /**
   * Add expense
   */
  addExpense: async (expense: Omit<Expense, 'id'>): Promise<Expense> => {
    return api.post<Expense>('/api/financial/expenses', expense);
  },

  /**
   * Update expense
   */
  updateExpense: async (id: string, expense: Partial<Expense>): Promise<Expense> => {
    return api.put<Expense>(`/api/financial/expenses/${id}`, expense);
  },

  /**
   * Delete expense
   */
  deleteExpense: async (id: string): Promise<void> => {
    return api.delete(`/api/financial/expenses/${id}`);
  },

  /**
   * Get income
   */
  getIncome: async (params?: { start_date?: string; end_date?: string }): Promise<Income[]> => {
    return api.get<Income[]>('/api/financial/income', { params });
  },

  /**
   * Add income
   */
  addIncome: async (income: Omit<Income, 'id'>): Promise<Income> => {
    return api.post<Income>('/api/financial/income', income);
  },

  /**
   * Get goals
   */
  getGoals: async (): Promise<Goal[]> => {
    return api.get<Goal[]>('/api/financial/goals');
  },

  /**
   * Create goal
   */
  createGoal: async (goal: Omit<Goal, 'id' | 'current_amount' | 'status'>): Promise<Goal> => {
    return api.post<Goal>('/api/financial/goals', goal);
  },

  /**
   * Update goal
   */
  updateGoal: async (id: string, goal: Partial<Goal>): Promise<Goal> => {
    return api.put<Goal>(`/api/financial/goals/${id}`, goal);
  },

  /**
   * Delete goal
   */
  deleteGoal: async (id: string): Promise<void> => {
    return api.delete(`/api/financial/goals/${id}`);
  },

  /**
   * Get alerts
   */
  getAlerts: async (params?: { is_read?: boolean }): Promise<Alert[]> => {
    return api.get<Alert[]>('/api/financial/alerts', { params });
  },

  /**
   * Mark alert as read
   */
  markAlertAsRead: async (id: string): Promise<void> => {
    return api.patch(`/api/financial/alerts/${id}/read`);
  },

  /**
   * Get recommendations
   */
  getRecommendations: async (): Promise<Recommendation[]> => {
    return api.get<Recommendation[]>('/api/financial/recommendations');
  },

  /**
   * Apply recommendation
   */
  applyRecommendation: async (id: string): Promise<void> => {
    return api.post(`/api/financial/recommendations/${id}/apply`);
  },

  /**
   * Dismiss recommendation
   */
  dismissRecommendation: async (id: string): Promise<void> => {
    return api.post(`/api/financial/recommendations/${id}/dismiss`);
  },

  /**
   * Get expense analytics
   */
  getExpenseAnalytics: async (params?: {
    start_date?: string;
    end_date?: string;
  }): Promise<any> => {
    return api.get('/api/financial/analytics/expenses', { params });
  },

  /**
   * Get savings analytics
   */
  getSavingsAnalytics: async (): Promise<any> => {
    return api.get('/api/financial/analytics/savings');
  },

  /**
   * Get net worth
   */
  getNetWorth: async (): Promise<{ net_worth: number; timestamp: string }> => {
    return api.get('/api/financial/net-worth');
  },
};

export default financialService;
