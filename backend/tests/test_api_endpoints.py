"""
API Endpoint Tests
"""
import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns system info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "app_name" in data
        assert "version" in data
    
    def test_health_endpoint(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestAuthEndpoints:
    """Test authentication endpoints"""
    
    def test_login_success(self, client: TestClient):
        """Test successful login"""
        response = client.post("/api/login", json={
            "username": "22243045",
            "password": "Senthilkumaran@2000"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
    
    def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials"""
        response = client.post("/api/login", json={
            "username": "invalid_user",
            "password": "wrong_password"
        })
        assert response.status_code == 401
    
    def test_login_missing_fields(self, client: TestClient):
        """Test login with missing fields"""
        response = client.post("/api/login", json={
            "username": "test_user"
        })
        assert response.status_code == 422


class TestFinancialEndpoints:
    """Test financial data endpoints"""
    
    def test_get_metrics_unauthorized(self, client: TestClient):
        """Test metrics endpoint without authentication"""
        response = client.get("/api/financial/metrics")
        assert response.status_code == 401
    
    def test_get_metrics_authorized(self, client: TestClient, auth_headers):
        """Test metrics endpoint with authentication"""
        if not auth_headers:
            pytest.skip("Authentication not available")
        
        response = client.get("/api/financial/metrics", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "monthly_income" in data or "error" not in data
    
    def test_get_expenses(self, client: TestClient, auth_headers):
        """Test expenses endpoint"""
        if not auth_headers:
            pytest.skip("Authentication not available")
        
        response = client.get("/api/financial/expenses", headers=auth_headers)
        assert response.status_code in [200, 404]


class TestValidation:
    """Test input validation"""
    
    def test_invalid_json(self, client: TestClient):
        """Test endpoint with invalid JSON"""
        response = client.post(
            "/api/login",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self, client: TestClient):
        """Test endpoint with missing required fields"""
        response = client.post("/api/login", json={})
        assert response.status_code == 422


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_not_found(self, client: TestClient):
        """Test 404 error handling"""
        response = client.get("/api/nonexistent/endpoint")
        assert response.status_code == 404
    
    def test_405_method_not_allowed(self, client: TestClient):
        """Test 405 error handling"""
        response = client.put("/")
        assert response.status_code == 405


@pytest.mark.asyncio
class TestAsyncEndpoints:
    """Test async endpoint behavior"""
    
    async def test_concurrent_requests(self, async_client):
        """Test handling of concurrent requests"""
        import asyncio
        
        # Make multiple concurrent requests
        tasks = [
            async_client.get("/health")
            for _ in range(10)
        ]
        
        responses = await asyncio.gather(*tasks)
        
        # All should succeed
        assert all(r.status_code == 200 for r in responses)
