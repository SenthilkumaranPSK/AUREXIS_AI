"""Test script to verify risk endpoint works"""
import requests
import json

# Login first
login_response = requests.post(
    "http://localhost:8000/api/login",
    json={"username": "Mani", "password": "Mani@2000"}
)

if login_response.status_code == 200:
    login_data = login_response.json()
    print("Login response:", json.dumps(login_data, indent=2))
    
    # Handle both response formats
    if "data" in login_data:
        access_token = login_data["data"]["access_token"]
    elif "access_token" in login_data:
        access_token = login_data["access_token"]
    else:
        print("❌ Unexpected login response format")
        exit(1)
        
    print("✅ Login successful")
    print(f"Token: {access_token[:50]}...")
    
    # Test risk endpoint
    risk_response = requests.get(
        "http://localhost:8000/api/financial/risk",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    print(f"\n📊 Risk Endpoint Status: {risk_response.status_code}")
    if risk_response.status_code == 200:
        risk_data = risk_response.json()
        print("✅ Risk data retrieved successfully:")
        print(json.dumps(risk_data, indent=2))
    else:
        print(f"❌ Error: {risk_response.text}")
        
    # Test goals endpoint
    goals_response = requests.get(
        "http://localhost:8000/api/financial/goals",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    print(f"\n🎯 Goals Endpoint Status: {goals_response.status_code}")
    if goals_response.status_code == 200:
        goals_data = goals_response.json()
        print(f"✅ Goals retrieved: {len(goals_data)} goals")
    else:
        print(f"❌ Error: {goals_response.text}")
else:
    print(f"❌ Login failed: {login_response.text}")
