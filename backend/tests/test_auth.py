"""Authentication tests aligned to `/api/v1/auth` routes."""

from datetime import timedelta
from uuid import uuid4
from auth.jwt_handler import JWTHandler


def test_signup_login_refresh_and_profile(client):
    email = f"auth_flow_{uuid4().hex[:8]}@example.com"
    password = "TestPass@123"

    signup = client.post(
        "/api/v1/auth/signup", # Updated path
        json={
            "name": "Auth Flow",
            "email": email,
            "password": password,
            "occupation": "Engineer",
            "age": 25,
            "location": "Chennai",
        },
    )
    assert signup.status_code == 201
    signup_data = signup.json()
    assert signup_data["success"] is True
    assert "access_token" in signup_data
    assert "refresh_token" in signup_data

    login = client.post("/api/v1/auth/login", json={"email": email, "password": password}) # Updated path
    assert login.status_code == 200
    login_data = login.json()
    assert login_data["success"] is True

    profile = client.get(
        "/api/v1/auth/profile", # Updated path
        headers={"Authorization": f"Bearer {login_data['access_token']}"},
    )
    assert profile.status_code == 200
    assert profile.json()["email"] == email

    refresh = client.post("/api/v1/auth/refresh", json={"refresh_token": login_data["refresh_token"]}) # Updated path
    assert refresh.status_code == 200
    assert "access_token" in refresh.json()


def test_jwt_handler_class_wrapper():
    jwt_handler = JWTHandler()
    token = jwt_handler.create_access_token({"sub": "u1", "email": "u1@example.com"})
    assert isinstance(token, str) and token
    decoded = jwt_handler.decode_token(token)
    assert decoded["sub"] == "u1"
