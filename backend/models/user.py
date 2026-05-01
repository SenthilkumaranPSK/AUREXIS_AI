"""
User Model
Database operations for users
"""

from typing import Optional, Dict
from datetime import datetime, timezone
import uuid
import secrets
from database.connection_enhanced import get_db
from auth.jwt_handler import hash_password, verify_password


class UserModel:
    """User database operations"""
    
    @staticmethod
    def _normalize_user_record(user: Dict) -> Dict:
        """Normalize nullable DB fields to API-safe values."""
        is_active = user.get("is_active")
        is_verified = user.get("is_verified")
        user["is_active"] = True if is_active is None else bool(is_active)
        user["is_verified"] = False if is_verified is None else bool(is_verified)
        user["created_at"] = user.get("created_at") or datetime.now(timezone.utc).isoformat()
        return user

    @staticmethod
    def create_user(
        name: str,
        email: str,
        password: str,
        occupation: Optional[str] = None,
        age: Optional[int] = None,
        location: Optional[str] = None
    ) -> Dict:
        """Create a new user"""
        user_id = str(uuid.uuid4())
        # `user_number` is required by your current DB schema (NOT NULL + UNIQUE).
        user_number = f"AUREXIS_{secrets.token_hex(4).upper()}"  # length >= 8
        password_hash = hash_password(password)
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (id, name, email, password_hash, user_number, occupation, age, location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, name, email, password_hash, user_number, occupation, age, location))
            cursor.execute("""
                SELECT id, name, email, occupation, age, location,
                       is_active, is_verified, created_at, last_login
                FROM users WHERE id = ?
            """, (user_id,))
            row = cursor.fetchone()
            if not row:
                return None

            return UserModel._normalize_user_record(dict(row))
    
    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, email, occupation, age, location, 
                       is_active, is_verified, created_at, last_login
                FROM users WHERE id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            if row:
                return UserModel._normalize_user_record(dict(row))
            return None
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict]:
        """Get user by email"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, email, password_hash, occupation, age, location,
                       is_active, is_verified, created_at, last_login
                FROM users WHERE email = ?
            """, (email,))
            
            row = cursor.fetchone()
            if row:
                return UserModel._normalize_user_record(dict(row))
            return None
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[Dict]:
        """Authenticate user with email and password"""
        user = UserModel.get_user_by_email(email)
        if not user:
            return None
        
        if not verify_password(password, user['password_hash']):
            return None
        
        # Update last login
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET last_login = ? WHERE id = ?
            """, (datetime.now(timezone.utc).isoformat(), user['id']))
        
        # Remove password hash from returned user
        user.pop('password_hash', None)
        return user
    
    @staticmethod
    def update_user(user_id: str, **kwargs) -> Optional[Dict]:
        """Update user information"""
        allowed_fields = ['name', 'occupation', 'age', 'location']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            return UserModel.get_user_by_id(user_id)
        
        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        # SQLite parameter binding is more reliable with ISO strings.
        values = list(update_fields.values()) + [datetime.now(timezone.utc).isoformat(), user_id]
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE users 
                SET {set_clause}, updated_at = ?
                WHERE id = ?
            """, values)
        
        return UserModel.get_user_by_id(user_id)
    
    @staticmethod
    def change_password(user_id: str, new_password: str) -> bool:
        """Change user password"""
        password_hash = hash_password(new_password)
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET password_hash = ?, updated_at = ?
                WHERE id = ?
            """, (password_hash, datetime.now(timezone.utc).isoformat(), user_id))
            
            return cursor.rowcount > 0
    
    @staticmethod
    def delete_user(user_id: str) -> bool:
        """Delete user (soft delete by setting is_active to False)"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET is_active = 0, updated_at = ?
                WHERE id = ?
            """, (datetime.now(timezone.utc).isoformat(), user_id))
            
            return cursor.rowcount > 0
