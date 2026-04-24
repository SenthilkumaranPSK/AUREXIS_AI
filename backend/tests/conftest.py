"""Pytest configuration and shared fixtures."""

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="module")
def client():
    """Create a test client for FastAPI app."""
    from server import app

    with TestClient(app) as test_client:
        yield test_client


# ── Sample Data ────────────────────────────────────────────────────────────

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "id": "1010101010",
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPass@123",
        "occupation": "Software Engineer",
        "age": 25,
        "location": "Test City",
    }


@pytest.fixture
def sample_financial_data():
    """Sample financial data for testing"""
    return {
        "fetch_bank_transactions": {
            "bankTransactions": [{
                "bank": "Test Bank",
                "txns": [
                    ["50000", "SALARY", "2024-01-01", 1, "NEFT", "50000"],
                    ["20000", "RENT", "2024-01-02", 2, "UPI", "30000"],
                    ["5000", "GROCERIES", "2024-01-05", 2, "UPI", "25000"],
                ]
            }]
        },
        "fetch_net_worth": {
            "netWorthResponse": {
                "totalNetWorthValue": {"units": "500000"}
            }
        },
        "fetch_credit_report": {
            "creditReports": [{
                "creditReportData": {
                    "score": {"bureauScore": "750"}
                }
            }]
        }
    }


@pytest.fixture
def auth_headers(client, sample_user_data):
    """Create auth token and return headers for protected routes."""
    email = sample_user_data["email"]
    password = sample_user_data["password"]

    client.post(
        "/api/auth/signup",
        json={
            "name": sample_user_data["name"],
            "email": email,
            "password": password,
            "occupation": sample_user_data["occupation"],
            "age": sample_user_data["age"],
            "location": sample_user_data["location"],
        },
    )
    response = client.post("/api/auth/login", json={"email": email, "password": password})

    token = response.json().get("access_token") if response.status_code == 200 else ""
    return {"Authorization": f"Bearer {token}"} if token else {}
