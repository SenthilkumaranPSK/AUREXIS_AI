"""
User Management Module for AUREXIS AI
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any

BASE_DIR = Path(__file__).parent
TEST_DATA_DIR = BASE_DIR / "user_data"

USERS_DATA = [
    {"si_no": 1,  "name": "Senthilkumaran", "user_number": "1010101010", "email": "sk@gmail.com",   "occupation": "Software Engineer",   "age": 24, "password": "Senthilkumaran@2000", "account_number": "1010101010", "bank_name": "Indian", "account_type": "Savings", "bank_location": "Salem",      "credit_card": "Yes", "location": "Salem",      "number": "22243045"},
    {"si_no": 2,  "name": "Imayavarman",    "user_number": "1111111111", "email": "imi@gmail.com",  "occupation": "Doctor",              "age": 32, "password": "Imayavarman@2000",    "account_number": "1111111111", "bank_name": "KVB",    "account_type": "Savings", "bank_location": "Erode",      "credit_card": "Yes", "location": "Erode",      "number": "22243017"},
    {"si_no": 3,  "name": "Srivarshan",     "user_number": "1212121212", "email": "sri@gmail.com",  "occupation": "Business Owner",      "age": 40, "password": "Srivarshan@2000",     "account_number": "1212121212", "bank_name": "Canara", "account_type": "Current", "bank_location": "Theni",      "credit_card": "Yes", "location": "Theni",      "number": "22243050"},
    {"si_no": 4,  "name": "Rahulprasath",   "user_number": "1313131313", "email": "rp@gmail.com",   "occupation": "Teacher",             "age": 30, "password": "Rahulprasath@2000",   "account_number": "1313131313", "bank_name": "AXIS",   "account_type": "Savings", "bank_location": "Omalur",     "credit_card": "No",  "location": "Omalur",     "number": "22243040"},
    {"si_no": 5,  "name": "Magudesh",       "user_number": "1414141414", "email": "magu@gmail.com", "occupation": "Freelancer",          "age": 28, "password": "Magudesh@2000",       "account_number": "1414141414", "bank_name": "Canara", "account_type": "Savings", "bank_location": "Bangalore",  "credit_card": "No",  "location": "Bangalore",  "number": "22243055"},
    {"si_no": 6,  "name": "Deepak",         "user_number": "2020202020", "email": "dee@gmail.com",  "occupation": "CA",                  "age": 29, "password": "Deepak@2000",         "account_number": "2020202020", "bank_name": "KVB",    "account_type": "Current", "bank_location": "Chennai",    "credit_card": "No",  "location": "Chennai",    "number": "22243009"},
    {"si_no": 7,  "name": "Mani",           "user_number": "2121212121", "email": "mani@gmail.com", "occupation": "Government Employee", "age": 38, "password": "Mani@2000",           "account_number": "2121212121", "bank_name": "SBI",    "account_type": "Savings", "bank_location": "Edapadi",    "credit_card": "Yes", "location": "Edapadi",    "number": "22243060"},
    {"si_no": 8,  "name": "Dineshkumar",    "user_number": "2222222222", "email": "dk@gmail.com",   "occupation": "Lawyer",              "age": 52, "password": "Dineshkumar@2000",    "account_number": "2222222222", "bank_name": "Indian", "account_type": "Savings", "bank_location": "Sangagari",  "credit_card": "Yes", "location": "Sangagari",  "number": "22243012"},
    {"si_no": 9,  "name": "Avinash",        "user_number": "2525252525", "email": "avi@gmail.com",  "occupation": "IPS",                 "age": 28, "password": "Avinash@2000",        "account_number": "2525252525", "bank_name": "AXIS",   "account_type": "Savings", "bank_location": "Ambur",      "credit_card": "No",  "location": "Ambur",      "number": "22243007"},
    {"si_no": 10, "name": "Kumar",          "user_number": "3333333333", "email": "kum@gmail.com",  "occupation": "Content Creator",     "age": 23, "password": "Kumar@2000",          "account_number": "3333333333", "bank_name": "Indian", "account_type": "Current", "bank_location": "Coimbatore", "credit_card": "No",  "location": "Coimbatore", "number": "22243020"},
    {"si_no": 11, "name": "Hari",           "user_number": "4444444444", "email": "hari@gmail.com", "occupation": "Startup Founder",     "age": 44, "password": "Hari@2000",           "account_number": "4444444444", "bank_name": "Canara", "account_type": "Current", "bank_location": "Karur",      "credit_card": "Yes", "location": "Karur",      "number": "22243016"},
    {"si_no": 12, "name": "Janakrishnan",   "user_number": "5555555555", "email": "jk@gmail.com",   "occupation": "Government Employee", "age": 22, "password": "Janakrishnan@2000",   "account_number": "5555555555", "bank_name": "SBI",    "account_type": "Savings", "bank_location": "Rasipuram",  "credit_card": "Yes", "location": "Rasipuram",  "number": "22243019"},
]


def load_user_data(user_id: str, data_type: str):
    """Load financial JSON data for a user from user_data/."""
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
