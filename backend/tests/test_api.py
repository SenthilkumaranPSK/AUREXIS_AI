"""Core API smoke tests for currently available endpoints."""


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code in (200, 429)
    if response.status_code == 200:
        data = response.json()
        assert data.get("status") == "online"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy"
    assert "components" in data


def test_login_invalid_credentials(client):
    # Assuming login is now under v1 auth route
    response = client.post("/api/v1/auth/login", json={"username": "nonexistent", "password": "wrongpassword"})
    assert response.status_code == 401


def test_users_list(client):
    # Assuming users list is now under v1, adjust path if necessary.
    # If no direct /api/v1/users route, this might need to be adapted or removed.
    # For now, assuming it maps to a v1 equivalent or checking for a placeholder.
    # If /api/users is truly legacy and removed, this test would fail appropriately.
    response = client.get("/api/v1/users") # Changed to /api/v1/users
    assert response.status_code == 200
    payload = response.json()
    assert "users" in payload and "count" in payload


def test_cors_headers(client):
    response = client.options(
        "/",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"},
    )
    assert "access-control-allow-origin" in response.headers


def test_process_time_header_exists(client):
    response = client.get("/health")
    assert "x-process-time" in response.headers
