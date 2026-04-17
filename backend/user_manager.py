"""
User Management Module for AUREXIS AI
Reads user data from Users.xlsx and generates/retrieves user financial data
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Try to import pandas for Excel reading, fallback to manual data
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

# Base paths
BASE_DIR = Path(__file__).parent
TEST_DATA_DIR = BASE_DIR.parent / "test_data_dir"
USERS_XLSX_PATH = BASE_DIR.parent / "Users.xlsx"

# Hardcoded user data from Users.xlsx (fallback if pandas not available)
USERS_DATA = [
    {"si_no": 1, "name": "Senthilkumaran", "number": "1010101010", "email": "sk@gmail.com", "occupation": "Software Engineer", "age": 24},
    {"si_no": 2, "name": "Imayavarman", "number": "1111111111", "email": "imi@gmail.com", "occupation": "Doctor", "age": 32},
    {"si_no": 3, "name": "Srivarshan", "number": "1212121212", "email": "sri@gmail.com", "occupation": "Business Owner", "age": 40},
    {"si_no": 4, "name": "Rahulprasath", "number": "1313131313", "email": "rp@gmail.com", "occupation": "Teacher", "age": 30},
    {"si_no": 5, "name": "Dineshkumar", "number": "1414141414", "email": "dk@gmail.com", "occupation": "Freelancer", "age": 28},
    {"si_no": 6, "name": "Deepak", "number": "2020202020", "email": "dee@gmail.com", "occupation": "CA", "age": 29},
    {"si_no": 7, "name": "Mani", "number": "2121212121", "email": "mani@gmail.com", "occupation": "Government Employee", "age": 38},
    {"si_no": 8, "name": "Murugesan", "number": "2222222222", "email": "mru@gmail.com", "occupation": "Lawayer", "age": 52},
    {"si_no": 9, "name": "Avinash", "number": "2525252525", "email": "avi@gmail.com", "occupation": "IPS", "age": 28},
    {"si_no": 10, "name": "Kumar", "number": "3333333333", "email": "kum@gamil.com", "occupation": "Content Creator", "age": 23},
    {"si_no": 11, "name": "Vadivel", "number": "4444444444", "email": "vadi@gmail.com", "occupation": "Startup Founder", "age": 44},
    {"si_no": 12, "name": "Janakrishnan", "number": "5555555555", "email": "jk@gmail.com", "occupation": "Government Employee", "age": 22},
]

# Clean user names (strip trailing spaces)
for user in USERS_DATA:
    user["name"] = user["name"].strip()


def get_users_from_excel() -> list:
    """Read users from Excel file if pandas is available."""
    if not HAS_PANDAS:
        return USERS_DATA

    try:
        df = pd.read_excel(USERS_XLSX_PATH)
        users = []
        for idx, row in df.iterrows():
            # Use hardcoded numbers as fallback if Excel Number column is empty
            number = str(row.get("Number", "")).strip()
            if not number and idx < len(USERS_DATA):
                number = USERS_DATA[idx]["number"]

            users.append({
                "si_no": int(row.get("SI.No", 0)),
                "name": str(row.get("Name", "")).strip(),  # Strip trailing spaces
                "number": number,
                "email": str(row.get("Mail", "")),
                "occupation": str(row.get("occupation", "")),
                "age": int(row.get("Age", 0)),
            })
        return users
    except Exception as e:
        print(f"Error reading Excel: {e}. Using fallback data.")
        return USERS_DATA


def load_user_data(user_id: str, data_type: str) -> Optional[Dict[str, Any]]:
    """
    Load user financial data from test_data_dir.

    Args:
        user_id: User's phone number (e.g., "1010101010")
        data_type: Type of data to load (e.g., "fetch_bank_transactions", "fetch_net_worth")

    Returns:
        Dictionary containing the financial data or None if not found
    """
    user_dir = TEST_DATA_DIR / user_id
    data_file = user_dir / f"{data_type}.json"

    if not data_file.exists():
        return None

    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {data_type} for user {user_id}: {e}")
        return None


def get_all_user_data(user_id: str) -> Dict[str, Any]:
    """
    Get all available financial data for a user.

    Args:
        user_id: User's phone number

    Returns:
        Dictionary containing all available financial data
    """
    data_types = [
        "fetch_bank_transactions",
        "fetch_credit_report",
        "fetch_epf_details",
        "fetch_mf_transactions",
        "fetch_net_worth",
        "fetch_stock_transactions",
    ]

    result = {"user_id": user_id}
    for data_type in data_types:
        data = load_user_data(user_id, data_type)
        if data:
            result[data_type] = data

    return result


def get_user_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Find a user by name (case-insensitive).

    Args:
        name: User's name

    Returns:
        User dictionary or None if not found
    """
    users = get_users_from_excel()
    name_lower = name.lower().strip()

    for user in users:
        if user["name"].lower() == name_lower:
            return user

    return None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Find a user by ID (phone number).

    Args:
        user_id: User's phone number

    Returns:
        User dictionary or None if not found
    """
    users = get_users_from_excel()

    for user in users:
        if user["number"] == user_id:
            return user

    return None


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user. Username and password must match (case-insensitive).

    Args:
        username: User's name
        password: User's password (must match username)

    Returns:
        User dictionary with financial data or None if authentication fails
    """
    # Check if username matches password (case-insensitive)
    if username.lower().strip() != password.lower().strip():
        return None

    # Find user by name
    user = get_user_by_name(username)
    if not user:
        return None

    # Get user's financial data
    user_id = user["number"]
    financial_data = get_all_user_data(user_id)

    return {
        **user,
        "id": user_id,
        "financial_data": financial_data,
    }


def get_all_users() -> list:
    """Get list of all users."""
    return get_users_from_excel()


if __name__ == "__main__":
    # Test the module
    print("Testing user_manager module...")
    print(f"\nAll users: {len(get_all_users())}")

    # Test authentication
    test_user = authenticate_user("Senthilkumaran", "Senthilkumaran")
    if test_user:
        print(f"\nAuthenticated user: {test_user['name']} (ID: {test_user['id']})")
        print(f"Available data types: {list(test_user.get('financial_data', {}).keys())}")
    else:
        print("\nAuthentication failed!")
