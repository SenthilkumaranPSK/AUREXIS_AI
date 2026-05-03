"""
JSON-Based User Management Module for AUREXIS AI
Fetches all data directly from user_data folder JSON files
No database dependency
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
USER_DATA_DIR = BASE_DIR / "user_data"


class UserManagerJSON:
    """JSON-based user management - no database required"""

    # Mapping of account numbers to user IDs for quick lookup
    _account_to_user_map = {
        "1010101010": {"user_id": "22243045", "name": "SK", "password": "SK@2000"},
        "1111111111": {"user_id": "22243017", "name": "Imayavarman", "password": "Imayavarman@2000"},
        "1212121212": {"user_id": "22243050", "name": "Srivarshan", "password": "Srivarshan@2000"},
        "1313131313": {"user_id": "22243040", "name": "Rahulprasath", "password": "Rahulprasath@2000"},
        "1414141414": {"user_id": "22243055", "name": "Magudesh", "password": "Magudesh@2000"},
        "2020202020": {"user_id": "22243009", "name": "Deepak", "password": "Deepak@2000"},
        "2121212121": {"user_id": "22243060", "name": "Mani", "password": "Mani@2000"},
        "2222222222": {"user_id": "22243012", "name": "Dineshkumar", "password": "Dineshkumar@2000"},
        "2525252525": {"user_id": "22243007", "name": "Avinash", "password": "Avinash@2000"},
        "3333333333": {"user_id": "22243020", "name": "Kumar", "password": "Kumar@2000"},
        "4444444444": {"user_id": "22243016", "name": "Hari", "password": "Hari@2000"},
        "5555555555": {"user_id": "22243019", "name": "Janakrishnan", "password": "Janakrishnan@2000"},
    }

    @staticmethod
    def _load_json_file(file_path: Path) -> Optional[Dict[str, Any]]:
        """Load JSON file safely"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
        return None

    @staticmethod
    def _get_user_folder(identifier: str) -> Optional[Path]:
        """
        Get user folder by account number, user_id, or name
        Returns the folder path if found
        """
        # Try direct folder match (account number)
        folder = USER_DATA_DIR / identifier
        if folder.exists():
            return folder

        # Try to find by user_id or name in mapping
        for account_num, user_info in UserManagerJSON._account_to_user_map.items():
            if user_info["user_id"] == identifier or user_info["name"].lower() == identifier.lower():
                folder = USER_DATA_DIR / account_num
                if folder.exists():
                    return folder

        return None

    @staticmethod
    def _load_user_profile(account_number: str) -> Optional[Dict[str, Any]]:
        """Load user profile from profile.json"""
        folder = USER_DATA_DIR / account_number
        profile_file = folder / "profile.json"
        
        if not profile_file.exists():
            return None

        profile = UserManagerJSON._load_json_file(profile_file)
        if not profile:
            return None

        # Enrich with mapping data
        user_info = UserManagerJSON._account_to_user_map.get(account_number, {})
        
        # Build complete user profile
        return {
            "id": user_info.get("user_id", profile.get("user_id", account_number)),
            "user_number": account_number,
            "name": user_info.get("name", profile.get("name", "Unknown")),
            "email": f"{profile.get('name', 'user').lower().replace(' ', '')}@gmail.com",
            "occupation": profile.get("occupation", "Unknown"),
            "age": profile.get("age", 0),
            "location": profile.get("city", "Unknown"),
            "monthly_income": profile.get("monthly_income", 0),
            "risk_profile": profile.get("risk_profile", "Moderate"),
            "financial_goals": profile.get("financial_goals", []),
            "dependents": profile.get("dependents", 0),
            "marital_status": profile.get("marital_status", "Single"),
            "investment_preference": profile.get("investment_preference", "Balanced"),
            "is_active": True,
            "is_verified": True,
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
        }

    @staticmethod
    def get_all_user_data(identifier: str) -> Dict[str, Any]:
        """
        Get all financial data for a user by account number, user_id, or name
        """
        folder = UserManagerJSON._get_user_folder(identifier)
        
        if not folder:
            logger.warning(f"User folder not found for: {identifier}")
            return {"user_id": identifier, "error": "User not found"}

        account_number = folder.name
        
        # Load profile
        profile = UserManagerJSON._load_user_profile(account_number)
        if not profile:
            return {"user_id": identifier, "error": "Profile not found"}

        # Load all financial data files
        data_files = [
            "fetch_bank_transactions",
            "fetch_credit_report",
            "fetch_epf_details",
            "fetch_mf_transactions",
            "fetch_net_worth",
            "fetch_stock_transactions",
        ]

        result = {
            "user_id": profile["id"],
            "profile": profile
        }

        for data_type in data_files:
            file_path = folder / f"{data_type}.json"
            data = UserManagerJSON._load_json_file(file_path)
            if data:
                result[data_type] = data

        return result

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user by username (can be user_id, name, or account number) and password
        """
        # Find user in mapping
        user_info = None
        account_number = None

        # Check if username is account number
        if username in UserManagerJSON._account_to_user_map:
            account_number = username
            user_info = UserManagerJSON._account_to_user_map[username]
        else:
            # Search by user_id or name
            for acc_num, info in UserManagerJSON._account_to_user_map.items():
                if info["user_id"] == username or info["name"].lower() == username.lower():
                    account_number = acc_num
                    user_info = info
                    break

        if not user_info:
            logger.warning(f"User not found: {username}")
            return None

        # Verify password (simple comparison for now)
        if user_info["password"] != password:
            logger.warning(f"Invalid password for user: {username}")
            return None

        # Load full user profile
        profile = UserManagerJSON._load_user_profile(account_number)
        if not profile:
            return None

        # Load financial data
        financial_data = UserManagerJSON.get_all_user_data(account_number)
        
        # Combine profile with financial data
        user_data = {**profile}
        user_data["financial_data"] = financial_data

        logger.info(f"User authenticated successfully: {user_info['name']}")
        return user_data

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by user_id"""
        for account_num, info in UserManagerJSON._account_to_user_map.items():
            if info["user_id"] == user_id:
                return UserManagerJSON._load_user_profile(account_num)
        return None

    @staticmethod
    def get_user_by_name(name: str) -> Optional[Dict[str, Any]]:
        """Get user by name"""
        for account_num, info in UserManagerJSON._account_to_user_map.items():
            if info["name"].lower() == name.lower():
                return UserManagerJSON._load_user_profile(account_num)
        return None

    @staticmethod
    def get_user_by_user_number(user_number: str) -> Optional[Dict[str, Any]]:
        """Get user by user number (account number)"""
        if user_number in UserManagerJSON._account_to_user_map:
            return UserManagerJSON._load_user_profile(user_number)
        return None

    @staticmethod
    def get_all_users() -> List[Dict[str, Any]]:
        """Get all users"""
        users = []
        for account_num in UserManagerJSON._account_to_user_map.keys():
            profile = UserManagerJSON._load_user_profile(account_num)
            if profile:
                # Remove sensitive data
                safe_profile = {k: v for k, v in profile.items() if k != "password_hash"}
                users.append(safe_profile)
        return users


# Legacy compatibility functions
def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Legacy function for backward compatibility"""
    return UserManagerJSON.authenticate_user(username, password)


def get_all_users() -> List[Dict[str, Any]]:
    """Legacy function for backward compatibility"""
    return UserManagerJSON.get_all_users()


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Legacy function for backward compatibility"""
    return UserManagerJSON.get_user_by_id(user_id)


def get_all_user_data(user_id: str) -> Dict[str, Any]:
    """Legacy function for backward compatibility"""
    return UserManagerJSON.get_all_user_data(user_id)
