/**
 * Custom hook for handling async operations with loading, error states
 */
import { useState, useEffect, useCallback, useRef } from 'react';

interface UseAsyncOptions<T> {
  immediate?: boolean;
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
  retry?: number;
  retryDelay?: number;
}

interface UseAsyncReturn<T, Args extends any[]> {
  data: T | null;
  error: Error | null;
  loading: boolean;
  execute: (...args: Args) => Promise<T | null>;
  reset: () => void;
  retry: () => Promise<T | null>;
}

export function useAsync<T, Args extends any[] = []>(
  asyncFunction: (...args: Args) => Promise<T>,
  options: UseAsyncOptions<T> = {}
): UseAsyncReturn<T, Args> {
  const {
    immediate = false,
    onSuccess,
    onError,
    retry: maxRetries = 0,
    retryDelay = 1000,
  } = options;

  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(immediate);

  const lastArgsRef = useRef<Args | null>(null);
  const mountedRef = useRef(true);
  const retriesRef = useRef(0);

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
    };
  }, []);

  const execute = useCallback(
    async (...args: Args): Promise<T | null> => {
      lastArgsRef.current = args;
      setLoading(true);
      setError(null);

      try {
        const result = await asyncFunction(...args);
        
        if (mountedRef.current) {
          setData(result);
          setLoading(false);
          retriesRef.current = 0;
          
          if (onSuccess) {
            onSuccess(result);
          }
        }
        
        return result;
      } catch (err) {
        const error = err instanceof Error ? err : new Error(String(err));
        
        if (mountedRef.current) {
          // Retry logic
          if (retriesRef.current < maxRetries) {
            retriesRef.current++;
            await new Promise(resolve => setTimeout(resolve, retryDelay * retriesRef.current));
            return execute(...args);
          }

          setError(error);
          setLoading(false);
          
          if (onError) {
            onError(error);
          }
        }
        
        return null;
      }
    },
    [asyncFunction, onSuccess, onError, maxRetries, retryDelay]
  );

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
    retriesRef.current = 0;
  }, []);

  const retryFn = useCallback(async (): Promise<T | null> => {
    if (lastArgsRef.current) {
      retriesRef.current = 0;
      return execute(...lastArgsRef.current);
    }
    return null;
  }, [execute]);

  useEffect(() => {
    if (immediate) {
      execute([] as any as Args);
    }
  }, []);

  return {
    data,
    error,
    loading,
    execute,
    reset,
    retry: retryFn,
  };
}

/**
 * Hook for data fetching with caching
 */
interface UseFetchOptions<T> extends UseAsyncOptions<T> {
  cache?: boolean;
  cacheTTL?: number;
  refetchInterval?: number;
}

const fetchCache = new Map<string, { data: any; timestamp: number; ttl: number }>();

export function useFetch<T>(
  key: string,
  fetcher: () => Promise<T>,
  options: UseFetchOptions<T> = {}
): UseAsyncReturn<T, []> & { refetch: () => Promise<T | null> } {
  const {
    cache = true,
    cacheTTL = 300000, // 5 minutes
    refetchInterval,
    ...asyncOptions
  } = options;

  // Check cache
  const getCachedData = useCallback((): T | null => {
    if (!cache) return null;

    const cached = fetchCache.get(key);
    if (!cached) return null;

    const isExpired = Date.now() - cached.timestamp > cached.ttl;
    if (isExpired) {
      fetchCache.delete(key);
      return null;
    }

    return cached.data;
  }, [key, cache]);

  // Wrapper that checks cache first
  const fetchWithCache = useCallback(async (): Promise<T> => {
    const cached = getCachedData();
    if (cached !== null) {
      return cached;
    }

    const data = await fetcher();

    if (cache) {
      fetchCache.set(key, {
        data,
        timestamp: Date.now(),
        ttl: cacheTTL,
      });
    }

    return data;
  }, [fetcher, getCachedData, cache, key, cacheTTL]);

  const asyncResult = useAsync(fetchWithCache, {
    ...asyncOptions,
    immediate: true,
  });

  // Auto refetch interval
  useEffect(() => {
    if (!refetchInterval) return;

    const interval = setInterval(() => {
      asyncResult.execute();
    }, refetchInterval);

    return () => clearInterval(interval);
  }, [refetchInterval, asyncResult.execute]);

  const refetch = useCallback(async (): Promise<T | null> => {
    // Clear cache and refetch
    fetchCache.delete(key);
    return asyncResult.execute();
  }, [key, asyncResult.execute]);

  return {
    ...asyncResult,
    refetch,
  };
}

/**
 * Clear all fetch cache
 */
export function clearFetchCache(): void {
  fetchCache.clear();
}

/**
 * Clear specific cache entry
 */
export function clearCacheEntry(key: string): void {
  fetchCache.delete(key);
}
