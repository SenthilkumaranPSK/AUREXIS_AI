import { UserProfile } from "@/types/finance";

/**
 * API Client for AUREXIS AI Backend
 * Handles communication between frontend and modern Python backend (v1)
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const API_V1_URL = `${API_BASE_URL}/api`;

/**
 * Generic API request handler
 */
async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = endpoint.startsWith('http') ? endpoint : `${API_V1_URL}${endpoint}`;

  const token = localStorage.getItem('access_token');
  const defaultHeaders: HeadersInit = {
    "Content-Type": "application/json",
    ...(token ? { "Authorization": `Bearer ${token}` } : {}),
  };

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...(options?.headers || {}),
    },
  };

  try {
    const response = await fetch(url, config);

    if (response.status === 401) {
      console.warn("Unauthorized request - token may be expired");
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || errorData.detail || `API Error: ${response.status} ${response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error(`API request failed: ${endpoint}`, error);
    throw error;
  }
}

// --- Auth API ---

export interface LoginCredentials {
  username: string;  // Changed from email to username to match backend
  password: string;
}

export interface LoginResponse {
  success: boolean;
  access_token: string;
  refresh_token: string;
  user: UserProfile;
  data?: {
    session_id: string;
    user: any;
    expires_in: number;
  };
  message?: string;
}

export async function login(credentials: LoginCredentials): Promise<LoginResponse> {
  const response = await apiRequest<LoginResponse>("/login", {  // Changed from /auth/login to /login
    method: "POST",
    body: JSON.stringify(credentials),
  });
  
  // Backend returns tokens under `data.*` (legacy compatibility wrapper).
  // Store actual JWT access token so protected endpoints work.
  if (response.success && response.data?.access_token) {
    localStorage.setItem('access_token', response.data.access_token);
  }
  if (response.success && response.data?.refresh_token) {
    localStorage.setItem('refresh_token', response.data.refresh_token);
  }
  if (response.success && response.data?.user) {
    localStorage.setItem('user_data', JSON.stringify(response.data.user));
  }
  
  return response;
}

export async function logout(): Promise<{ success: boolean }> {
  const refreshToken = localStorage.getItem('refresh_token');
  try {
    await apiRequest("/auth/logout", {
      method: "POST",
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
  } finally {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
  return { success: true };
}

// --- Financial API ---

export async function getUserMetrics(): Promise<any> {
  return apiRequest(`/financial/metrics`);
}

export async function getUserGoals(): Promise<any> {
  return apiRequest(`/financial/goals`);
}

export async function getUserIncome(): Promise<any> {
  return apiRequest(`/financial/income`);
}

export async function getUserExpenses(): Promise<any> {
  return apiRequest(`/financial/expenses`);
}

export async function getUserInvestments(): Promise<any> {
  return apiRequest(`/financial/investments`);
}

export async function getUserRisk(): Promise<any> {
  return apiRequest(`/financial/risk`);
}

export async function getUserHealth(): Promise<any> {
  return apiRequest(`/financial/health`);
}

export async function getUserAlerts(): Promise<any> {
  return apiRequest(`/financial/alerts`);
}

export async function getUserStocks(): Promise<any> {
  return apiRequest(`/financial/stocks`);
}

export async function getUserMutualFunds(): Promise<any> {
  return apiRequest(`/financial/mutual-funds`);
}

export async function addTransaction(transaction: any): Promise<any> {
  return apiRequest(`/financial/transactions`, {
    method: "POST",
    body: JSON.stringify(transaction),
  });
}

export async function updateGoal(goalId: string | number, updates: any): Promise<any> {
  return apiRequest(`/financial/goals/${goalId}`, {
    method: "PATCH",
    body: JSON.stringify(updates),
  });
}

// --- Forecast API ---

export async function getMonthlyForecast(): Promise<any> {
  return apiRequest(`/forecast/monthly`);
}

export async function getNetworthForecast(years = 5): Promise<any> {
  return apiRequest(`/forecast/networth?years=${years}`);
}

export async function getGoalForecast(): Promise<any> {
  return apiRequest(`/forecast/goals`);
}

// --- Chat API ---

export interface ChatRequest {
  user_id?: string;
  message: string;
  session_id?: string;
  use_memory?: boolean;
}

export async function sendChatMessage(request: ChatRequest): Promise<any> {
  return apiRequest("/chat", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function getChatHistory(sessionId?: string): Promise<any> {
  const endpoint = sessionId ? `/chat/history?session_id=${sessionId}` : '/chat/history';
  return apiRequest(endpoint);
}

// --- Advanced API ---

export async function getMLForecast(steps = 6): Promise<any> {
  return apiRequest(`/ml/forecast?steps=${steps}`);
}

export async function getRecommendations(): Promise<any> {
  return apiRequest(`/financial/recommendations`);
}

export async function runSimulation(_userId: string, params: any): Promise<any> {
  return apiRequest(`/financial/simulation`, {
    method: "POST",
    body: JSON.stringify(params),
  });
}
