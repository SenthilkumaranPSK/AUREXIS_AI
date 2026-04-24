import { create } from "zustand";
import { UserProfile, SimulationParams } from "@/types/finance";

interface AppStore {
  currentUser: UserProfile | null;
  sessionId: string | null;
  setCurrentUser: (user: UserProfile | null) => void;
  setSessionId: (id: string | null) => void;
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  chatOpen: boolean;
  setChatOpen: (open: boolean) => void;
  isDark: boolean;
  setIsDark: (dark: boolean) => void;
  simulationParams: SimulationParams;
  setSimulationParams: (params: Partial<SimulationParams>) => void;
}

export const useStore = create<AppStore>((set) => ({
  currentUser: null,
  sessionId: null,
  setCurrentUser: (user) => set({ currentUser: user }),
  setSessionId: (id) => set({ sessionId: id }),
  sidebarOpen: true,
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  chatOpen: false,
  setChatOpen: (open) => set({ chatOpen: open }),
  isDark: true,
  setIsDark: (dark) => set({ isDark: dark }),
  simulationParams: {
    newLoanAmount: 0,
    salaryIncrease: 0,
    jobLoss: false,
    vacationExpense: 0,
    housePurchase: false,
    carPurchase: false,
    investmentIncrease: 0,
  },
  setSimulationParams: (params) =>
    set((state) => ({
      simulationParams: { ...state.simulationParams, ...params },
    })),
}));
