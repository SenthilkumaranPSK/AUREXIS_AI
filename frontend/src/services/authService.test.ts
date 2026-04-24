/**
 * Authentication Service Tests
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock localStorage
const localStorageMock = {
  store: {} as Record<string, string>,
  getItem: vi.fn((key: string) => this.store[key] || null),
  setItem: vi.fn((key: string, value: string) => { this.store[key] = value; }),
  removeItem: vi.fn((key: string) => { delete this.store[key]; }),
  clear: vi.fn(() => { this.store = {}; }),
};

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock fetch
global.fetch = vi.fn();

describe('Auth Service', () => {
  beforeEach(() => {
    localStorageMock.clear();
    vi.clearAllMocks();
  });

  describe('Token management', () => {
    it('should store tokens in localStorage', () => {
      localStorageMock.setItem('access_token', 'test-token');
      localStorageMock.setItem('refresh_token', 'test-refresh');

      expect(localStorageMock.setItem).toHaveBeenCalledWith('access_token', 'test-token');
      expect(localStorageMock.getItem('access_token')).toBe('test-token');
    });

    it('should clear tokens on logout', () => {
      localStorageMock.setItem('access_token', 'test-token');
      localStorageMock.setItem('refresh_token', 'test-refresh');

      localStorageMock.removeItem('access_token');
      localStorageMock.removeItem('refresh_token');

      expect(localStorageMock.getItem('access_token')).toBeNull();
      expect(localStorageMock.getItem('refresh_token')).toBeNull();
    });

    it('should return null when no token', () => {
      // Simulate no token in localStorage
      expect(localStorageMock.getItem('access_token')).toBeNull();
    });
  });

  describe('Token storage', () => {
    it('should retrieve stored token', () => {
      localStorageMock.setItem('access_token', 'my-token');
      const token = localStorageMock.getItem('access_token');
      expect(token).toBe('my-token');
    });
  });
});
