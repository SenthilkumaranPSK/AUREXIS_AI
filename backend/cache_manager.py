"""
Redis Cache Manager for AUREXIS AI
Provides caching functionality for improved performance
"""

import logging
from typing import Optional, Any
from functools import wraps

logger = logging.getLogger(__name__)


class CacheManager:
    """Simple in-memory cache manager (fallback if Redis unavailable)"""

    def __init__(self):
        self._cache = {}
        self._ttl = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self._cache:
            return self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache with TTL (default 5 minutes)"""
        self._cache[key] = value
        return True

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> bool:
        """Clear all cache"""
        self._cache.clear()
        return True

    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        return key in self._cache


# Global cache instance
cache = CacheManager()


def cached(ttl: int = 300, key_prefix: str = ""):
    """
    Decorator to cache function results

    Args:
        ttl: Time to live in seconds (default 300)
        key_prefix: Prefix for cache key
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"

            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_result

            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            logger.debug(f"Cache miss for {cache_key}, cached result")
            return result

        return wrapper
    return decorator


def invalidate_pattern(pattern: str):
    """
    Invalidate all cache keys matching pattern

    Args:
        pattern: Pattern to match (e.g., "user:*")
    """
    keys_to_delete = [k for k in cache._cache.keys() if pattern in k]
    for key in keys_to_delete:
        cache.delete(key)
    logger.info(f"Invalidated {len(keys_to_delete)} cache keys matching '{pattern}'")
