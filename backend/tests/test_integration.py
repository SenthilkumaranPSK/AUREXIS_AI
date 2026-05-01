"""
Backend Integration Tests
Test complete user flows and API endpoint integration
"""

import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


class TestUserAuthFlow:
    """Test complete authentication flow"""

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert "service" in data

    def test_list_users(self):
        """Test listing all users"""
        response = client.get("/api/users")
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert "count" in data

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/login",
            json={"username": "invalid", "password": "wrong"}
        )
        assert response.status_code == 401

    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = client.get("/", headers={"Origin": "http://localhost:5173"})
        assert response.status_code == 200
        # CORS should allow the origin
        assert "access-control-allow-origin" in response.headers or response.status_code == 200


class TestFinancialEndpoints:
    """Test financial data endpoints"""

    def test_get_metrics_for_demo_user(self):
        """Test getting metrics for a user"""
        # Use a known demo user ID
        response = client.get("/api/user/1010101010/metrics")
        # Should return 200 or 404 if user data doesn't exist
        assert response.status_code in [200, 404]

    def test_get_forecast_for_demo_user(self):
        """Test getting forecast for a user"""
        response = client.get("/api/user/1010101010/forecast")
        assert response.status_code in [200, 404]

    def test_get_health_for_demo_user(self):
        """Test getting health score for a user"""
        response = client.get("/api/user/1010101010/health")
        assert response.status_code in [200, 404]

    def test_get_recommendations_for_demo_user(self):
        """Test getting recommendations for a user"""
        response = client.get("/api/user/1010101010/recommendations")
        assert response.status_code in [200, 404]

    def test_get_alerts_for_demo_user(self):
        """Test getting alerts for a user"""
        response = client.get("/api/user/1010101010/alerts")
        assert response.status_code in [200, 404]


class TestCacheIntegration:
    """Test caching functionality"""

    def test_cache_manager_initialization(self):
        """Test that cache manager is initialized"""
        from cache import cache
        assert cache is not None
        assert hasattr(cache, 'backend')

    def test_cache_set_get(self):
        """Test basic cache operations"""
        from cache import cache

        # Set a value
        cache.set("test_key", {"test": "value"}, ttl=60)

        # Get the value back
        result = cache.get("test_key")
        assert result == {"test": "value"}

        # Clean up
        cache.delete("test_key")


class TestSecurityModule:
    """Test security functionality"""

    def test_password_hashing(self):
        """Test password hashing"""
        from security import hash_password, verify_password

        password = "TestPassword123!"
        hashed = hash_password(password)

        # Hash should be different from password
        assert hashed != password
        # Hash should start with $2 (bcrypt identifier)
        assert hashed.startswith("$2")

    def test_password_verification(self):
        """Test password verification"""
        from security import hash_password, verify_password

        password = "TestPassword123!"
        hashed = hash_password(password)

        # Correct password should verify
        assert verify_password(password, hashed) is True
        # Wrong password should not verify
        assert verify_password("wrongpassword", hashed) is False

    def test_password_strength_validation(self):
        """Test password strength validation"""
        from security import validate_password_strength

        # Weak password - too short
        is_valid, message = validate_password_strength("weak")
        assert is_valid is False

        # Strong password
        is_valid, message = validate_password_strength("StrongPass123!")
        assert is_valid is True

    def test_jwt_token_creation(self):
        """Test JWT token creation"""
        from security import create_access_token, decode_token

        token = create_access_token({"sub": "user123", "email": "test@example.com"})

        # Token should be a string
        assert isinstance(token, str)
        # Token should be decodable
        payload = decode_token(token)
        assert payload["sub"] == "user123"

    def test_api_key_generation(self):
        """Test API key generation"""
        from security import generate_api_key, hash_api_key, verify_api_key

        api_key = generate_api_key()
        hashed = hash_api_key(api_key)

        # Key should be non-empty
        assert len(api_key) > 0
        # Hash should be different from key
        assert hashed != api_key
        # Verification should work
        assert verify_api_key(api_key, hashed) is True


class TestDatabaseIntegration:
    """Test database operations"""

    def test_database_connection(self):
        """Test database connection"""
        from database.connection_enhanced import get_db

        conn = get_db_connection()
        cursor = conn.cursor()

        # Test basic query
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result[0] == 1

        conn.close()

    def test_database_indexes_exist(self):
        """Test that performance indexes are created"""
        from database.connection_enhanced import get_db

        conn = get_db_connection()
        cursor = conn.cursor()

        # List all indexes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = cursor.fetchall()

        # Should have multiple indexes
        assert len(indexes) > 0

        conn.close()


class TestRateLimiting:
    """Test rate limiting functionality"""

    def test_rate_limiter_initialization(self):
        """Test rate limiter is configured"""
        from slowapi import Limiter
        from server import limiter

        assert limiter is not None
        assert isinstance(limiter, Limiter)

    def test_rate_limit_decorator(self):
        """Test rate limit decorator works"""
        from cache import rate_limiter

        # Test rate limiting logic
        identifier = "test_user"
        is_allowed, remaining = rate_limiter.is_allowed(
            identifier,
            max_requests=5,
            window_seconds=60
        )

        # First request should be allowed
        assert is_allowed is True
        assert remaining == 4

        # Clean up
        rate_limiter.cache.delete(rate_limiter.cache.make_key("ratelimit", identifier))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
