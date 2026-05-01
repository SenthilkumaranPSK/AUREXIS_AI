/**
 * Fixed Enhanced State Management for AUREXIS AI Frontend
 * Critical bug fixes for missing functions and connection issues
 */

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { subscribeWithSelector } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';
import * as api from '@/lib/api';

// Types (same as before)
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
  
  // WebSocket connection
  websocket: WebSocket | null;
  
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
  
  // Analytics
  fetchRiskAnalysis: () => Promise<void>;
  fetchHealthScore: () => Promise<void>;
  fetchRecommendations: () => Promise<void>;
  fetchAlerts: () => Promise<void>;
  
  // WebSocket
  connectWebSocket: () => void;
  disconnectWebSocket: () => void;

  
  // UI - FIXED: Added missing functions
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

// Create the enhanced store with fixes
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
        websocket: null,
        
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
            const data = await api.login(credentials);
            
            set((state) => {
              state.currentUser = data.user;
              state.sessionId = data.access_token; // Use access_token as sessionId for legacy compat
              state.isAuthenticated = true;
              state.loading = false;
              state.lastFetch.login = new Date().toISOString();
            });
            
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
          try {
            await api.logout();
          } catch (error) {
            console.error('Logout error:', error);
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
            state.websocket = null;
            state.connected = false;
          });
        },
        
        refreshUser: async () => {
          if (!get().isAuthenticated) return;
          
          try {
            const data = await api.getUserProfile();
            set((state) => {
              state.currentUser = data;
            });
          } catch (error) {
            console.error('Error refreshing user:', error);
          }
        },
        
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
            get().showToast('Transaction added successfully', 'success');
          } catch (error) {
            get().showToast('Failed to add transaction', 'error');
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
            get().showToast('Goal updated successfully', 'success');
          } catch (error) {
            get().showToast('Failed to update goal', 'error');
            console.error('Error updating goal:', error);
          }
        },
        
        sendMessage: async (message) => {
          const { currentUser, currentChatSession } = get();
          if (!get().isAuthenticated) return;
          
          set((state) => {
            state.chatLoading = true;
            state.error = null;
          });
          
          try {
            const userMessage: ChatMessage = {
              role: 'user',
              content: message,
              timestamp: new Date().toISOString(),
            };
            
            set((state) => {
              state.chatMessages.push(userMessage);
            });
            
            const data = await api.sendChatMessage({
              user_id: currentUser?.id,
              message,
              session_id: currentChatSession,
              use_memory: true,
            });
            
            const aiMessage: ChatMessage = {
              role: 'assistant',
              content: data.response.content,
              timestamp: data.response.timestamp || new Date().toISOString(),
              confidence: data.response.confidence,
              model: data.response.model,
            };
            
            set((state) => {
              state.chatMessages.push(aiMessage);
              state.chatLoading = false;
            });
          } catch (error) {
            set((state) => {
              state.chatLoading = false;
              state.error = error instanceof Error ? error.message : 'Failed to send message';
            });
            get().showToast('Failed to send message', 'error');
          }
        },
        
        loadChatHistory: async (sessionId) => {
          if (!get().isAuthenticated) return;
          
          try {
            const data = await api.getChatHistory(sessionId);
            set((state) => {
              state.chatMessages = data.history || [];
              state.currentChatSession = sessionId || data.session_id;
            });
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
            const data = await api.getUserRecommendations();
            set((state) => {
              state.userAnalytics = { ...state.userAnalytics, recommendations: data.recommendations || data };
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
              state.notifications = [...state.notifications, ...(data.alerts || [])];
            });
          } catch (error) {
            console.error('Error fetching alerts:', error);
          }
        },

        
        // FIXED: Real WebSocket implementation
        connectWebSocket: () => {
          const { currentUser, sessionId } = get();
          if (!currentUser || !sessionId) return;
          
          try {
            const wsUrl = `ws://localhost:8000/ws/v1/chat?session_id=${sessionId}&user_id=${currentUser.id}`;
            const ws = new WebSocket(wsUrl);
            
            ws.onopen = () => {
              set((state) => {
                state.connected = true;
                state.reconnecting = false;
                state.websocket = ws;
              });
              console.log('WebSocket connected');
            };
            
            ws.onmessage = (event) => {
              try {
                const data = JSON.parse(event.data);
                set((state) => {
                  state.lastMessage = event.data;
                  
                  // Handle different message types
                  if (data.type === 'notification') {
                    state.notifications.push(data.data);
                  } else if (data.type === 'chat_response') {
                    state.chatMessages.push({
                      role: 'assistant',
                      content: data.data.content,
                      timestamp: data.data.timestamp,
                      confidence: data.data.confidence,
                      model: data.data.model,
                    });
                  }
                });
              } catch (error) {
                console.error('Error parsing WebSocket message:', error);
              }
            };
            
            ws.onclose = () => {
              set((state) => {
                state.connected = false;
                state.websocket = null;
              });
              console.log('WebSocket disconnected');
              
              // Attempt to reconnect after 3 seconds
              setTimeout(() => {
                if (!get().connected) {
                  set((state) => { state.reconnecting = true; });
                  get().connectWebSocket();
                }
              }, 3000);
            };
            
            ws.onerror = (error) => {
              console.error('WebSocket error:', error);
              set((state) => {
                state.connected = false;
                state.reconnecting = false;
              });
            };
            
          } catch (error) {
            console.error('Failed to connect WebSocket:', error);
            set((state) => {
              state.connected = false;
              state.reconnecting = false;
            });
          }
        },
        
        disconnectWebSocket: () => {
          const { websocket } = get();
          if (websocket) {
            websocket.close();
          }
          
          set((state) => {
            state.connected = false;
            state.reconnecting = false;
            state.websocket = null;
          });
        },
        
        // FIXED: Added missing UI functions
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
          
          setTimeout(() => {
            get().removeToast(id);
          }, 5000);
        },
        
        removeToast: (id) => {
          set((state) => {
            state.toast = state.toast.filter(t => t.id !== id);
          });
        },
        
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
          const { currentUser, simulationParams } = get();
          if (!get().isAuthenticated || !currentUser) return;
          
          set((state) => {
            state.loading = true;
            state.error = null;
          });
          
          try {
            const data = await api.runSimulation(currentUser.id, simulationParams);
            set((state) => {
              state.simulationResults = data.data || data;
              state.loading = false;
            });
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
            get().fetchRiskAnalysis(),
            get().fetchHealthScore(),
            get().fetchRecommendations(),
            get().fetchAlerts(),
          ]);
        },

      })),
      {
        name: 'aurexis-store',
        storage: createJSONStorage(() => localStorage),
        partialize: (state) => ({
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

// FIXED: Added missing functions to UI selector
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

// Other selectors remain the same
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
    userAnalytics: store.userAnalytics,
    systemHealth: store.systemHealth,
    fetchFinancialMetrics: store.fetchFinancialMetrics,
    fetchTransactions: store.fetchTransactions,
    fetchGoals: store.fetchGoals,
    fetchIncome: store.fetchIncome,
    addTransaction: store.addTransaction,
    updateGoal: store.updateGoal,
    fetchRiskAnalysis: store.fetchRiskAnalysis,
    fetchHealthScore: store.fetchHealthScore,
    fetchRecommendations: store.fetchRecommendations,
    fetchAlerts: store.fetchAlerts,
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

export const useWebSocket = () => {
  const store = useEnhancedStore();
  return {
    connected: store.connected,
    reconnecting: store.reconnecting,
    lastMessage: store.lastMessage,
    notifications: store.notifications,
    websocket: store.websocket,
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
