"""
Pytest configuration and shared fixtures.
"""

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from typing import Generator, Dict  # Import Dict for type hinting

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import app from main
from main import app

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """Create a test client for FastAPI app."""
    # The client fixture needs to yield exactly once.
    # This ensures that the TestClient is properly created and used.
    with TestClient(app) as client:
        yield client

# --- Helper Functions ---

def get_auth_headers(client: TestClient, email: str, password: str) -> Dict[str, str]:
    """Login and get authorization headers."""
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    
    token = response.json().get("access_token") if response.status_code == 200 else ""
    return {"Authorization": f"Bearer {token}"} if token else {}



@pytest.fixture
def sample_financial_data() -> Dict:
    """Minimal financial data for analytics tests.
    Expected values:
    - income = 50000
    - expense = 25000 (20000 + 5000)
    - net worth = 500000
    - credit score = 750
    """
    return {
        "fetch_bank_transactions": {
            "bankTransactions": [
                {
                    "bank": "TestBank",
                    "txns": [
                        [50000, "Salary Credit", "2025-01-01", 1, "NEFT", "ref1"],
                        [20000, "Rent Payment", "2025-01-02", 2, "FT", "ref2"],
                        [5000, "Utility Bill", "2025-01-03", 2, "UPI", "ref3"]
                    ]
                }
            ]
        },
        "fetch_net_worth": {
            "netWorthResponse": {"totalNetWorthValue": {"units": 500000}}
        },
        "fetch_credit_report": {
            "creditReports": [{"creditReportData": {"score": {"bureauScore": 750}}}]
        }
    }
