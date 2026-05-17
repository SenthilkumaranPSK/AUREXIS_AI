import { create } from 'zustand';
import { persist, subscribeWithSelector } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';
import { AuthSlice, createAuthSlice } from './slices/auth-slice';
import { FinanceSlice, createFinanceSlice } from './slices/finance-slice';
import { UISlice, createUISlice } from './slices/ui-slice';
import { ChatSlice, createChatSlice } from './slices/chat-slice';

export type AppStore = AuthSlice & FinanceSlice & UISlice & ChatSlice & {
  clearCache: () => void;
  refreshData: () => Promise<void>;
};

export const useStore = create<AppStore>()(
  subscribeWithSelector(
    persist(
      immer((...a) => ({
        ...createAuthSlice(...a),
        ...createFinanceSlice(...a),
        ...createUISlice(...a),
        ...createChatSlice(...a),
        
        clearCache: () => {
          const [, get] = a;
          // Implement clear cache logic
        },
        
        refreshData: async () => {
          const [, get] = a;
          if (get().isAuthenticated) {
            await Promise.all([
              get().fetchFinancialMetrics(),
              get().fetchGoals(),
              get().fetchTransactions(),
            ]);
          }
        },
      })),
      {
        name: 'aurexis-storage',
        partialize: (state) => ({
          currentUser: state.currentUser,
          sessionId: state.sessionId,
          isAuthenticated: state.isAuthenticated,
          isDark: state.isDark,
          sidebarOpen: state.sidebarOpen,
          currency: state.currency,
        }),
      }
    )
  )
);

// For backward compatibility
export const useEnhancedStore = useStore;
