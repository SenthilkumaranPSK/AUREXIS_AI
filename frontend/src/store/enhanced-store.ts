/**
 * Enhanced State Management for AUREXIS AI Frontend
 * Comprehensive state management with persistence, caching, and real-time updates
 */

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { subscribeWithSelector } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// Types
export interface UserProfile {
  id: string;
  name: string;
  email: string;
  occupation?: string;
  age?: number;
  location?: string;
  user_number: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login?: string;
}

export interface FinancialMetrics {
  monthly_income: number;
  monthly_expenses: number;
  monthly_savings: number;
  savings_rate: number;
  net_worth: number;
  debt_to_income_ratio: number;
  emergency_fund_months: number;
  investment_portfolio_value: number;
}

export interface Transaction {
  id: number;
  user_id: string;
  date: string;
  amount: number;
  category: string;
  description?: string;
  merchant?: string;
  created_at: string;
}

export interface Goal {
  id: number;
  user_id: string;
  name: string;
  target_amount: number;
  current_amount: number;
  deadline?: string;
  category?: string;
  status: 'active' | 'completed' | 'paused';
  created_at: string;
  updated_at: string;
}

export interface ChatMessage {
  id?: number;
  session_id?: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  confidence?: number;
  model?: string;
}

export interface Notification {
  id: number;
  type: string;
  title: string;
  message: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  is_read: boolean;
  created_at: string;
}

export interface SimulationParams {
  new_loan: number;
  salary_increase: number;
  job_loss: boolean;
  vacation_expense: number;
  house_purchase: boolean;
  car_purchase: boolean;
  investment_increase: number;
}

export interface APIState {
  loading: boolean;
  error: string | null;
  lastFetch: Record<string, string>;
}

export interface WebSocketState {
  connected: boolean;
  reconnecting: boolean;
  lastMessage: string;
  notifications: Notification[];
}

export interface UIState {
  sidebarOpen: boolean;
  chatOpen: boolean;
  isDark: boolean;
  currentPage: string;
  breadcrumbs: Array<{ label: string; path: string }>;
  modals: Record<string, boolean>;
  toast: Array<{ id: string; message: string; type: 'success' | 'error' | 'info' | 'warning' }>;
}

// Main store interface
interface AppStore extends APIState, WebSocketState, UIState {
  // Authentication
  currentUser: UserProfile | null;
  sessionId: string | null;
  isAuthenticated: boolean;
  
  // Financial Data
  financialMetrics: FinancialMetrics | null;
  transactions: Transaction[];
  goals: Goal[];
  income: Array<{ month: string; amount: number; source?: string }>;
  
  // Chat
  chatMessages: ChatMessage[];
  currentChatSession: string | null;
  chatLoading: boolean;
  
  // Simulation
  simulationParams: SimulationParams;
  simulationResults: any;
  
  // Analytics
  userAnalytics: any;
  systemHealth: any;
  
  // Actions
  // Authentication
  login: (credentials: { username: string; password: string }) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  
  // Financial Data
  fetchFinancialMetrics: () => Promise<void>;
  fetchTransactions: (limit?: number) => Promise<void>;
  fetchGoals: () => Promise<void>;
  fetchIncome: () => Promise<void>;
  addTransaction: (transaction: Omit<Transaction, 'id' | 'user_id' | 'created_at'>) => Promise<void>;
  updateGoal: (goalId: number, updates: Partial<Goal>) => Promise<void>;
  
  // Chat
  sendMessage: (message: string) => Promise<void>;
  loadChatHistory: (sessionId?: string) => Promise<void>;
  clearChatHistory: () => void;
  
  // WebSocket
  connectWebSocket: () => void;
  disconnectWebSocket: () => void;
  
  // UI
  setCurrentPage: (page: string) => void;
  setBreadcrumbs: (breadcrumbs: Array<{ label: string; path: string }>) => void;
  openModal: (modal: string) => void;
  closeModal: (modal: string) => void;
  showToast: (message: string, type: 'success' | 'error' | 'info' | 'warning') => void;
  removeToast: (id: string) => void;
  setSidebarOpen: (open: boolean) => void;
  setChatOpen: (open: boolean) => void;
  setIsDark: (dark: boolean) => void;
  
