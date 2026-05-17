import { StateCreator } from 'zustand';
import { UIState, WebSocketState, Notification } from '../types';
import * as api from '@/lib/api';

export interface UISlice extends UIState, WebSocketState {
  websocket: WebSocket | null;
  currency: 'INR' | 'USD';
  
  setCurrency: (currency: 'INR' | 'USD') => void;
  setCurrentPage: (page: string) => void;
  setBreadcrumbs: (breadcrumbs: Array<{ label: string; path: string }>) => void;
  openModal: (modal: string) => void;
  closeModal: (modal: string) => void;
  showToast: (message: string, type: 'success' | 'error' | 'info' | 'warning') => void;
  removeToast: (id: string) => void;
  setSidebarOpen: (open: boolean) => void;
  setChatOpen: (open: boolean) => void;
  setIsDark: (dark: boolean) => void;
  
  connectWebSocket: () => void;
  disconnectWebSocket: () => void;
  markNotificationRead: (notificationId: number) => void;
  clearNotifications: () => void;
}

export const createUISlice: StateCreator<
  UISlice & any,
  [["zustand/subscribeWithSelector", never], ["zustand/persist", unknown], ["zustand/immer", never]],
  [],
  UISlice
> = (set, get) => ({
  // UI Initial State
  sidebarOpen: true,
  chatOpen: false,
  isDark: true,
  currentPage: 'dashboard',
  breadcrumbs: [{ label: 'Dashboard', path: '/dashboard' }],
  modals: {},
  toast: [],
  currency: 'INR',
  
  // WebSocket Initial State
  connected: false,
  reconnecting: false,
  lastMessage: '',
  notifications: [],
  websocket: null,

  setCurrency: (currency) => {
    set((state) => {
      state.currency = currency;
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
    const id = Math.random().toString(36).substring(2, 9);
    set((state) => {
      state.toast.push({ id, message, type });
    });
    setTimeout(() => get().removeToast(id), 5000);
  },

  removeToast: (id) => {
    set((state) => {
      state.toast = state.toast.filter((t: any) => t.id !== id);
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

  connectWebSocket: () => {
    // Basic WebSocket implementation (can be refined)
    if (get().websocket) return;
    
    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
    const socket = new WebSocket(wsUrl);
    
    socket.onopen = () => {
      set((state) => {
        state.connected = true;
        state.websocket = socket;
      });
    };
    
    socket.onmessage = (event) => {
      set((state) => {
        state.lastMessage = event.data;
        // Handle incoming notifications if any
      });
    };
    
    socket.onclose = () => {
      set((state) => {
        state.connected = false;
        state.websocket = null;
      });
    };
  },

  disconnectWebSocket: () => {
    if (get().websocket) {
      get().websocket.close();
    }
  },

  markNotificationRead: (notificationId) => {
    set((state) => {
      const notification = state.notifications.find((n: Notification) => n.id === notificationId);
      if (notification) notification.is_read = true;
    });
  },

  clearNotifications: () => {
    set((state) => {
      state.notifications = [];
    });
  },
});
