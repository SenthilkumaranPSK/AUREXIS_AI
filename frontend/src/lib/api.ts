import { UserProfile } from "@/types/finance";

/**
 * API Client for AUREXIS AI Backend
 * Handles communication between frontend and Python backend
 */

const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Generic API request handler
 */
async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultHeaders: HeadersInit = {
    "Content-Type": "application/json",
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

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `API Error: ${response.status} ${response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error(`API request failed: ${endpoint}`, error);
    throw error;
  }
}

// --- Types ---

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResponse {
  success: boolean;
  session_id: string;
  user: UserProfile;
}

export interface ChatRequest {
  user_id: string;
  message: string;
  conversation_history?: Array<{ role: string; content: string }>;
}

export interface ChatResponse {
  success: boolean;
  response: {
    summary: string;
    content: string;
    insights?: string[];
    recommendations?: string[];
    confidence?: number;
    risks?: string[];
  };
  user_id: string;
}

// --- API Functions ---

/**
 * Health check - verify backend is running
 */
export async function checkHealth(): Promise<{ status: string }> {
  return apiRequest("/");
}

/**
 * Authenticate user
 */
export async function login(
  credentials: LoginCredentials
): Promise<LoginResponse> {
  return apiRequest<LoginResponse>("/api/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}

/**
 * Logout user
 */
export async function logout(sessionId: string): Promise<{ success: boolean }> {
  return apiRequest("/api/logout", {
    method: "POST",
    body: JSON.stringify({ session_id: sessionId }),
  });
}

/**
 * Get all users (for demo/debugging)
 */
export async function getAllUsers(): Promise<{ users: any[]; count: number }> {
  return apiRequest("/api/users");
}

/**
 * Get specific financial data for a user
 */
export async function getUserData(
  userId: string,
  dataType: string
): Promise<any> {
  return apiRequest(`/api/user/${userId}/data/${dataType}`);
}

/**
 * Get all financial data for a user
 */
export async function getAllUserData(userId: string): Promise<any> {
  return apiRequest(`/api/user/${userId}/data`);
}

/**
 * Send message to Ollama AI advisor
 */
export async function sendChatMessage(
  request: ChatRequest
): Promise<ChatResponse> {
  return apiRequest<ChatResponse>("/api/chat", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

// --- Analytics API ---

export async function getUserMetrics(userId: string): Promise<any> {
  return apiRequest(`/api/user/${userId}/metrics`);
}

export async function getUserForecast(userId: string): Promise<{ forecast: any[] }> {
  return apiRequest(`/api/user/${userId}/forecast/monthly`);
}

export async function getNetworthForecast(userId: string, years = 5): Promise<{ forecast: any[] }> {
  return apiRequest(`/api/user/${userId}/forecast/networth?years=${years}`);
}

export async function getGoalForecast(userId: string): Promise<{ goals: any[] }> {
  return apiRequest(`/api/user/${userId}/forecast/goals`);
}

export async function getExpenseForecast(userId: string): Promise<{ categories: any[] }> {
  return apiRequest(`/api/user/${userId}/forecast/expenses`);
}

export async function getSavingsProjection(userId: string): Promise<any> {
  return apiRequest(`/api/user/${userId}/forecast/savings`);
}

export async function getFullReport(userId: string): Promise<any> {
  return apiRequest(`/api/user/${userId}/report`);
}

export async function getUserStocks(userId: string): Promise<any> {
  return apiRequest(`/api/user/${userId}/stocks`);
}

export async function getUserMutualFunds(userId: string): Promise<any> {
  return apiRequest(`/api/user/${userId}/mutual-funds`);
}

export async function getMLForecast(userId: string, steps = 6): Promise<any> {
  return apiRequest(`/api/user/${userId}/forecast/ml?steps=${steps}`);
}

export async function getUserExpenses(userId: string): Promise<{ expenses: any[] }> {
  return apiRequest(`/api/user/${userId}/expenses`);
}

export async function getUserInvestments(userId: string): Promise<any> {
  return apiRequest(`/api/user/${userId}/investments`);
}

export async function getUserGoals(userId: string): Promise<{ goals: any[] }> {
  return apiRequest(`/api/user/${userId}/goals`);
}

export async function getUserRisk(userId: string): Promise<any> {
  return apiRequest(`/api/user/${userId}/risk`);
}

export async function getUserHealth(userId: string): Promise<any> {
  return apiRequest(`/api/user/${userId}/health`);
}

export async function getUserRecommendations(userId: string): Promise<{ recommendations: any[] }> {
  return apiRequest(`/api/user/${userId}/recommendations`);
}

export async function getUserAlerts(userId: string): Promise<{ alerts: any[]; emis: any[] }> {
  return apiRequest(`/api/user/${userId}/alerts`);
}

export async function runSimulation(userId: string, params: {
  new_loan?: number;
  salary_increase?: number;
  job_loss?: boolean;
  vacation_expense?: number;
  house_purchase?: boolean;
  car_purchase?: boolean;
  investment_increase?: number;
}): Promise<any> {
  return apiRequest(`/api/user/${userId}/simulation`, {
    method: "POST",
    body: JSON.stringify(params),
  });
}
