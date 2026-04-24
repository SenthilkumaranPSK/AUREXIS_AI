"""
Caching Middleware

Caches GET requests for improved performance.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import hashlib
import json
from typing import Optional
import time

# Simple in-memory cache
_cache = {}
_cache_timestamps = {}

# Cache configuration
CACHE_TTL = 300  # 5 minutes
MAX_CACHE_SIZE = 1000  # Maximum number of cached items


class CachingMiddleware(BaseHTTPMiddleware):
    """Middleware to cache GET requests"""
    
    # Paths to cache
    CACHEABLE_PATHS = [
        "/api/user/",
        "/api/forecast/",
        "/api/analytics/",
        "/api/ml/",
        "/health",
    ]
    
    # Paths to never cache
    EXCLUDE_PATHS = [
        "/api/auth/",
        "/api/chat/",
        "/ws",
    ]
    
    async def dispatch(self, request: Request, call_next):
        # Only cache GET requests
        if request.method != "GET":
            return await call_next(request)
        
        path = request.url.path
        
        # Check if path should be cached
        should_cache = any(path.startswith(p) for p in self.CACHEABLE_PATHS)
        should_exclude = any(path.startswith(p) for p in self.EXCLUDE_PATHS)
        
        if not should_cache or should_exclude:
            return await call_next(request)
        
        # Generate cache key
        cache_key = self._generate_cache_key(request)
        
        # Check if cached response exists and is still valid
        cached_response = self._get_cached_response(cache_key)
        if cached_response:
            # Return cached response
            return Response(
                content=cached_response["content"],
                status_code=cached_response["status_code"],
                headers={
                    **cached_response["headers"],
                    "X-Cache": "HIT",
                    "X-Cache-Age": str(int(time.time() - _cache_timestamps.get(cache_key, 0)))
                },
                media_type=cached_response["media_type"]
            )
        
        # Process request
        response = await call_next(request)
        
        # Cache successful responses
        if response.status_code == 200:
            # Read response body
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            
            # Cache the response
            self._cache_response(cache_key, {
                "content": body,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "media_type": response.media_type
            })
            
            # Return response with cache miss header
            return Response(
                content=body,
                status_code=response.status_code,
                headers={
                    **dict(response.headers),
                    "X-Cache": "MISS"
                },
                media_type=response.media_type
            )
        
        return response
    
    def _generate_cache_key(self, request: Request) -> str:
        """Generate a unique cache key for the request"""
        # Include path, query params, and auth header in cache key
        key_parts = [
            request.url.path,
            str(request.url.query),
            request.headers.get("authorization", "")
        ]
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_cached_response(self, cache_key: str) -> Optional[dict]:
        """Get cached response if it exists and is still valid"""
        if cache_key not in _cache:
            return None
        
        # Check if cache is expired
        timestamp = _cache_timestamps.get(cache_key, 0)
        if time.time() - timestamp > CACHE_TTL:
            # Cache expired, remove it
            del _cache[cache_key]
            del _cache_timestamps[cache_key]
            return None
        
        return _cache[cache_key]
    
    def _cache_response(self, cache_key: str, response_data: dict):
        """Cache a response"""
        # Check cache size limit
        if len(_cache) >= MAX_CACHE_SIZE:
            # Remove oldest entry
            oldest_key = min(_cache_timestamps, key=_cache_timestamps.get)
            del _cache[oldest_key]
            del _cache_timestamps[oldest_key]
        
        _cache[cache_key] = response_data
        _cache_timestamps[cache_key] = time.time()


def clear_cache():
    """Clear all cached responses"""
    _cache.clear()
    _cache_timestamps.clear()


def get_cache_stats():
    """Get cache statistics"""
    return {
        "size": len(_cache),
        "max_size": MAX_CACHE_SIZE,
        "ttl": CACHE_TTL,
        "oldest_entry_age": int(time.time() - min(_cache_timestamps.values())) if _cache_timestamps else 0
    }
