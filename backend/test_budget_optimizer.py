"""
Test script for Budget Optimizer
Demonstrates all features with sample data
"""

import json
from budget_optimizer import budget_optimizer
from datetime import datetime, timedelta

print("=" * 80)
print("🤖 AUREXIS AI - Budget Optimizer Demo")
print("=" * 80)
print()

# Sample transaction data
sample_transactions = [
    {"date": "2026-01-15", "type": "debit", "amount": -5000, "category": "Groceries", "description": "Supermarket"},
    {"date": "2026-01-20", "type": "debit", "amount": -2500, "category": "Dining", "description": "Restaurant"},
    {"date": "2026-01-25", "type": "debit", "amount": -1500, "category": "Transportation", "description": "Uber rides"},
    {"date": "2026-02-10", "type": "debit", "amount": -4800, "category": "Groceries", "description": "Monthly groceries"},
    {"date": "2026-02-14", "type": "debit", "amount": -3000, "category": "Dining", "description": "Valentine dinner"},
    {"date": "2026-02-18", "type": "debit", "amount": -1200, "category": "Transportation", "description": "Fuel"},
    {"date": "2026-03-05", "type": "debit", "amount": -5200, "category": "Groceries", "description": "Grocery shopping"},
    {"date": "2026-03-12", "type": "debit", "amount": -2000, "category": "Entertainment", "description": "Movie tickets"},
    {"date": "2026-03-20", "type": "debit", "amount": -15000, "category": "Shopping", "description": "New laptop"},
    {"date": "2026-04-01", "type": "debit", "amount": -25000, "category": "Rent", "description": "Monthly rent"},
    {"date": "2026-04-05", "type": "debit", "amount": -5500, "category": "Groceries", "description": "Groceries"},
    {"date": "2026-04-10", "type": "debit", "amount": -2800, "category": "Dining", "description": "Weekend dining"},
    {"date": "2026-04-15", "type": "debit", "amount": -3000, "category": "Utilities", "description": "Electricity bill"},
]

# Test 1: Analyze Spending Patterns
print("📊 TEST 1: Spending Pattern Analysis")
print("-" * 80)
analysis = budget_optimizer.analyze_spending_patterns(sample_transactions)
print(json.dumps(analysis, indent=2))
print()

# Test 2: Predict Future Expenses
print("🔮 TEST 2: Future Expense Prediction (3 months)")
print("-" * 80)
predictions = budget_optimizer.predict_future_expenses(sample_transactions, months_ahead=3)
print(json.dumps(predictions, indent=2))
print()

# Test 3: Optimal Budget Allocation
print("💡 TEST 3: Optimal Budget Allocation")
print("-" * 80)
current_spending = {
    "Rent": 25000,
    "Groceries": 5000,
    "Dining": 2500,
    "Transportation": 1500,
    "Utilities": 3000,
    "Entertainment": 2000,
    "Shopping": 5000,
}

financial_goals = [
    {"target_amount": 500000, "months_remaining": 12},  # Emergency fund
    {"target_amount": 1000000, "months_remaining": 24},  # Car purchase
]

optimization = budget_optimizer.suggest_optimal_budget(
    income=80000,
    current_spending=current_spending,
    financial_goals=financial_goals
)
print(json.dumps(optimization, indent=2))
print()

# Test 4: Auto-Categorization
print("🏷️  TEST 4: Auto-Categorization")
print("-" * 80)
test_descriptions = [
    "Amazon purchase",
    "Swiggy food delivery",
    "Uber ride to office",
    "Netflix subscription",
    "Apollo pharmacy",
    "Reliance Fresh",
    "Movie tickets BookMyShow",
]

for desc in test_descriptions:
    category = budget_optimizer.auto_categorize_transaction(desc, 500)
    print(f"'{desc}' → {category}")
print()

# Test 5: Savings Plan
print("💰 TEST 5: Personalized Savings Plan")
print("-" * 80)
savings_plan = budget_optimizer.generate_savings_plan(
    current_savings=100000,
    target_amount=500000,
    months=12,
    current_monthly_savings=15000
)
print(json.dumps(savings_plan, indent=2))
print()

print("=" * 80)
print("✅ All tests completed successfully!")
print("=" * 80)
print()
print("🚀 Budget Optimizer Features:")
print("   1. Spending pattern analysis with temporal insights")
print("   2. ML-based expense prediction")
print("   3. Optimal budget allocation (50/30/20 rule + AI)")
print("   4. Auto-categorization of transactions")
print("   5. Personalized savings plans")
print()
print("📡 API Endpoints:")
print("   GET  /api/user/{user_id}/budget/analyze")
print("   GET  /api/user/{user_id}/budget/predict?months_ahead=3")
print("   GET  /api/user/{user_id}/budget/optimize")
print("   POST /api/budget/categorize")
print("   POST /api/budget/savings-plan")
print()
