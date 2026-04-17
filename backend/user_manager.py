"""
User Management Module for AUREXIS AI
Reads user data from Users.xlsx
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

BASE_DIR = Path(__file__).parent
TEST_DATA_DIR = BASE_DIR.parent / "test_data_dir"
USERS_XLSX_PATH = BASE_DIR.parent / "Users.xlsx"

# Fallback hardcoded data (used if pandas unavailable or Excel missing)
USERS_DATA = [
    {"si_no": 1,  "name": "Senthilkumaran", "user_number": "1010101010", "email": "sk@gmail.com",   "occupation": "Software Engineer",  "age": 24, "password": "Senthil@123",   "account_number": "ACC001", "bank_name": "SBI",   "account_type": "Savings", "bank_location": "Chennai",    "credit_card": "Yes", "location": "Chennai"},
    {"si_no": 2,  "name": "Imayavarman",    "user_number": "1111111111", "email": "imi@gmail.com",  "occupation": "Doctor",             "age": 32, "password": "Imaya@123",    "account_number": "ACC002", "bank_name": "HDFC",  "account_type": "Savings", "bank_location": "Coimbatore", "credit_card": "Yes", "location": "Coimbatore"},
    {"si_no": 3,  "name": "Srivarshan",     "user_number": "1212121212", "email": "sri@gmail.com",  "occupation": "Business Owner",     "age": 40, "password": "Sri@123",      "account_number": "ACC003", "bank_name": "ICICI", "account_type": "Current", "bank_location": "Madurai",    "credit_card": "Yes", "location": "Madurai"},
    {"si_no": 4,  "name": "Rahulprasath",   "user_number": "1313131313", "email": "rp@gmail.com",   "occupation": "Teacher",            "age": 30, "password": "Rahul@123",    "account_number": "ACC004", "bank_name": "SBI",   "account_type": "Savings", "bank_location": "Trichy",     "credit_card": "No",  "location": "Trichy"},
    {"si_no": 5,  "name": "Dineshkumar",    "user_number": "1414141414", "email": "dk@gmail.com",   "occupation": "Freelancer",         "age": 28, "password": "Dinesh@123",   "account_number": "ACC005", "bank_name": "Axis",  "account_type": "Savings", "bank_location": "Salem",      "credit_card": "No",  "location": "Salem"},
    {"si_no": 6,  "name": "Deepak",         "user_number": "2020202020", "email": "dee@gmail.com",  "occupation": "CA",                 "age": 29, "password": "Deepak@123",   "account_number": "ACC006", "bank_name": "HDFC",  "account_type": "Savings", "bank_location": "Chennai",    "credit_card": "Yes", "location": "Chennai"},
    {"si_no": 7,  "name": "Mani",           "user_number": "2121212121", "email": "mani@gmail.com", "occupation": "Government Employee","age": 38, "password": "Mani@123",     "account_number": "ACC007", "bank_name": "SBI",   "account_type": "Savings", "bank_location": "Madurai",    "credit_card": "No",  "location": "Madurai"},
    {"si_no": 8,  "name": "Murugesan",      "user_number": "2222222222", "email": "mru@gmail.com",  "occupation": "Lawyer",             "age": 52, "password": "Murugan@123",  "account_number": "ACC008", "bank_name": "IOB",   "account_type": "Savings", "bank_location": "Trichy",     "credit_card": "Yes", "location": "Trichy"},
    {"si_no": 9,  "name": "Avinash",        "user_number": "2525252525", "email": "avi@gmail.com",  "occupation": "IPS",                "age": 28, "password": "Avinash@123",  "account_number": "ACC009", "bank_name": "SBI",   "account_type": "Savings", "bank_location": "Chennai",    "credit_card": "No",  "location": "Chennai"},
    {"si_no": 10, "name": "Kumar",          "user_number": "3333333333", "email": "kum@gmail.com",  "occupation": "Content Creator",    "age": 23, "password": "Kumar@123",    "account_number": "ACC010", "bank_name": "Kotak", "account_type": "Savings", "bank_location": "Coimbatore", "credit_card": "No",  "location": "Coimbatore"},
    {"si_no": 11, "name": "Vadivel",        "user_number": "4444444444", "email": "vadi@gmail.com", "occupation": "Startup Founder",    "age": 44, "password": "Vadivel@123",  "account_number": "ACC011", "bank_name": "ICICI", "account_type": "Current", "bank_location": "Chennai",    "credit_card": "Yes", "location": "Chennai"},
    {"si_no": 12, "name": "Janakrishnan",   "user_number": "5555555555", "email": "jk@gmail.com",   "occupation": "Government Employee","age": 22, "password": "Janak@123",    "account_number": "ACC012", "bank_name": "SBI",   "account_type": "Savings", "bank_location": "Salem",      "credit_card": "No",  "location": "Salem"},
]

for user in USERS_DATA:
    user["name"] = user["name"].strip()


def get_users_from_excel() -> list:
    """Read users from Users.xlsx. Falls back to USERS_DATA if unavailable."""
    if not HAS_PANDAS:
        return USERS_DATA

    try:
        df = pd.read_excel(USERS_XLSX_PATH)
        users = []
        for idx, row in df.iterrows():
            # Support both old "Number" column and new "User Number" column
            user_number = str(row.get("User Number", row.get("Number", ""))).strip()
            if not user_number and idx < len(USERS_DATA):
                user_number = USERS_DATA[idx]["user_number"]

            users.append({
                "si_no":          int(row.get("SI.No", idx + 1)),
                "name":           str(row.get("Name", "")).strip(),
                "user_number":    user_number,
                "email":          str(row.get("Mail", "")),
                "occupation":     str(row.get("Occupation", row.get("occupation", ""))),
                "age":            int(row.get("Age", 0)),
                "password":       str(row.get("Password", "")).strip(),
                "account_number": str(row.get("Account Number", "")),
                "bank_name":      str(row.get("Bank Name", "")),
                "account_type":   str(row.get("Account Type", "")),
                "bank_location":  str(row.get("Bank Location", "")),
                "credit_card":    str(row.get("Credit Card", "No")),
                "location":       str(row.get("Location", "")),
            })
        return users
    except Exception as e:
        print(f"Error reading Excel: {e}. Using fallback data.")
        return USERS_DATA


def load_user_data(user_id: str, data_type: str):
    """Load financial JSON data for a user from test_data_dir."""
    data_file = TEST_DATA_DIR / user_id / f"{data_type}.json"
    if not data_file.exists():
        return None
    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {data_type} for user {user_id}: {e}")
        return None


def get_all_user_data(user_id: str) -> Dict[str, Any]:
    """Get all available financial data for a user."""
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
    """Find a user by name (case-insensitive)."""
    name_lower = name.lower().strip()
    for user in get_users_from_excel():
        if user["name"].lower() == name_lower:
            return user
    return None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Find a user by their user_number."""
    for user in get_users_from_excel():
        if user["user_number"] == user_id:
            return user
    return None


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user against the Excel password column.
    Falls back to name=password match if no password is set.
    """
    user = get_user_by_name(username)
    if not user:
        return None

    stored_password = user.get("password", "").strip()

    # If Excel has a real password, use it; otherwise fall back to name=password
    if stored_password:
        if password.strip() != stored_password:
            return None
    else:
        if username.lower().strip() != password.lower().strip():
            return None

    user_id = user["user_number"]
    financial_data = get_all_user_data(user_id)

    return {
        **user,
        "id": user_id,
        "number": user_id,   # keep "number" alias for backward compat
        "financial_data": financial_data,
    }


def get_all_users() -> list:
    """Get list of all users."""
    return get_users_from_excel()


if __name__ == "__main__":
    print("Testing user_manager...")
    print(f"Total users: {len(get_all_users())}")
    user = authenticate_user("Senthilkumaran", "Senthil@123")
    if user:
        print(f"Auth OK: {user['name']} | Bank: {user['bank_name']} | Acc: {user['account_number']}")
    else:
        print("Auth failed")