  // Simulation
  updateSimulationParams: (params: Partial<SimulationParams>) => void;
  runSimulation: () => Promise<void>;
  
  // Notifications
  markNotificationRead: (notificationId: number) => void;
  clearNotifications: () => void;
  
  // Cache management
  clearCache: () => void;
  refreshData: () => Promise<void>;
}

// Create the enhanced store
export const useEnhancedStore = create<AppStore>()(
  subscribeWithSelector(
    persist(
      immer((set, get) => ({
        // Initial state
        // Authentication
        currentUser: null,
        sessionId: null,
        isAuthenticated: false,
        
        // API State
        loading: false,
        error: null,
        lastFetch: {},
        
        // WebSocket State
        connected: false,
        reconnecting: false,
        lastMessage: '',
        notifications: [],
        
        // UI State
        sidebarOpen: true,
        chatOpen: false,
        isDark: true,
        currentPage: 'dashboard',
        breadcrumbs: [{ label: 'Dashboard', path: '/dashboard' }],
        modals: {},
        toast: [],
        
        // Financial Data
        financialMetrics: null,
        transactions: [],
        goals: [],
        income: [],
        
        // Chat
        chatMessages: [],
        currentChatSession: null,
        chatLoading: false,
        
        // Simulation
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
        
        // Analytics
        userAnalytics: null,
        systemHealth: null,
        
        // Actions
        login: async (credentials) => {
          set((state) => {
            state.loading = true;
            state.error = null;
          });
          
          try {
            const response = await fetch(API_BASE_URL + '/api/v1/auth/login', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(credentials),
            });
            
            if (!response.ok) {
              const error = await response.json();
              throw new Error(error.message || 'Login failed');
            }
            
            const data = await response.json();
            
            set((state) => {
              state.currentUser = data.data.user;
              state.sessionId = data.data.session_id;
              state.isAuthenticated = true;
              state.loading = false;
              state.lastFetch.login = new Date().toISOString();
            });
            
            // Store session ID in localStorage for API calls
            localStorage.setItem('sessionId', data.data.session_id);
            
            // Fetch initial data
            get().fetchFinancialMetrics();
            get().fetchGoals();
            
          } catch (error) {
            set((state) => {
              state.loading = false;
              state.error = error instanceof Error ? error.message : 'Login failed';
            });
            throw error;
          }
        },
        
        logout: async () => {
          const sessionId = get().sessionId;
          
          if (sessionId) {
            try {
              await fetch(API_BASE_URL + '/api/v1/auth/logout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId }),
              });
            } catch (error) {
              console.error('Logout error:', error);
            }
          }
          
          set((state) => {
            state.currentUser = null;
            state.sessionId = null;
            state.isAuthenticated = false;
            state.financialMetrics = null;
            state.transactions = [];
            state.goals = [];
            state.chatMessages = [];
            state.notifications = [];
          });
          
          localStorage.removeItem('sessionId');
        },
        
        refreshUser: async () => {
          const { currentUser } = get();
          if (!currentUser) return;
          
          try {
            // Fetch updated user data
            const response = await fetch(`${API_BASE_URL}/api/v1/users/${currentUser.id}`, {
              headers: { 'X-Session-ID': get().sessionId || '' },
            });
            
            if (response.ok) {
              const data = await response.json();
              set((state) => {
                state.currentUser = data.data;
              });
            }
          } catch (error) {
            console.error('Error refreshing user:', error);
          }
        },
        
        fetchFinancialMetrics: async () => {
          const { currentUser, sessionId } = get();
          if (!currentUser || !sessionId) return;
          
          try {
            const response = await fetch(`${API_BASE_URL}/api/v1/analytics/metrics/${currentUser.id}`, {
              headers: { 'X-Session-ID': sessionId },
            });
            
            if (response.ok) {
              const data = await response.json();
              set((state) => {
                state.financialMetrics = data.data;
                state.lastFetch.metrics = new Date().toISOString();
              });
            }
          } catch (error) {
            console.error('Error fetching metrics:', error);
          }
        },
        
        fetchTransactions: async (limit = 100) => {
          const { currentUser, sessionId } = get();
          if (!currentUser || !sessionId) return;
          
          try {
            const response = await fetch(`${API_BASE_URL}/api/v1/financial/transactions/${currentUser.id}?limit=${limit}`, {
              headers: { 'X-Session-ID': sessionId },
            });
            
            if (response.ok) {
              const data = await response.json();
              set((state) => {
                state.transactions = data.data || [];
                state.lastFetch.transactions = new Date().toISOString();
              });
            }
          } catch (error) {
            console.error('Error fetching transactions:', error);
          }
        },
        
        fetchGoals: async () => {
          const { currentUser, sessionId } = get();
          if (!currentUser || !sessionId) return;
          
          try {
            const response = await fetch(`${API_BASE_URL}/api/v1/financial/goals/${currentUser.id}`, {
              headers: { 'X-Session-ID': sessionId },
            });
            
            if (response.ok) {
              const data = await response.json();
              set((state) => {
                state.goals = data.data || [];
                state.lastFetch.goals = new Date().toISOString();
              });
            }
          } catch (error) {
            console.error('Error fetching goals:', error);
          }
        },
        
        fetchIncome: async () => {
          const { currentUser, sessionId } = get();
          if (!currentUser || !sessionId) return;
          
          try {
            const response = await fetch(`${API_BASE_URL}/api/v1/financial/income/${currentUser.id}`, {
              headers: { 'X-Session-ID': sessionId },
            });
            
            if (response.ok) {
              const data = await response.json();
              set((state) => {
                state.income = data.data || [];
                state.lastFetch.income = new Date().toISOString();
              });
            }
          } catch (error) {
            console.error('Error fetching income:', error);
          }
        },
        
        addTransaction: async (transaction) => {
          const { currentUser, sessionId } = get();
          if (!currentUser || !sessionId) return;
          
          try {
            const response = await fetch(`${API_BASE_URL}/api/v1/financial/transactions/${currentUser.id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-Session-ID': sessionId,
              },
              body: JSON.stringify(transaction),
            });
            
            if (response.ok) {
              // Refresh transactions
              get().fetchTransactions();
              get().fetchFinancialMetrics();
              
              get().showToast('Transaction added successfully', 'success');
            } else {
              throw new Error('Failed to add transaction');
            }
          } catch (error) {
            get().showToast('Failed to add transaction', 'error');
            console.error('Error adding transaction:', error);
          }
        },
        
        updateGoal: async (goalId, updates) => {
          const { currentUser, sessionId } = get();
          if (!currentUser || !sessionId) return;
          
          try {
            const response = await fetch(`${API_BASE_URL}/api/v1/financial/goals/${currentUser.id}/${goalId}`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
                'X-Session-ID': sessionId,
              },
              body: JSON.stringify(updates),
            });
            
            if (response.ok) {
              // Update local state
              set((state) => {
                const goalIndex = state.goals.findIndex(g => g.id === goalId);
                if (goalIndex !== -1) {
                  state.goals[goalIndex] = { ...state.goals[goalIndex], ...updates };
                }
              });
              
              get().showToast('Goal updated successfully', 'success');
            } else {
              throw new Error('Failed to update goal');
            }
          } catch (error) {
            get().showToast('Failed to update goal', 'error');
            console.error('Error updating goal:', error);
          }
        },
        
        sendMessage: async (message) => {
          const { currentUser, sessionId, currentChatSession } = get();
          if (!currentUser || !sessionId) return;
          
          set((state) => {
            state.chatLoading = true;
            state.error = null;
          });
          
          try {
            // Add user message to local state immediately
            const userMessage: ChatMessage = {
              role: 'user',
              content: message,
              timestamp: new Date().toISOString(),
            };
            
            set((state) => {
              state.chatMessages.push(userMessage);
            });
            
            const response = await fetch(API_BASE_URL + '/api/v1/chat', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-Session-ID': sessionId,
              },
              body: JSON.stringify({
                user_id: currentUser.id,
                message,
                session_id: currentChatSession,
                use_memory: true,
              }),
            });
            
            if (response.ok) {
              const data = await response.json();
              
              // Add AI response to local state
              const aiMessage: ChatMessage = {
                role: 'assistant',
                content: data.response.content,
                timestamp: data.response.timestamp,
                confidence: data.response.confidence,
                model: data.response.model,
              };
              
              set((state) => {
                state.chatMessages.push(aiMessage);
                state.chatLoading = false;
              });
            } else {
              throw new Error('Failed to send message');
            }
          } catch (error) {
            set((state) => {
              state.chatLoading = false;
              state.error = error instanceof Error ? error.message : 'Failed to send message';
            });
            get().showToast('Failed to send message', 'error');
          }
        },
        
        loadChatHistory: async (sessionId) => {
          const { currentUser, sessionId: userSessionId } = get();
          if (!currentUser || !userSessionId) return;
          
          try {
            const response = await fetch(
              `/api/v1/chat/history/${currentUser.id}${sessionId ? `?session_id=${sessionId}` : ''}`,
              { headers: { 'X-Session-ID': userSessionId } }
            );
            
            if (response.ok) {
              const data = await response.json();
              set((state) => {
                state.chatMessages = data.history || [];
                state.currentChatSession = sessionId;
              });
            }
          } catch (error) {
            console.error('Error loading chat history:', error);
          }
        },
        
        clearChatHistory: () => {
          set((state) => {
            state.chatMessages = [];
            state.currentChatSession = null;
          });
        },
        
        connectWebSocket: () => {
          const { currentUser, sessionId } = get();
          if (!currentUser || !sessionId) return;
          
          // WebSocket connection logic would go here
          // For now, just set connected state
          set((state) => {
            state.connected = true;
          });
        },
        
        disconnectWebSocket: () => {
          set((state) => {
            state.connected = false;
            state.reconnecting = false;
          });
        },
        
        setCurrentPage: (page) => {
          set((state) => {
            state.currentPage = page;
          });
        },
        
        setBreadcrumbs: (breadcrumbs) => {
          set((state) => {
            state.breadcrumbs = breadcrumbs;
          });
        },
        
        openModal: (modal) => {
          set((state) => {
            state.modals[modal] = true;
          });
        },
        
        closeModal: (modal) => {
          set((state) => {
            state.modals[modal] = false;
          });
        },
        
        showToast: (message, type) => {
          const id = Date.now().toString();
          set((state) => {
            state.toast.push({ id, message, type });
          });
          
          // Auto-remove toast after 5 seconds
          setTimeout(() => {
            get().removeToast(id);
          }, 5000);
        },
        
        removeToast: (id) => {
          set((state) => {
            state.toast = state.toast.filter(t => t.id !== id);
          });
        },
        
        // Add missing UI functions
        setSidebarOpen: (open) => {
          set((state) => {
            state.sidebarOpen = open;
          });
        },
        
        setChatOpen: (open) => {
          set((state) => {
            state.chatOpen = open;
          });
        },
        
        setIsDark: (dark) => {
          set((state) => {
            state.isDark = dark;
          });
        },
        
        updateSimulationParams: (params) => {
          set((state) => {
            state.simulationParams = { ...state.simulationParams, ...params };
          });
        },
        
        runSimulation: async () => {
          const { currentUser, sessionId, simulationParams } = get();
          if (!currentUser || !sessionId) return;
          
          set((state) => {
            state.loading = true;
            state.error = null;
          });
          
          try {
            const response = await fetch(`${API_BASE_URL}/api/v1/analytics/simulation/${currentUser.id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-Session-ID': sessionId,
              },
              body: JSON.stringify(simulationParams),
            });
            
            if (response.ok) {
              const data = await response.json();
              set((state) => {
                state.simulationResults = data.data;
                state.loading = false;
              });
            } else {
              throw new Error('Simulation failed');
            }
          } catch (error) {
            set((state) => {
              state.loading = false;
              state.error = error instanceof Error ? error.message : 'Simulation failed';
            });
            get().showToast('Simulation failed', 'error');
          }
        },
        
        markNotificationRead: (notificationId) => {
          set((state) => {
            const notification = state.notifications.find(n => n.id === notificationId);
            if (notification) {
              notification.is_read = true;
            }
          });
        },
        
        clearNotifications: () => {
          set((state) => {
            state.notifications = [];
          });
        },
        
        clearCache: () => {
          set((state) => {
            state.lastFetch = {};
            state.financialMetrics = null;
            state.transactions = [];
            state.goals = [];
            state.income = [];
          });
        },
        
        refreshData: async () => {
          const { isAuthenticated } = get();
          if (!isAuthenticated) return;
          
          get().clearCache();
          await Promise.all([
            get().fetchFinancialMetrics(),
            get().fetchTransactions(),
            get().fetchGoals(),
            get().fetchIncome(),
          ]);
        },
      })),
      {
        name: 'aurexis-store',
        storage: createJSONStorage(() => localStorage),
        partialize: (state) => ({
          // Only persist these fields
          currentUser: state.currentUser,
          sessionId: state.sessionId,
          isAuthenticated: state.isAuthenticated,
          sidebarOpen: state.sidebarOpen,
          chatOpen: state.chatOpen,
          isDark: state.isDark,
          simulationParams: state.simulationParams,
          lastFetch: state.lastFetch,
        }),
      }
    )
  )
);

