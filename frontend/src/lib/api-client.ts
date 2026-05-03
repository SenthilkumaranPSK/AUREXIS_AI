/**
 * Enhanced API Client with Retry Logic, Caching, and Error Handling
 */

interface RequestConfig extends RequestInit {
  retry?: number;
  retryDelay?: number;
  timeout?: number;
  cache?: boolean;
  cacheTTL?: number;
}

interface CacheEntry {
  data: any;
  timestamp: number;
  ttl: number;
}

class APIClient {
  private baseURL: string;
  private cache: Map<string, CacheEntry>;
  private defaultTimeout: number = 30000; // 30 seconds
  private defaultRetries: number = 3;
  private defaultRetryDelay: number = 1000; // 1 second

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    this.cache = new Map();
    
    // Clear expired cache entries every minute
    setInterval(() => this.clearExpiredCache(), 60000);
  }

  /**
   * Make HTTP request with retry logic and caching
   */
  async request<T = any>(
    endpoint: string,
    config: RequestConfig = {}
  ): Promise<T> {
    const {
      retry = this.defaultRetries,
      retryDelay = this.defaultRetryDelay,
      timeout = this.defaultTimeout,
      cache = false,
      cacheTTL = 300000, // 5 minutes
      ...fetchConfig
    } = config;

    const url = `${this.baseURL}${endpoint}`;
    const cacheKey = this.getCacheKey(url, fetchConfig);

    // Check cache for GET requests
    if (cache && fetchConfig.method === 'GET') {
      const cached = this.getFromCache(cacheKey);
      if (cached) {
        return cached;
      }
    }

    let lastError: Error | null = null;
    let attempt = 0;

    while (attempt <= retry) {
      try {
        const response = await this.fetchWithTimeout(url, fetchConfig, timeout);
        
        if (!response.ok) {
          throw await this.handleErrorResponse(response);
        }

        const data = await response.json();

        // Cache successful GET requests
        if (cache && fetchConfig.method === 'GET') {
          this.setCache(cacheKey, data, cacheTTL);
        }

        return data;
      } catch (error) {
        lastError = error as Error;
        attempt++;

        // Don't retry on client errors (4xx) except 429 (rate limit)
        if (error instanceof APIError && error.status >= 400 && error.status < 500 && error.status !== 429) {
          throw error;
        }

        // Don't retry if no more attempts left
        if (attempt > retry) {
          break;
        }

        // Exponential backoff
        const delay = retryDelay * Math.pow(2, attempt - 1);
        await this.sleep(delay);
      }
    }

    throw lastError || new Error('Request failed after retries');
  }

  /**
   * GET request
   */
  async get<T = any>(endpoint: string, config: RequestConfig = {}): Promise<T> {
    return this.request<T>(endpoint, {
      ...config,
      method: 'GET',
      cache: config.cache !== false, // Cache by default for GET
    });
  }

  /**
   * POST request
   */
  async post<T = any>(endpoint: string, data?: any, config: RequestConfig = {}): Promise<T> {
    return this.request<T>(endpoint, {
      ...config,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...config.headers,
      },
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * PUT request
   */
  async put<T = any>(endpoint: string, data?: any, config: RequestConfig = {}): Promise<T> {
    return this.request<T>(endpoint, {
      ...config,
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...config.headers,
      },
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * DELETE request
   */
  async delete<T = any>(endpoint: string, config: RequestConfig = {}): Promise<T> {
    return this.request<T>(endpoint, {
      ...config,
      method: 'DELETE',
    });
  }

  /**
   * PATCH request
   */
  async patch<T = any>(endpoint: string, data?: any, config: RequestConfig = {}): Promise<T> {
    return this.request<T>(endpoint, {
      ...config,
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        ...config.headers,
      },
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * Fetch with timeout
   */
  private async fetchWithTimeout(
    url: string,
    config: RequestInit,
    timeout: number
  ): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        ...config,
        signal: controller.signal,
      });
      return response;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  /**
   * Handle error response
   */
  private async handleErrorResponse(response: Response): Promise<APIError> {
    let errorData: any;
    
    try {
      errorData = await response.json();
    } catch {
      errorData = { message: response.statusText };
    }

    return new APIError(
      errorData.error?.message || errorData.message || 'Request failed',
      response.status,
      errorData.error?.details || errorData.details
    );
  }

  /**
   * Cache management
   */
  private getCacheKey(url: string, config: RequestInit): string {
    return `${url}_${JSON.stringify(config.headers || {})}`;
  }

  private getFromCache(key: string): any | null {
    const entry = this.cache.get(key);
    
    if (!entry) {
      return null;
    }

    // Check if expired
    if (Date.now() - entry.timestamp > entry.ttl) {
      this.cache.delete(key);
      return null;
    }

    return entry.data;
  }

  private setCache(key: string, data: any, ttl: number): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl,
    });
  }

  private clearExpiredCache(): void {
    const now = Date.now();
    
    for (const [key, entry] of this.cache.entries()) {
      if (now - entry.timestamp > entry.ttl) {
        this.cache.delete(key);
      }
    }
  }

  /**
   * Clear all cache
   */
  clearCache(): void {
    this.cache.clear();
  }

  /**
   * Clear specific cache entry
   */
  clearCacheEntry(endpoint: string): void {
    const url = `${this.baseURL}${endpoint}`;
    
    for (const key of this.cache.keys()) {
      if (key.startsWith(url)) {
        this.cache.delete(key);
      }
    }
  }

  /**
   * Sleep utility
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Set authorization token
   */
  setAuthToken(token: string): void {
    this.defaultHeaders = {
      ...this.defaultHeaders,
      Authorization: `Bearer ${token}`,
    };
  }

  /**
   * Remove authorization token
   */
  clearAuthToken(): void {
    const { Authorization, ...rest } = this.defaultHeaders;
    this.defaultHeaders = rest;
  }

  private defaultHeaders: Record<string, string> = {};

  /**
   * Get default headers
   */
  private getHeaders(customHeaders?: HeadersInit): HeadersInit {
    return {
      ...this.defaultHeaders,
      ...customHeaders,
    };
  }
}

/**
 * Custom API Error class
 */
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public details?: any
  ) {
    super(message);
    this.name = 'APIError';
  }

  get isClientError(): boolean {
    return this.status >= 400 && this.status < 500;
  }

  get isServerError(): boolean {
    return this.status >= 500;
  }

  get isAuthError(): boolean {
    return this.status === 401 || this.status === 403;
  }

  get isNotFound(): boolean {
    return this.status === 404;
  }

  get isValidationError(): boolean {
    return this.status === 422;
  }

  get isRateLimitError(): boolean {
    return this.status === 429;
  }
}

// Create and export API client instance
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const apiClient = new APIClient(API_BASE_URL);

// Export for testing or custom instances
export { APIClient };
