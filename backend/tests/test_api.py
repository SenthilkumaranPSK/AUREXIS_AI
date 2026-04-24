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
    response = client.post("/api/login", json={"username": "nonexistent", "password": "wrongpassword"})
    assert response.status_code == 401


def test_users_list(client):
    response = client.get("/api/users")
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
