"""
AUREXIS AI — Caching Layer
Redis-based caching with fallback to in-memory cache
"""

import json
import pickle
from typing import Any, Optional, Callable
from datetime import datetime, timedelta
from functools import wraps
import hashlib

from config import settings
from logger import logger

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available, using in-memory cache")


# ── Cache Backends ─────────────────────────────────────────────────────────

class InMemoryCache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self):
        self._cache = {}
        self._expiry = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self._cache:
            if key in self._expiry and datetime.now() > self._expiry[key]:
                # Expired
                del self._cache[key]
                del self._expiry[key]
                return None
            return self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL in seconds"""
        self._cache[key] = value
        self._expiry[key] = datetime.now() + timedelta(seconds=ttl)
    
    def delete(self, key: str):
        """Delete key from cache"""
        self._cache.pop(key, None)
        self._expiry.pop(key, None)
    
    def clear(self):
        """Clear all cache"""
        self._cache.clear()
        self._expiry.clear()
    
    def exists(self, key: str) -> bool:
        """Check if key exists and is not expired"""
        return self.get(key) is not None


class RedisCache:
    """Redis-based cache"""
    
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=False,  # We'll handle encoding
        )
        # Test connection
        try:
            self.client.ping()
            logger.info("Redis cache connected successfully")
        except redis.ConnectionError:
            logger.error("Failed to connect to Redis")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.client.get(key)
            if value:
                return pickle.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL in seconds"""
        try:
            serialized = pickle.dumps(value)
            self.client.setex(key, ttl, serialized)
        except Exception as e:
            logger.error(f"Redis set error: {e}")
    
    def delete(self, key: str):
        """Delete key from cache"""
        try:
            self.client.delete(key)
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
    
    def clear(self):
        """Clear all cache (use with caution!)"""
        try:
            self.client.flushdb()
        except Exception as e:
            logger.error(f"Redis clear error: {e}")
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Redis exists error: {e}")
            return False
    
    def increment(self, key: str, amount: int = 1) -> int:
        """Increment a counter"""
        try:
            return self.client.incrby(key, amount)
        except Exception as e:
            logger.error(f"Redis increment error: {e}")
            return 0
    
    def expire(self, key: str, ttl: int):
        """Set expiry on existing key"""
        try:
            self.client.expire(key, ttl)
        except Exception as e:
            logger.error(f"Redis expire error: {e}")


# ── Cache Manager ──────────────────────────────────────────────────────────

class CacheManager:
    """Unified cache manager with automatic backend selection"""
    
    def __init__(self):
        if settings.CACHE_ENABLED and REDIS_AVAILABLE:
            try:
                self.backend = RedisCache()
                self.backend_name = "Redis"
            except Exception as e:
                logger.warning(f"Redis initialization failed: {e}, falling back to in-memory cache")
                self.backend = InMemoryCache()
                self.backend_name = "InMemory"
        else:
            self.backend = InMemoryCache()
            self.backend_name = "InMemory"
        
        logger.info(f"Cache backend: {self.backend_name}")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        return self.backend.get(key)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        if ttl is None:
            ttl = settings.CACHE_TTL
        self.backend.set(key, value, ttl)
    
    def delete(self, key: str):
        """Delete key from cache"""
        self.backend.delete(key)
    
    def clear(self):
        """Clear all cache"""
        self.backend.clear()
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        return self.backend.exists(key)
    
    def make_key(self, *parts) -> str:
        """Generate cache key from parts"""
        key_str = ":".join(str(p) for p in parts)
        return f"aurexis:{key_str}"
    
    def make_hash_key(self, *parts) -> str:
        """Generate hashed cache key for long keys"""
        key_str = ":".join(str(p) for p in parts)
        hash_val = hashlib.md5(key_str.encode()).hexdigest()
        return f"aurexis:hash:{hash_val}"


# Global cache instance
cache = CacheManager()


# ── Cache Decorators ───────────────────────────────────────────────────────

def cached(
    ttl: Optional[int] = None,
    key_prefix: str = "",
    key_func: Optional[Callable] = None
):
    """
    Decorator to cache function results
    
    Usage:
        @cached(ttl=3600, key_prefix="metrics")
        def compute_metrics(user_id: str):
            # expensive computation
            return result
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default: use function name and arguments
                key_parts = [key_prefix or func.__name__]
                key_parts.extend(str(arg) for arg in args)
                key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
                cache_key = cache.make_key(*key_parts)
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_value
            
            # Compute and cache
            logger.debug(f"Cache miss: {cache_key}")
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        
        return wrapper
    return decorator


def cache_user_data(user_id: str, data_type: str, data: Any, ttl: int = 3600):
    """Cache user financial data"""
    key = cache.make_key("user_data", user_id, data_type)
    cache.set(key, data, ttl)


def get_cached_user_data(user_id: str, data_type: str) -> Optional[Any]:
    """Get cached user financial data"""
    key = cache.make_key("user_data", user_id, data_type)
    return cache.get(key)


def invalidate_user_cache(user_id: str):
    """Invalidate all cache for a user"""
    # Note: This is a simple implementation
    # For production, use Redis SCAN with pattern matching
    patterns = ["user_data", "metrics", "forecast", "analytics"]
    for pattern in patterns:
        key = cache.make_key(pattern, user_id, "*")
        cache.delete(key)


# ── Rate Limiting ──────────────────────────────────────────────────────────

class RateLimiter:
    """Simple rate limiter using cache backend"""
    
    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
    
    def is_allowed(
        self,
        identifier: str,
        max_requests: int,
        window_seconds: int
    ) -> tuple[bool, int]:
        """
        Check if request is allowed under rate limit
        Returns: (is_allowed, remaining_requests)
        """
        key = self.cache.make_key("ratelimit", identifier)
        
        # Get current count
        current = self.cache.get(key)
        if current is None:
            current = 0
        
        if current >= max_requests:
            return False, 0
        
        # Increment counter
        new_count = current + 1
        self.cache.set(key, new_count, window_seconds)
        
        remaining = max_requests - new_count
        return True, remaining


# Global rate limiter
rate_limiter = RateLimiter(cache)
