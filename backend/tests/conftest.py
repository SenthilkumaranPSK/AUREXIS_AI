"""
Pytest Configuration and Fixtures
"""
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_app():
    """Create test FastAPI application"""
    # Set test environment
    os.environ["ENVIRONMENT"] = "test"
    os.environ["JWT_SECRET_KEY"] = "test-secret-key"
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    
    from server import app
    return app


@pytest.fixture
def client(test_app) -> Generator:
    """Create test client"""
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture
async def async_client(test_app) -> AsyncGenerator:
    """Create async test client"""
    from httpx import AsyncClient
    
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_user_data():
    """Sample test user data"""
    return {
        "id": "test_user_123",
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPassword123!",
        "occupation": "Software Engineer",
        "monthlyIncome": 100000,
        "monthlyExpense": 60000
    }


@pytest.fixture
def auth_headers(client, test_user_data):
    """Get authentication headers for test user"""
    # Login and get token
    response = client.post("/api/login", json={
        "username": test_user_data["id"],
        "password": test_user_data["password"]
    })
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    return {}


@pytest.fixture
def mock_transactions():
    """Sample transaction data"""
    return [
        {
            "id": "txn_1",
            "amount": 5000,
            "type": "CREDIT",
            "category": "Salary",
            "date": "2026-05-01",
            "description": "Monthly Salary"
        },
        {
            "id": "txn_2",
            "amount": 2000,
            "type": "DEBIT",
            "category": "Groceries",
            "date": "2026-05-02",
            "description": "Supermarket"
        },
        {
            "id": "txn_3",
            "amount": 1500,
            "type": "DEBIT",
            "category": "Utilities",
            "date": "2026-05-03",
            "description": "Electricity Bill"
        }
    ]


@pytest.fixture
def mock_budget():
    """Sample budget data"""
    return {
        "name": "May 2026 Budget",
        "month": "2026-05",
        "total_budget": 50000,
        "categories": [
            {
                "name": "Groceries",
                "budget_amount": 10000,
                "icon": "ShoppingCart",
                "color": "#3b82f6"
            },
            {
                "name": "Utilities",
                "budget_amount": 5000,
                "icon": "Zap",
                "color": "#ef4444"
            },
            {
                "name": "Entertainment",
                "budget_amount": 5000,
                "icon": "Film",
                "color": "#8b5cf6"
            }
        ]
    }


@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Cleanup test data after each test"""
    yield
    # Cleanup code here if needed
    pass
