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
