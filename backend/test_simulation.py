"""
Test script for simulation endpoint
"""
import requests
import json

# First login to get a token
login_url = "http://127.0.0.1:8000/api/login"
login_data = {
    "username": "22243045",
    "password": "Senthilkumaran@2000"
}

print("1. Testing login...")
response = requests.post(login_url, json=login_data)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"   Success: {data.get('success')}")
    
    # Extract token if available
    # Note: The current implementation doesn't return a JWT token
    # It returns a session_id instead
    session_id = data.get('data', {}).get('session_id')
    print(f"   Session ID: {session_id}")
    
    # Try to call simulation endpoint
    print("\n2. Testing simulation endpoint...")
    simulation_url = "http://127.0.0.1:8000/api/financial/simulation"
    
    # Test with query parameters
    params = {
        "new_loan": 100000,
        "salary_increase": 5000,
        "new_expense": 2000,
        "investment_amount": 50000,
        "months": 12
    }
    
    # Note: Current auth uses session_id, not JWT Bearer token
    # The endpoint expects get_current_user which needs JWT
    # This is a mismatch that needs to be fixed
    
    headers = {
        "Authorization": f"Bearer {session_id}"
    }
    
    response = requests.post(simulation_url, params=params, headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:500]}")
    
else:
    print(f"   Login failed: {response.text}")
