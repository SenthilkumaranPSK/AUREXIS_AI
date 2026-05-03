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
  access_token?: string;
  refresh_token?: string;
  user?: UserProfile;
  data?: {
    access_token?: string;
    refresh_token?: string;
    session_id: string;
    user: UserProfile;
    expires_in: number;
  };
  message?: string;
}

export async function login(credentials: LoginCredentials): Promise<LoginResponse> {
  const response = await apiRequest<LoginResponse>("/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });

  const normalized: LoginResponse = response.data
    ? response
    : {
        ...response,
        data: response.user
          ? {
              access_token: response.access_token,
              refresh_token: response.refresh_token,
              session_id: `session_${response.user.id}`,
              user: response.user,
              expires_in: 1800,
            }
          : undefined,
      };

  if (normalized.success && normalized.data?.access_token) {
    localStorage.setItem("access_token", normalized.data.access_token);
  }
  if (normalized.success && normalized.data?.refresh_token) {
    localStorage.setItem("refresh_token", normalized.data.refresh_token);
  }
  if (normalized.success && normalized.data?.user) {
    localStorage.setItem("user_data", JSON.stringify(normalized.data.user));
  }

  return normalized;
}

export async function logout(sessionId?: string | null): Promise<{ success: boolean }> {
  const refreshToken = localStorage.getItem("refresh_token");
  try {
    if (sessionId) {
      await apiRequest("/logout", {
        method: "POST",
        body: JSON.stringify({ session_id: sessionId }),
      });
    }

    if (refreshToken) {
      await apiRequest("/auth/logout", {
        method: "POST",
        body: JSON.stringify({ refresh_token: refreshToken }),
      });
    }
  } finally {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user_data");
  }
  return { success: true };
}

// --- Financial API ---

export async function getUserMetrics(): Promise<any> {
  return apiRequest(`/financial/metrics`);
}

export async function getUserGoals(_userId?: string): Promise<any> {
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

export async function getUserHealth(_userId?: string): Promise<any> {
  return apiRequest(`/financial/health`);
}

export async function getUserAlerts(_userId?: string): Promise<any> {
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
    method: "PUT",
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
  conversation_history?: Array<{
    role: string;
    content: string;
  }>;
}

export async function sendChatMessage(request: ChatRequest): Promise<any> {
  return apiRequest("/chat/message", {
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
  return apiRequest(`/forecast/ml?steps=${steps}`);
}

export async function getRecommendations(): Promise<any> {
  return apiRequest(`/financial/recommendations`);
}

export async function generateRecommendations(): Promise<any> {
  return apiRequest(`/financial/recommendations/generate`, {
    method: "POST",
  });
}

export async function runSimulation(_userId: string, params: any): Promise<any> {
  return apiRequest(`/financial/simulation`, {
    method: "POST",
    body: JSON.stringify(params),
  });
}
