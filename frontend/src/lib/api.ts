import { UserProfile } from "@/types/finance";

/**
 * API Client for AUREXIS AI Backend
 * Handles communication between frontend and Python backend
 */

const API_BASE_URL = "http://localhost:8000";

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
 * Send message to ADK agent
 */
export async function sendChatMessage(
  request: ChatRequest
): Promise<ChatResponse> {
  return apiRequest<ChatResponse>("/api/chat", {
    method: "POST",
    body: JSON.stringify(request),
  });
}
