"""
Complete test for simulation endpoint with JWT authentication
Run this after starting the server: python server.py
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_simulation():
    print("=" * 60)
    print("SIMULATION ENDPOINT TEST")
    print("=" * 60)
    
    # Step 1: Login
    print("\n[1/3] Testing login...")
    login_url = f"{BASE_URL}/api/login"
    login_data = {
        "username": "22243045",
        "password": "Senthilkumaran@2000"
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Login failed: {response.text}")
            return
        
        data = response.json()
        if not data.get('success'):
            print(f"   ❌ Login unsuccessful: {data}")
            return
        
        access_token = data.get('data', {}).get('access_token')
        if not access_token:
            print(f"   ❌ No access_token in response")
            print(f"   Response: {json.dumps(data, indent=2)}")
            return
        
        print(f"   ✅ Login successful")
        print(f"   Token: {access_token[:50]}...")
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server. Is it running?")
        print("   Start server with: python server.py")
        return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 2: Test simulation endpoint
    print("\n[2/3] Testing simulation endpoint...")
    simulation_url = f"{BASE_URL}/api/financial/simulation"
    
    params = {
        "new_loan": 100000,
        "salary_increase": 5000,
        "new_expense": 2000,
        "investment_amount": 50000,
        "months": 12
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.post(simulation_url, params=params, headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Simulation failed")
            print(f"   Response: {response.text[:500]}")
            return
        
        result = response.json()
        print(f"   ✅ Simulation successful")
        
        # Step 3: Display results
        print("\n[3/3] Simulation Results:")
        print("-" * 60)
        
        if result.get('success'):
            sim = result.get('simulation', {})
            
            # Current state
            current = sim.get('current', {})
            print("\n📊 CURRENT FINANCIAL STATE:")
            print(f"   Monthly Income:  ₹{current.get('monthly_income', 0):,.0f}")
            print(f"   Monthly Expense: ₹{current.get('monthly_expense', 0):,.0f}")
            print(f"   Monthly Savings: ₹{current.get('monthly_savings', 0):,.0f}")
            print(f"   Savings Rate:    {current.get('savings_rate', 0):.1f}%")
            
            # Projected state
            projected = sim.get('projected', {})
            print("\n🔮 PROJECTED STATE (after simulation):")
            print(f"   Monthly Income:  ₹{projected.get('monthly_income', 0):,.0f}")
            print(f"   Monthly Expense: ₹{projected.get('monthly_expense', 0):,.0f}")
            print(f"   Monthly Savings: ₹{projected.get('monthly_savings', 0):,.0f}")
            print(f"   Savings Rate:    {projected.get('savings_rate', 0):.1f}%")
            print(f"   Loan Payment:    ₹{projected.get('loan_payment', 0):,.0f}")
            print(f"   Investment Value:₹{projected.get('investment_value', 0):,.0f}")
            print(f"   Final Net Worth: ₹{projected.get('final_net_worth', 0):,.0f}")
            
            # Changes
            changes = sim.get('changes', {})
            print("\n📈 CHANGES:")
            print(f"   Income Change:   ₹{changes.get('income_change', 0):,.0f}")
            print(f"   Expense Change:  ₹{changes.get('expense_change', 0):,.0f}")
            print(f"   Savings Change:  ₹{changes.get('savings_change', 0):,.0f}")
            print(f"   Net Worth Change:₹{changes.get('net_worth_change', 0):,.0f}")
            
            # Timeline
            timeline = sim.get('timeline', {})
            print("\n📅 TIMELINE:")
            print(f"   Duration:        {timeline.get('months', 0)} months")
            print(f"   Start Date:      {timeline.get('start_date', 'N/A')}")
            print(f"   End Date:        {timeline.get('end_date', 'N/A')}")
            
            # Recommendations
            recommendations = result.get('recommendations', [])
            if recommendations:
                print("\n💡 RECOMMENDATIONS:")
                for rec in recommendations:
                    rec_type = rec.get('type', 'info').upper()
                    message = rec.get('message', '')
                    icon = "✅" if rec_type == "SUCCESS" else "⚠️" if rec_type == "WARNING" else "ℹ️"
                    print(f"   {icon} {message}")
            
            print("\n" + "=" * 60)
            print("✅ ALL TESTS PASSED!")
            print("=" * 60)
        else:
            print(f"   ❌ Simulation returned success=false")
            print(f"   Response: {json.dumps(result, indent=2)}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_simulation()