// Selectors for optimized re-renders
export const useAuth = () => {
  const store = useEnhancedStore();
  return {
    currentUser: store.currentUser,
    sessionId: store.sessionId,
    isAuthenticated: store.isAuthenticated,
    login: store.login,
    logout: store.logout,
    refreshUser: store.refreshUser,
  };
};

export const useFinancialData = () => {
  const store = useEnhancedStore();
  return {
    financialMetrics: store.financialMetrics,
    transactions: store.transactions,
    goals: store.goals,
    income: store.income,
    loading: store.loading,
    error: store.error,
    fetchFinancialMetrics: store.fetchFinancialMetrics,
    fetchTransactions: store.fetchTransactions,
    fetchGoals: store.fetchGoals,
    fetchIncome: store.fetchIncome,
    addTransaction: store.addTransaction,
    updateGoal: store.updateGoal,
  };
};

export const useChat = () => {
  const store = useEnhancedStore();
  return {
    chatMessages: store.chatMessages,
    currentChatSession: store.currentChatSession,
    chatLoading: store.chatLoading,
    sendMessage: store.sendMessage,
    loadChatHistory: store.loadChatHistory,
    clearChatHistory: store.clearChatHistory,
  };
};

export const useUI = () => {
  const store = useEnhancedStore();
  return {
    sidebarOpen: store.sidebarOpen,
    chatOpen: store.chatOpen,
    isDark: store.isDark,
    currentPage: store.currentPage,
    breadcrumbs: store.breadcrumbs,
    modals: store.modals,
    toast: store.toast,
    setSidebarOpen: store.setSidebarOpen,
    setChatOpen: store.setChatOpen,
    setIsDark: store.setIsDark,
    setCurrentPage: store.setCurrentPage,
    setBreadcrumbs: store.setBreadcrumbs,
    openModal: store.openModal,
    closeModal: store.closeModal,
    showToast: store.showToast,
    removeToast: store.removeToast,
  };
};

export const useWebSocket = () => {
  const store = useEnhancedStore();
  return {
    connected: store.connected,
    reconnecting: store.reconnecting,
    lastMessage: store.lastMessage,
    notifications: store.notifications,
    connectWebSocket: store.connectWebSocket,
    disconnectWebSocket: store.disconnectWebSocket,
    markNotificationRead: store.markNotificationRead,
    clearNotifications: store.clearNotifications,
  };
};

export const useSimulation = () => {
  const store = useEnhancedStore();
  return {
    simulationParams: store.simulationParams,
    simulationResults: store.simulationResults,
    loading: store.loading,
    error: store.error,
    updateSimulationParams: store.updateSimulationParams,
    runSimulation: store.runSimulation,
  };
};

// Export the main store for backward compatibility
export const useStore = useEnhancedStore;
