"""
Test script for JSON-based user manager
"""

from user_manager_json import UserManagerJSON

print("=" * 60)
print("🧪 Testing JSON-Based User Manager")
print("=" * 60)

# Test 1: Get all users
print("\n1️⃣ Testing get_all_users()...")
users = UserManagerJSON.get_all_users()
print(f"   ✅ Found {len(users)} users")
for user in users[:3]:
    print(f"   - {user['name']} ({user['id']})")

# Test 2: Authentication with user_id
print("\n2️⃣ Testing authentication with user_id...")
user = UserManagerJSON.authenticate_user('22243045', 'Senthilkumaran@2000')
if user:
    print(f"   ✅ Authentication successful!")
    print(f"   - Name: {user['name']}")
    print(f"   - Email: {user['email']}")
    print(f"   - Occupation: {user['occupation']}")
    has_financial = 'fetch_bank_transactions' in user.get('financial_data', {})
    print(f"   - Has financial data: {has_financial}")
else:
    print("   ❌ Authentication failed")

# Test 3: Authentication with name
print("\n3️⃣ Testing authentication with name...")
user = UserManagerJSON.authenticate_user('Senthilkumaran', 'Senthilkumaran@2000')
if user:
    print(f"   ✅ Authentication successful with name!")
    print(f"   - User ID: {user['id']}")
else:
    print("   ❌ Authentication failed")

# Test 4: Authentication with account number
print("\n4️⃣ Testing authentication with account number...")
user = UserManagerJSON.authenticate_user('1010101010', 'Senthilkumaran@2000')
if user:
    print(f"   ✅ Authentication successful with account number!")
    print(f"   - User ID: {user['id']}")
else:
    print("   ❌ Authentication failed")

# Test 5: Get user data
print("\n5️⃣ Testing get_all_user_data()...")
data = UserManagerJSON.get_all_user_data('22243045')
if 'error' not in data:
    print(f"   ✅ Data loaded successfully!")
    print(f"   - Profile: {'profile' in data}")
    print(f"   - Bank transactions: {'fetch_bank_transactions' in data}")
    print(f"   - Credit report: {'fetch_credit_report' in data}")
    print(f"   - EPF details: {'fetch_epf_details' in data}")
    print(f"   - MF transactions: {'fetch_mf_transactions' in data}")
    print(f"   - Net worth: {'fetch_net_worth' in data}")
    print(f"   - Stock transactions: {'fetch_stock_transactions' in data}")
else:
    print(f"   ❌ Error: {data['error']}")

# Test 6: Invalid authentication
print("\n6️⃣ Testing invalid authentication...")
user = UserManagerJSON.authenticate_user('22243045', 'wrongpassword')
if user:
    print("   ❌ Should have failed!")
else:
    print("   ✅ Correctly rejected invalid password")

print("\n" + "=" * 60)
print("✅ All tests completed!")
print("=" * 60)
