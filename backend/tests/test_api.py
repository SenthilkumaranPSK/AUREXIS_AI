"""
Test API Endpoints
"""

import pytest


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "online"


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data
    assert "components" in data


def test_metrics_endpoint(client):
    """Test Prometheus metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post("/api/login", json={
        "username": "nonexistent",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_users_list(client):
    """Test users list endpoint"""
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert "count" in data


def test_rate_limiting(client):
    """Test rate limiting"""
    # Make many requests quickly
    responses = []
    for _ in range(70):  # Exceed rate limit
        response = client.get("/")
        responses.append(response.status_code)
    
    # Should have some 429 responses
    assert 429 in responses


def test_cors_headers(client):
    """Test CORS headers"""
    response = client.options("/", headers={
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "GET"
    })
    
    assert "access-control-allow-origin" in response.headers


def test_security_headers(client):
    """Test security headers"""
    response = client.get("/")
    
    assert "x-content-type-options" in response.headers
    assert "x-frame-options" in response.headers
    assert "x-xss-protection" in response.headers


def test_request_id_header(client):
    """Test request ID header"""
    response = client.get("/")
    assert "x-request-id" in response.headers
    assert len(response.headers["x-request-id"]) > 0


def test_process_time_header(client):
    """Test process time header"""
    response = client.get("/")
    assert "x-process-time" in response.headers
    assert "ms" in response.headers["x-process-time"]
