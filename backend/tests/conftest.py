"""
Pytest Configuration and Fixtures
"""

import pytest
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from config import settings


# ── Test Database ──────────────────────────────────────────────────────────

TEST_DATABASE_URL = "sqlite:///./test_aurexis.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# ── Test Client ────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def client():
    """Create a test client"""
    from server import app
    
    # Override database dependency
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
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
    """Get authentication headers"""
    # Create user and login
    response = client.post("/api/login", json={
        "username": sample_user_data["name"],
        "password": sample_user_data["password"]
    })
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        return {"Authorization": f"Bearer {token}"}
    
    return {}
