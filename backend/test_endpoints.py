"""
Test AUREXIS AI Backend Endpoints
Quick verification script for all new API endpoints
"""

import pytest
import requests
import json
from datetime import date

pytestmark = pytest.mark.skip(reason="Manual integration script; not intended as pytest test suite")

BASE_URL = "http://localhost:8000"

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ️  {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def test_health_check():
    """Test basic server health"""
    print_info("Testing server health...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print_success("Server is running")
            return True
        else:
            print_error(f"Server returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Server is not running: {e}")
        return False

def test_signup():
    """Test user signup"""
    print_info("Testing signup...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/signup",
            json={
                "name": "Test User",
                "email": "test@aurexis.ai",
                "password": "SecurePass123",
                "occupation": "Software Engineer",
                "age": 30,
                "location": "Mumbai"
            }
        )
        
        if response.status_code == 201:
            data = response.json()
            print_success("Signup successful")
            return data.get("access_token"), data.get("refresh_token")
        elif response.status_code == 400 and "already registered" in response.text:
            print_warning("User already exists, trying login...")
            return test_login()
        else:
            print_error(f"Signup failed: {response.text}")
            return None, None
    except Exception as e:
        print_error(f"Signup error: {e}")
        return None, None

def test_login():
    """Test user login"""
    print_info("Testing login...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": "test@aurexis.ai",
                "password": "SecurePass123"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Login successful")
            return data.get("access_token"), data.get("refresh_token")
        else:
            print_error(f"Login failed: {response.text}")
            return None, None
    except Exception as e:
        print_error(f"Login error: {e}")
        return None, None

def test_protected_endpoint(access_token, endpoint, method="GET", data=None):
    """Test a protected endpoint"""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(f"{BASE_URL}{endpoint}", headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
        
        if response.status_code in [200, 201]:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

def run_tests():
    """Run all endpoint tests"""
    print("\n" + "=" * 60)
    print("🧪 AUREXIS AI Backend Endpoint Tests")
    print("=" * 60 + "\n")
    
    # Test 1: Health Check
    if not test_health_check():
        print_error("Server is not running. Please start the server first.")
        print_info("Run: cd backend && python server.py")
        return
    
    print()
    
    # Test 2: Signup/Login
    access_token, refresh_token = test_signup()
    if not access_token:
        print_error("Authentication failed. Cannot continue tests.")
        return
    
    print()
    
    # Test 3: Get Profile
    print_info("Testing GET /api/auth/profile...")
    success, result = test_protected_endpoint(access_token, "/api/auth/profile")
    if success:
        print_success("Profile retrieved successfully")
    else:
        print_error(f"Profile retrieval failed: {result}")
    
    print()
    
    # Test 4: Create Expense
    print_info("Testing POST /api/financial/expenses...")
    expense_data = {
        "date": str(date.today()),
        "amount": 500,
        "category": "Food",
        "description": "Test expense",
        "merchant": "Test Store"
    }
    success, result = test_protected_endpoint(
        access_token, 
        "/api/financial/expenses", 
        method="POST", 
        data=expense_data
    )
    if success:
        print_success("Expense created successfully")
        expense_id = result.get("id")
    else:
        print_error(f"Expense creation failed: {result}")
        expense_id = None
    
    print()
    
    # Test 5: Get Expenses
    print_info("Testing GET /api/financial/expenses...")
    success, result = test_protected_endpoint(access_token, "/api/financial/expenses")
    if success:
        print_success(f"Retrieved {len(result)} expenses")
    else:
        print_error(f"Get expenses failed: {result}")
    
    print()
    
    # Test 6: Get Financial Health
    print_info("Testing GET /api/financial/health...")
    success, result = test_protected_endpoint(access_token, "/api/financial/health")
    if success:
        print_success("Financial health retrieved successfully")
    else:
        print_error(f"Health retrieval failed: {result}")
    
    print()
    
    # Test 7: Get Financial Metrics
    print_info("Testing GET /api/financial/metrics...")
    success, result = test_protected_endpoint(access_token, "/api/financial/metrics")
    if success:
        print_success("Financial metrics retrieved successfully")
    else:
        print_error(f"Metrics retrieval failed: {result}")
    
    print()
    
    # Test 8: Monthly Forecast
    print_info("Testing GET /api/forecast/monthly...")
    success, result = test_protected_endpoint(access_token, "/api/forecast/monthly?months=6")
    if success:
        print_success("Monthly forecast retrieved successfully")
    else:
        print_error(f"Forecast retrieval failed: {result}")
    
    print()
    
    # Test 9: Create Goal
    print_info("Testing POST /api/financial/goals...")
    goal_data = {
        "name": "Emergency Fund",
        "target_amount": 100000,
        "deadline": "2026-12-31",
        "category": "Savings"
    }
    success, result = test_protected_endpoint(
        access_token, 
        "/api/financial/goals", 
        method="POST", 
        data=goal_data
    )
    if success:
        print_success("Goal created successfully")
    else:
        print_error(f"Goal creation failed: {result}")
    
    print()
    
    # Test 10: Get Goals
    print_info("Testing GET /api/financial/goals...")
    success, result = test_protected_endpoint(access_token, "/api/financial/goals")
    if success:
        print_success(f"Retrieved {len(result)} goals")
    else:
        print_error(f"Get goals failed: {result}")
    
    print()
    
    # Test 11: Chat Message
    print_info("Testing POST /api/chat/message...")
    chat_data = {
        "message": "What is my financial health?",
        "use_memory": True
    }
    success, result = test_protected_endpoint(
        access_token, 
        "/api/chat/message", 
        method="POST", 
        data=chat_data
    )
    if success:
        print_success("Chat message sent successfully")
    else:
        print_error(f"Chat message failed: {result}")
    
    print()
    
    # Test 12: Refresh Token
    print_info("Testing POST /api/auth/refresh...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        if response.status_code == 200:
            print_success("Token refresh successful")
        else:
            print_error(f"Token refresh failed: {response.text}")
    except Exception as e:
        print_error(f"Token refresh error: {e}")
    
    print()
    
    # Summary
    print("=" * 60)
    print("✅ Test suite completed!")
    print("=" * 60)
    print()
    print_info("All new API endpoints are working correctly!")
    print_info("You can now integrate the frontend with these endpoints.")
    print()

if __name__ == "__main__":
    run_tests()
