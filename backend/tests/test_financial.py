"""Financial route tests aligned to `/api/financial` APIs."""

from datetime import date
from uuid import uuid4


def _create_user_and_get_headers(client):
    email = f"fin_flow_{uuid4().hex[:8]}@example.com"
    password = "TestPass@123"
    client.post(
        "/api/auth/signup",
        json={
            "name": "Fin Flow",
            "email": email,
            "password": password,
            "occupation": "Engineer",
            "age": 28,
            "location": "Coimbatore",
        },
    )
    login = client.post("/api/auth/login", json={"email": email, "password": password})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_expense_income_goal_crud_and_metrics(client):
    headers = _create_user_and_get_headers(client)

    expense = client.post(
        "/api/financial/expenses",
        headers=headers,
        json={
            "date": str(date.today()),
            "amount": 1500.0,
            "category": "Groceries",
            "description": "Weekly groceries",
            "merchant": "Local Store",
        },
    )
    assert expense.status_code == 201
    expense_id = expense.json()["id"]

    list_expenses = client.get("/api/financial/expenses", headers=headers)
    assert list_expenses.status_code == 200
    assert isinstance(list_expenses.json(), list)

    update_expense = client.put(
        f"/api/financial/expenses/{expense_id}",
        headers=headers,
        json={"amount": 1800.0, "description": "Updated groceries"},
    )
    assert update_expense.status_code == 200

    income = client.post(
        "/api/financial/income",
        headers=headers,
        json={"month": str(date.today()), "amount": 50000.0, "source": "Salary"},
    )
    assert income.status_code == 201

    goal = client.post(
        "/api/financial/goals",
        headers=headers,
        json={
            "name": "Emergency Fund",
            "target_amount": 100000.0,
            "deadline": str(date.today()),
            "category": "Savings",
        },
    )
    assert goal.status_code == 201

    metrics = client.get("/api/financial/metrics", headers=headers)
    assert metrics.status_code == 200
    assert "monthlyIncome" in metrics.json()

    health = client.get("/api/financial/health", headers=headers)
    assert health.status_code == 200
