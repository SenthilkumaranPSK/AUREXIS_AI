"""
Test AI Recommendations endpoint
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_recommendations():
    print("=" * 60)
    print("AI RECOMMENDATIONS TEST")
    print("=" * 60)
    
    # Step 1: Login
    print("\n[1/4] Logging in...")
    login_url = f"{BASE_URL}/api/login"
    login_data = {
        "username": "22243045",
        "password": "Senthilkumaran@2000"
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        if response.status_code != 200:
            print(f"   ❌ Login failed: {response.text}")
            return
        
        data = response.json()
        access_token = data.get('data', {}).get('access_token')
        if not access_token:
            print(f"   ❌ No access_token in response")
            return
        
        print(f"   ✅ Login successful")
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server. Is it running?")
        return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Step 2: Generate recommendations
    print("\n[2/4] Generating recommendations...")
    generate_url = f"{BASE_URL}/api/financial/recommendations/generate"
    
    try:
        response = requests.post(generate_url, headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Failed: {response.text[:500]}")
            return
        
        result = response.json()
        print(f"   ✅ Generated successfully")
        print(f"   Response: {json.dumps(result, indent=2)}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 3: Get recommendations
    print("\n[3/4] Fetching recommendations...")
    get_url = f"{BASE_URL}/api/financial/recommendations"
    
    try:
        response = requests.get(get_url, headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Failed: {response.text[:500]}")
            return
        
        recommendations = response.json()
        print(f"   ✅ Fetched {len(recommendations)} recommendations")
        
        # Step 4: Display recommendations
        print("\n[4/4] Recommendations:")
        print("-" * 60)
        
        if not recommendations:
            print("   No recommendations found")
        else:
            for i, rec in enumerate(recommendations, 1):
                print(f"\n   {i}. {rec.get('title', 'No title')}")
                print(f"      Category: {rec.get('category', 'N/A')}")
                print(f"      Priority: {rec.get('priority', 'N/A')}")
                print(f"      Impact: {rec.get('impact', 'N/A')}")
                print(f"      Status: {rec.get('status', 'N/A')}")
                print(f"      Description: {rec.get('description', 'N/A')}")
        
        print("\n" + "=" * 60)
        print("✅ TEST COMPLETE!")
        print("=" * 60)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_recommendations()
