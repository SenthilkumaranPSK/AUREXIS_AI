"""
Test Analytics Module
"""

import pytest
from analytics import (
    extract_transactions,
    extract_net_worth,
    extract_credit_score,
    compute_metrics,
    compute_expenses,
    compute_investments,
    compute_goals,
    compute_risk,
)


def test_extract_transactions(sample_financial_data):
    """Test transaction extraction"""
    income, expense, transactions = extract_transactions(sample_financial_data)
    
    assert income == 50000
    assert expense == 25000  # 20000 + 5000
    assert len(transactions) == 3
    assert transactions[0]["type"] == "CREDIT"
    assert transactions[1]["type"] == "DEBIT"


def test_extract_net_worth(sample_financial_data):
    """Test net worth extraction"""
    net_worth = extract_net_worth(sample_financial_data)
    assert net_worth == 500000


def test_extract_credit_score(sample_financial_data):
    """Test credit score extraction"""
    credit_score = extract_credit_score(sample_financial_data)
    assert credit_score == 750


def test_compute_metrics(sample_financial_data):
    """Test metrics computation"""
    metrics = compute_metrics(sample_financial_data)
    
    assert "monthlyIncome" in metrics
    assert "monthlyExpense" in metrics
    assert "savings" in metrics
    assert "savingsRate" in metrics
    assert "netWorth" in metrics
    assert "creditScore" in metrics
    assert "debtToIncomeRatio" in metrics
    assert "financialHealthScore" in metrics
    
    assert metrics["monthlyIncome"] == 50000
    assert metrics["monthlyExpense"] == 25000
    assert metrics["savings"] == 25000
    assert metrics["savingsRate"] == 50.0
    assert metrics["netWorth"] == 500000
    assert metrics["creditScore"] == 750


def test_compute_expenses(sample_financial_data):
    """Test expense breakdown computation"""
    expenses = compute_expenses(sample_financial_data)
    
    assert isinstance(expenses, list)
    assert len(expenses) > 0
    
    # Check structure
    for expense in expenses:
        assert "category" in expense
        assert "amount" in expense
        assert "percentage" in expense
        assert "trend" in expense
        assert "color" in expense


def test_compute_investments(sample_financial_data):
    """Test investment portfolio computation"""
    investments = compute_investments(sample_financial_data)
    
    assert "totalValue" in investments
    assert "avgReturns" in investments
    assert "portfolio" in investments
    
    assert isinstance(investments["portfolio"], list)
    assert len(investments["portfolio"]) > 0


def test_compute_goals(sample_financial_data):
    """Test financial goals computation"""
    goals = compute_goals(sample_financial_data)
    
    assert isinstance(goals, list)
    assert len(goals) > 0
    
    # Check structure
    for goal in goals:
        assert "id" in goal
        assert "name" in goal
        assert "target" in goal
        assert "current" in goal
        assert "progress" in goal


def test_compute_risk(sample_financial_data):
    """Test risk analysis computation"""
    risk = compute_risk(sample_financial_data)
    
    assert "riskScore" in risk
    assert "riskLevel" in risk
    assert "debtToIncomeRatio" in risk
    assert "savingsRate" in risk
    assert "emergencyFundMonths" in risk
    assert "creditScore" in risk
    assert "factors" in risk
    
    assert risk["riskLevel"] in ["Low", "Medium", "High"]
    assert isinstance(risk["factors"], list)
