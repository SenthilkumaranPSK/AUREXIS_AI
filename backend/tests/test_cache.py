"""
Test Cache Module
"""

import pytest
import time
from cache import InMemoryCache, CacheManager, cached


def test_in_memory_cache():
    """Test in-memory cache operations"""
    cache = InMemoryCache()
    
    # Set and get
    cache.set("key1", "value1", ttl=10)
    assert cache.get("key1") == "value1"
    
    # Non-existent key
    assert cache.get("nonexistent") is None
    
    # Exists
    assert cache.exists("key1")
    assert not cache.exists("nonexistent")
    
    # Delete
    cache.delete("key1")
    assert cache.get("key1") is None
    
    # TTL expiry
    cache.set("key2", "value2", ttl=1)
    time.sleep(1.1)
    assert cache.get("key2") is None


def test_cache_manager():
    """Test cache manager"""
    cache = CacheManager()
    
    # Make key
    key = cache.make_key("user", "1010101010", "metrics")
    assert key.startswith("aurexis:")
    assert "user" in key
    assert "1010101010" in key
    
    # Set and get
    cache.set(key, {"data": "test"}, ttl=10)
    assert cache.get(key) == {"data": "test"}
    
    # Clear
    cache.delete(key)
    assert cache.get(key) is None


def test_cached_decorator():
    """Test cached decorator"""
    call_count = 0
    
    @cached(ttl=10, key_prefix="test")
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call - should execute
    result1 = expensive_function(5)
    assert result1 == 10
    assert call_count == 1
    
    # Second call - should use cache
    result2 = expensive_function(5)
    assert result2 == 10
    assert call_count == 1  # Not incremented
    
    # Different argument - should execute
    result3 = expensive_function(10)
    assert result3 == 20
    assert call_count == 2
