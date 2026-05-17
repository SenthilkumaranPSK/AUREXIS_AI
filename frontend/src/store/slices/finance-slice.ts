import { StateCreator } from 'zustand';
import { FinancialMetrics, Transaction, Goal, SimulationParams } from '../types';
import * as api from '@/lib/api';

export interface FinanceSlice {
  financialMetrics: FinancialMetrics | null;
  transactions: Transaction[];
  goals: Goal[];
  income: Array<{ month: string; amount: number; source?: string }>;
  simulationParams: SimulationParams;
  simulationResults: any;
  userAnalytics: any;
  systemHealth: any;

  fetchFinancialMetrics: () => Promise<void>;
  fetchTransactions: (limit?: number) => Promise<void>;
  fetchGoals: () => Promise<void>;
  fetchIncome: () => Promise<void>;
  addTransaction: (transaction: Omit<Transaction, 'id' | 'user_id' | 'created_at'>) => Promise<void>;
  updateGoal: (goalId: number, updates: Partial<Goal>) => Promise<void>;
  updateSimulationParams: (params: Partial<SimulationParams>) => void;
  setSimulationParams: (params: Partial<SimulationParams>) => void;
  runSimulation: () => Promise<void>;
  fetchRiskAnalysis: () => Promise<void>;
  fetchHealthScore: () => Promise<void>;
  fetchRecommendations: () => Promise<void>;
  fetchAlerts: () => Promise<void>;
}

export const createFinanceSlice: StateCreator<
  FinanceSlice & any,
  [["zustand/subscribeWithSelector", never], ["zustand/persist", unknown], ["zustand/immer", never]],
  [],
  FinanceSlice
> = (set, get) => ({
  financialMetrics: null,
  transactions: [],
  goals: [],
  income: [],
  simulationParams: {
    new_loan: 0,
    salary_increase: 0,
    job_loss: false,
    vacation_expense: 0,
    house_purchase: false,
    car_purchase: false,
    investment_increase: 0,
  },
  simulationResults: null,
  userAnalytics: null,
  systemHealth: null,

  fetchFinancialMetrics: async () => {
    if (!get().isAuthenticated) return;
    try {
      const data = await api.getUserMetrics();
      set((state) => {
        state.financialMetrics = data;
        state.lastFetch.metrics = new Date().toISOString();
      });
    } catch (error) {
      console.error('Error fetching metrics:', error);
    }
  },

  fetchTransactions: async (limit = 100) => {
    if (!get().isAuthenticated) return;
    try {
      const data = await api.getUserTransactions(limit);
      set((state) => {
        state.transactions = data || [];
        state.lastFetch.transactions = new Date().toISOString();
      });
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  },

  fetchGoals: async () => {
    if (!get().isAuthenticated) return;
    try {
      const data = await api.getUserGoals();
      set((state) => {
        state.goals = data.goals || data || [];
        state.lastFetch.goals = new Date().toISOString();
      });
    } catch (error) {
      console.error('Error fetching goals:', error);
    }
  },

  fetchIncome: async () => {
    if (!get().isAuthenticated) return;
    try {
      const data = await api.getUserIncome();
      set((state) => {
        state.income = data || [];
        state.lastFetch.income = new Date().toISOString();
      });
    } catch (error) {
      console.error('Error fetching income:', error);
    }
  },

  addTransaction: async (transaction) => {
    if (!get().isAuthenticated) return;
    try {
      await api.addTransaction(transaction);
      get().fetchTransactions();
      get().fetchFinancialMetrics();
      if (get().showToast) get().showToast('Transaction added successfully', 'success');
    } catch (error) {
      if (get().showToast) get().showToast('Failed to add transaction', 'error');
      console.error('Error adding transaction:', error);
    }
  },

  updateGoal: async (goalId, updates) => {
    if (!get().isAuthenticated) return;
    try {
      await api.updateGoal(goalId, updates);
      set((state) => {
        const goalIndex = state.goals.findIndex(g => g.id === goalId);
        if (goalIndex !== -1) {
          state.goals[goalIndex] = { ...state.goals[goalIndex], ...updates };
        }
      });
      if (get().showToast) get().showToast('Goal updated successfully', 'success');
    } catch (error) {
      if (get().showToast) get().showToast('Failed to update goal', 'error');
      console.error('Error updating goal:', error);
    }
  },

  updateSimulationParams: (params) => {
    set((state) => {
      state.simulationParams = { ...state.simulationParams, ...params };
    });
  },

  setSimulationParams: (params) => {
    set((state) => {
      state.simulationParams = { ...state.simulationParams, ...params };
    });
  },

  runSimulation: async () => {
    if (!get().isAuthenticated) return;
    try {
      const results = await api.runSimulation(get().currentUser?.id, get().simulationParams);
      set((state) => {
        state.simulationResults = results;
      });
    } catch (error) {
      console.error('Error running simulation:', error);
    }
  },

  fetchRiskAnalysis: async () => {
    if (!get().isAuthenticated) return;
    try {
      const data = await api.getUserRisk();
      set((state) => {
        state.userAnalytics = { ...state.userAnalytics, risk: data };
      });
    } catch (error) {
      console.error('Error fetching risk analysis:', error);
    }
  },

  fetchHealthScore: async () => {
    if (!get().isAuthenticated) return;
    try {
      const data = await api.getUserHealth();
      set((state) => {
        state.systemHealth = data;
      });
    } catch (error) {
      console.error('Error fetching health score:', error);
    }
  },

  fetchRecommendations: async () => {
    if (!get().isAuthenticated) return;
    try {
      const data = await api.getRecommendations();
      set((state) => {
        state.userAnalytics = { ...state.userAnalytics, recommendations: data };
      });
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  },

  fetchAlerts: async () => {
    if (!get().isAuthenticated) return;
    try {
      const data = await api.getUserAlerts();
      set((state) => {
        state.userAnalytics = { ...state.userAnalytics, alerts: data };
      });
    } catch (error) {
      console.error('Error fetching alerts:', error);
    }
  },
});
