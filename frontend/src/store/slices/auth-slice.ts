import { StateCreator } from 'zustand';
import { UserProfile } from '../types';
import * as api from '@/lib/api';

export interface AuthSlice {
  currentUser: UserProfile | null;
  sessionId: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
  lastFetch: Record<string, string>;
  
  setCurrentUser: (user: UserProfile | null) => void;
  setSessionId: (id: string | null) => void;
  login: (credentials: { username: string; password: string }) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

export const createAuthSlice: StateCreator<
  AuthSlice & any,
  [["zustand/subscribeWithSelector", never], ["zustand/persist", unknown], ["zustand/immer", never]],
  [],
  AuthSlice
> = (set, get) => ({
  currentUser: null,
  sessionId: null,
  isAuthenticated: false,
  loading: false,
  error: null,
  lastFetch: {},

  setCurrentUser: (user) => {
    set((state) => {
      state.currentUser = user;
      state.isAuthenticated = !!user;
    });
  },

  setSessionId: (id) => {
    set((state) => {
      state.sessionId = id;
    });
  },

  login: async (credentials) => {
    set((state) => {
      state.loading = true;
      state.error = null;
    });
    
    try {
      const data = await api.login(credentials);
      
      set((state) => {
        state.currentUser = data.user;
        state.sessionId = data.access_token;
        state.isAuthenticated = true;
        state.loading = false;
        state.lastFetch.login = new Date().toISOString();
      });
      
      if (get().fetchFinancialMetrics) await get().fetchFinancialMetrics();
      if (get().fetchGoals) await get().fetchGoals();
      
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
      // Reset other states if needed or handle in root store
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
});
