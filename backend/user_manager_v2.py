"""
AUREXIS AI — Enhanced User Manager v2.0
Database-backed user management with async file loading
"""

import json
import aiofiles
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from sqlalchemy.orm import Session
from database import User, get_db_context, create_user, get_user_by_id, get_user_by_name, get_user_by_email
from security import hash_password, verify_password
from cache import cache, cache_user_data, get_cached_user_data
from logger import logger
from config import settings


BASE_DIR = Path(__file__).parent
USER_DATA_DIR = BASE_DIR / settings.USER_DATA_DIR


# ── Legacy User Data (for migration) ───────────────────────────────────────

LEGACY_USERS = [
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


# ── Async File Operations ──────────────────────────────────────────────────

async def load_user_data_async(user_id: str, data_type: str) -> Optional[Dict[str, Any]]:
    """Asynchronously load financial JSON data for a user"""
    
    # Try cache first
    cached = get_cached_user_data(user_id, data_type)
    if cached is not None:
        logger.debug(f"Cache hit: {user_id}/{data_type}")
        return cached
    
    # Load from file
    data_file = USER_DATA_DIR / user_id / f"{data_type}.json"
    if not data_file.exists():
        logger.warning(f"Data file not found: {data_file}")
        return None
    
    try:
        async with aiofiles.open(data_file, "r", encoding="utf-8") as f:
            content = await f.read()
            data = json.loads(content)
        
        # Cache for future requests
        cache_user_data(user_id, data_type, data, ttl=settings.CACHE_TTL)
        
        logger.debug(f"Loaded from file: {user_id}/{data_type}")
        return data
        
    except Exception as e:
        logger.error(f"Error loading {data_type} for user {user_id}: {e}")
        return None


async def get_all_user_data_async(user_id: str) -> Dict[str, Any]:
    """Asynchronously get all available financial data for a user"""
    import asyncio
    
    data_types = [
        "fetch_bank_transactions",
        "fetch_credit_report",
        "fetch_epf_details",
        "fetch_mf_transactions",
        "fetch_net_worth",
        "fetch_stock_transactions",
    ]
    
    # Load all files concurrently
    tasks = [load_user_data_async(user_id, dt) for dt in data_types]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Build result dictionary
    result = {"user_id": user_id}
    for i, data_type in enumerate(data_types):
        if not isinstance(results[i], Exception) and results[i] is not None:
            result[data_type] = results[i]
    
    return result


# ── User Authentication ────────────────────────────────────────────────────

def authenticate_user_legacy(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Legacy authentication (for backward compatibility)
    Uses hardcoded user list
    """
    # Find user by name
    user_data = next((u for u in LEGACY_USERS if u["name"].lower() == username.lower()), None)
    
    if not user_data:
        logger.warning(f"User not found: {username}")
        return None
    
    # Verify password
    if password.strip() != user_data["password"]:
        logger.warning(f"Invalid password for user: {username}")
        return None
    
    user_id = user_data["user_number"]
    
    logger.info(f"User authenticated (legacy): {username} ({user_id})")
    
    return {
        **user_data,
        "id": user_id,
        "number": user_id,
    }


def authenticate_user_db(db: Session, username: str, password: str) -> Optional[User]:
    """
    Database authentication with hashed passwords
    """
    # Try to find user by email or name
    user = get_user_by_email(db, username) or get_user_by_name(db, username)
    
    if not user:
        logger.warning(f"User not found in database: {username}")
        return None
    
    # Verify password
    if not verify_password(password, user.password_hash):
        logger.warning(f"Invalid password for user: {username}")
        return None
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    logger.info(f"User authenticated (database): {user.name} ({user.id})")
    
    return user


async def authenticate_user(username: str, password: str, use_db: bool = False) -> Optional[Dict[str, Any]]:
    """
    Unified authentication function
    
    Args:
        username: Username or email
        password: Plain text password
        use_db: If True, use database authentication; otherwise use legacy
    
    Returns:
        User data dictionary or None
    """
    if use_db:
        with get_db_context() as db:
            user = authenticate_user_db(db, username, password)
            if user:
                # Load financial data
                financial_data = await get_all_user_data_async(user.id)
                
                return {
                    "id": user.id,
                    "number": user.id,
                    "name": user.name,
                    "email": user.email,
                    "occupation": user.occupation,
                    "age": user.age,
                    "location": user.location,
                    "account_number": user.account_number,
                    "bank_name": user.bank_name,
                    "account_type": user.account_type,
                    "bank_location": user.bank_location,
                    "credit_card": user.credit_card,
                    "financial_data": financial_data,
                }
            return None
    else:
        # Legacy authentication
        user_data = authenticate_user_legacy(username, password)
        if user_data:
            # Load financial data
            financial_data = await get_all_user_data_async(user_data["user_number"])
            user_data["financial_data"] = financial_data
        return user_data


# ── User Migration ─────────────────────────────────────────────────────────

def migrate_legacy_users_to_db():
    """Migrate legacy users to database with hashed passwords"""
    with get_db_context() as db:
        migrated = 0
        skipped = 0
        
        for legacy_user in LEGACY_USERS:
            # Check if user already exists
            existing = get_user_by_id(db, legacy_user["user_number"])
            if existing:
                logger.info(f"User already exists: {legacy_user['name']}")
                skipped += 1
                continue
            
            # Create new user with hashed password
            user_data = {
                "id": legacy_user["user_number"],
                "name": legacy_user["name"],
                "email": legacy_user["email"],
                "password_hash": hash_password(legacy_user["password"]),
                "occupation": legacy_user["occupation"],
                "age": legacy_user["age"],
                "location": legacy_user["location"],
                "account_number": legacy_user["account_number"],
                "bank_name": legacy_user["bank_name"],
                "account_type": legacy_user["account_type"],
                "bank_location": legacy_user["bank_location"],
                "credit_card": legacy_user["credit_card"].lower() == "yes",
                "is_active": True,
                "is_verified": True,
            }
            
            try:
                create_user(db, user_data)
                logger.info(f"Migrated user: {legacy_user['name']}")
                migrated += 1
            except Exception as e:
                logger.error(f"Failed to migrate user {legacy_user['name']}: {e}")
        
        logger.info(f"Migration complete: {migrated} migrated, {skipped} skipped")


# ── User Listing ───────────────────────────────────────────────────────────

def get_all_users_legacy() -> List[Dict[str, Any]]:
    """Get all users from legacy data"""
    return LEGACY_USERS


def get_all_users_db(db: Session) -> List[User]:
    """Get all users from database"""
    return db.query(User).filter(User.is_active == True).all()


# ── Backward Compatibility ─────────────────────────────────────────────────

# Keep old function names for compatibility
def get_user_by_name_legacy(name: str) -> Optional[Dict[str, Any]]:
    """Find a user by name (case-insensitive) - legacy"""
    name_lower = name.lower().strip()
    for user in LEGACY_USERS:
        if user["name"].lower() == name_lower:
            return user
    return None


def get_user_by_id_legacy(user_id: str) -> Optional[Dict[str, Any]]:
    """Find a user by their user_number - legacy"""
    for user in LEGACY_USERS:
        if user["user_number"] == user_id:
            return user
    return None
