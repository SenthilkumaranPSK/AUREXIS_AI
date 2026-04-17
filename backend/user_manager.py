"""
User Management Module for AUREXIS AI
All user data is hardcoded — no Excel dependency.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any

BASE_DIR = Path(__file__).parent
TEST_DATA_DIR = BASE_DIR.parent / "test_data_dir"

USERS_DATA = [
    {"si_no": 1,  "name": "Senthilkumaran", "user_number": "1010101010", "email": "sk@gmail.com",   "occupation": "Software Engineer",   "age": 24, "password": "Senthil@123",  "account_number": "ACC001", "bank_name": "SBI",   "account_type": "Savings", "bank_location": "Chennai",    "credit_card": "Yes", "location": "Chennai"},
    {"si_no": 2,  "name": "Imayavarman",    "user_number": "1111111111", "email": "imi@gmail.com",  "occupation": "Doctor",              "age": 32, "password": "Imaya@123",    "account_number": "ACC002", "bank_name": "HDFC",  "account_type": "Savings", "bank_location": "Coimbatore", "credit_card": "Yes", "location": "Coimbatore"},
    {"si_no": 3,  "name": "Srivarshan",     "user_number": "1212121212", "email": "sri@gmail.com",  "occupation": "Business Owner",      "age": 40, "password": "Sri@123",      "account_number": "ACC003", "bank_name": "ICICI", "account_type": "Current", "bank_location": "Madurai",    "credit_card": "Yes", "location": "Madurai"},
    {"si_no": 4,  "name": "Rahulprasath",   "user_number": "1313131313", "email": "rp@gmail.com",   "occupation": "Teacher",             "age": 30, "password": "Rahul@123",    "account_number": "ACC004", "bank_name": "SBI",   "account_type": "Savings", "bank_location": "Trichy",     "credit_card": "No",  "location": "Trichy"},
    {"si_no": 5,  "name": "Dineshkumar",    "user_number": "1414141414", "email": "dk@gmail.com",   "occupation": "Freelancer",          "age": 28, "password": "Dinesh@123",   "account_number": "ACC005", "bank_name": "Axis",  "account_type": "Savings", "bank_location": "Salem",      "credit_card": "No",  "location": "Salem"},
    {"si_no": 6,  "name": "Deepak",         "user_number": "2020202020", "email": "dee@gmail.com",  "occupation": "CA",                  "age": 29, "password": "Deepak@123",   "account_number": "ACC006", "bank_name": "HDFC",  "account_type": "Savings", "bank_location": "Chennai",    "credit_card": "Yes", "location": "Chennai"},
    {"si_no": 7,  "name": "Mani",           "user_number": "2121212121", "email": "mani@gmail.com", "occupation": "Government Employee", "age": 38, "password": "Mani@123",     "account_number": "ACC007", "bank_name": "SBI",   "account_type": "Savings", "bank_location": "Madurai",    "credit_card": "No",  "location": "Madurai"},
    {"si_no": 8,  "name": "Murugesan",      "user_number": "2222222222", "email": "mru@gmail.com",  "occupation": "Lawyer",              "age": 52, "password": "Murugan@123",  "account_number": "ACC008", "bank_name": "IOB",   "account_type": "Savings", "bank_location": "Trichy",     "credit_card": "Yes", "location": "Trichy"},
    {"si_no": 9,  "name": "Avinash",        "user_number": "2525252525", "email": "avi@gmail.com",  "occupation": "IPS",                 "age": 28, "password": "Avinash@123",  "account_number": "ACC009", "bank_name": "SBI",   "account_type": "Savings", "bank_location": "Chennai",    "credit_card": "No",  "location": "Chennai"},
    {"si_no": 10, "name": "Kumar",          "user_number": "3333333333", "email": "kum@gmail.com",  "occupation": "Content Creator",     "age": 23, "password": "Kumar@123",    "account_number": "ACC010", "bank_name": "Kotak", "account_type": "Savings", "bank_location": "Coimbatore", "credit_card": "No",  "location": "Coimbatore"},
    {"si_no": 11, "name": "Vadivel",        "user_number": "4444444444", "email": "vadi@gmail.com", "occupation": "Startup Founder",     "age": 44, "password": "Vadivel@123",  "account_number": "ACC011", "bank_name": "ICICI", "account_type": "Current", "bank_location": "Chennai",    "credit_card": "Yes", "location": "Chennai"},
    {"si_no": 12, "name": "Janakrishnan",   "user_number": "5555555555", "email": "jk@gmail.com",   "occupation": "Government Employee", "age": 22, "password": "Janak@123",    "account_number": "ACC012", "bank_name": "SBI",   "account_type": "Savings", "bank_location": "Salem",      "credit_card": "No",  "location": "Salem"},
]


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
    for user in USERS_DATA:
        if user["name"].lower() == name_lower:
            return user
    return None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Find a user by their user_number."""
    for user in USERS_DATA:
        if user["user_number"] == user_id:
            return user
    return None


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate a user against the hardcoded password."""
    user = get_user_by_name(username)
    if not user:
        return None
    if password.strip() != user["password"]:
        return None

    user_id = user["user_number"]
    return {
        **user,
        "id": user_id,
        "number": user_id,
        "financial_data": get_all_user_data(user_id),
    }


def get_all_users() -> list:
    """Get list of all users."""
    return USERS_DATA
