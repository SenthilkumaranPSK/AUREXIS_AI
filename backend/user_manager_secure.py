"""
Secure User Management Module for AUREXIS AI
Database-backed with parameterized queries and proper security
"""

import json
import logging
import secrets
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import uuid
import sqlite3
import bcrypt  # Use bcrypt for secure password hashing

from database.db_utils import get_db 
from exceptions import (
    ValidationError,
    NotFoundError,
    AuthenticationError,
    DatabaseError
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
TEST_DATA_DIR = BASE_DIR / "user_data"


class UserManager:
    """Secure user management with database operations"""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using bcrypt (industry standard)
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        # Bcrypt automatically handles salting
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)  # 12 rounds is a good balance
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify password against bcrypt hash
        
        Args:
            password: Plain text password to verify
            hashed: Bcrypt hashed password from database
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            if not hashed:
                return False
            password_bytes = password.encode('utf-8')
            hashed_bytes = hashed.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False

    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user with parameterized queries"""
        required_fields = ["name", "email", "password"]
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                raise ValidationError(f"Missing required field: {field}")

        # Generate user_number if not provided
        user_number = user_data.get("user_number") or f"AUREXIS_{secrets.token_hex(4).upper()}"
        user_id = user_data.get("id") or str(uuid.uuid4())

        # Hash password
        password_hash = UserManager.hash_password(user_data["password"])

        try:
            with get_db() as conn:
                cursor = conn.cursor()

                # Check if user already exists
                cursor.execute(
                    "SELECT id FROM users WHERE email = ? OR user_number = ?",
                    (user_data["email"], user_number)
                )
                if cursor.fetchone():
                    raise ValidationError("User with this email or user number already exists")

                # Insert user with parameterized query
                cursor.execute("""
                    INSERT INTO users (
                        id, name, email, password_hash, user_number, occupation, age,
                        location, is_active, is_verified, created_at, updated_at       
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    user_data["name"],
                    user_data["email"],
                    password_hash,
                    user_number,
                    user_data.get("occupation"),
                    user_data.get("age"),
                    user_data.get("location"),
                    1,  # is_active
                    0,  # is_verified
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))

                # Return user without password
                return {
                    "id": user_id,
                    "name": user_data["name"],
                    "email": user_data["email"],
                    "user_number": user_number,
                    "occupation": user_data.get("occupation"),
                    "age": user_data.get("age"),
                    "location": user_data.get("location"),
                    "is_active": True,
                    "is_verified": False,
                    "created_at": datetime.now().isoformat()
                }

        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise DatabaseError(f"Failed to create user: {e}")

    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email with parameterized query"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE email = ? AND is_active = 1",
                    (email,)
                )
                row = cursor.fetchone()

                if row:
                    return dict(row)
                return None

        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            raise DatabaseError("Failed to retrieve user")

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID with parameterized query"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE id = ? AND is_active = 1",
                    (user_id,)
                )
                row = cursor.fetchone()

                if row:
                    return dict(row)
                return None

        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            raise DatabaseError("Failed to retrieve user")

    @staticmethod
    def get_user_by_user_number(user_number: str) -> Optional[Dict[str, Any]]:
        """Get user by user number with parameterized query"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE user_number = ? AND is_active = 1",
                    (user_number,)
                )
                row = cursor.fetchone()

                if row:
                    return dict(row)
                return None

        except Exception as e:
            logger.error(f"Error getting user by user number: {e}")
            raise DatabaseError("Failed to retrieve user")

    @staticmethod
    def get_user_by_name(name: str) -> Optional[Dict[str, Any]]:
        """Get user by name with parameterized query"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE name = ? AND is_active = 1",
                    (name,)
                )
                row = cursor.fetchone()

                if row:
                    return dict(row)
                return None

        except Exception as e:
            logger.error(f"Error getting user by name: {e}")
            raise DatabaseError("Failed to retrieve user")

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:    
        """Authenticate user with secure password verification"""
        try:
            # Try to find user by email, user_number, or name
            user = UserManager.get_user_by_email(username)
            if not user:
                user = UserManager.get_user_by_user_number(username)
            if not user:
                user = UserManager.get_user_by_name(username)

            if not user:
                return None

            # Verify password
            if not UserManager.verify_password(password, user["password_hash"]):        
                return None

            # Update last login
            UserManager.update_last_login(user["id"])

            # Remove password hash from response
            user_data = dict(user)
            user_data.pop("password_hash", None)

            # Add financial data
            user_data["financial_data"] = UserManager.get_all_user_data(user["id"])

            return user_data

        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None

    @staticmethod
    def update_last_login(user_id: str) -> None:
        """Update user's last login timestamp"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET last_login = ? WHERE id = ?",
                    (datetime.now().isoformat(), user_id)
                )
        except Exception as e:
            logger.error(f"Error updating last login: {e}")

    @staticmethod
    def get_all_users() -> List[Dict[str, Any]]:
        """Get all active users without sensitive data"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, name, email, occupation, age, location, user_number,     
                           is_active, is_verified, created_at, last_login
                    FROM users
                    WHERE is_active = 1
                    ORDER BY created_at DESC
                """)

                users = []
                for row in cursor.fetchall():
                    users.append(dict(row))

                return users

        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            raise DatabaseError("Failed to retrieve users")

    @staticmethod
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
            # Try user_id first
            data_file = TEST_DATA_DIR / user_id / f"{data_type}.json"
            
            # If not found and user_id looks like a UUID/number, try finding by name 
            if not data_file.exists():
                user = UserManager.get_user_by_id(user_id)
                if user and user.get("name"):
                    data_file = TEST_DATA_DIR / user["name"].strip() / f"{data_type}.json"
            
            if data_file.exists():
                try:
                    with open(data_file, "r") as f:
                        result[data_type] = json.load(f)
                except Exception as e:
                    logger.error(f"Error loading {data_type} for user {user_id}: {e}")
        return result


# Legacy compatibility functions
def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Legacy function for backward compatibility"""
    return UserManager.authenticate_user(username, password)

def get_all_users() -> List[Dict[str, Any]]:
    """Legacy function for backward compatibility"""
    return UserManager.get_all_users()

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Legacy function for backward compatibility"""
    return UserManager.get_user_by_id(user_id)

def get_all_user_data(user_id: str) -> Dict[str, Any]:
    """Legacy function for backward compatibility"""
    return UserManager.get_all_user_data(user_id)