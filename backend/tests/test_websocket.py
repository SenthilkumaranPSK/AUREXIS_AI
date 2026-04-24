"""WebSocket smoke tests aligned with current auth and ws protocol."""

from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


@pytest.fixture
def auth_token():
    email = f"wstest_{uuid4().hex[:8]}@example.com"
    password = "TestPass@123"
    client.post(
        "/api/auth/signup",
        json={"name": "WebSocket Test", "email": email, "password": password},
    )
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    if response.status_code != 200:
        pytest.skip("Unable to authenticate websocket test user")
    return response.json()["access_token"]


def test_websocket_requires_token():
    with pytest.raises(Exception):
        with client.websocket_connect("/ws"):
            pass


def test_websocket_connect_and_ping(auth_token):
    with client.websocket_connect(f"/ws?token={auth_token}") as websocket:
        welcome = websocket.receive_json()
        assert welcome["type"] == "connected"
        websocket.send_json({"type": "ping"})
        pong = websocket.receive_json()
        assert pong["type"] == "pong"
