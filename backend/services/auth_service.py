"""
Authentication Service
Business logic for authentication operations
"""

from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta, timezone
from models.user import UserModel
from auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    verify_token,
    verify_password
)
from database.connection import get_db


class AuthService:
    """Authentication business logic"""
    
    @staticmethod
    def signup(
        name: str,
        email: str,
        password: str,
        occupation: Optional[str] = None,
        age: Optional[int] = None,
        location: Optional[str] = None
    ) -> Dict:
        """
        Register a new user
        Returns: user dict and tokens
        """
        # Check if email already exists
        existing_user = UserModel.get_user_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create user
        user = UserModel.create_user(
            name=name,
            email=email,
            password=password,
            occupation=occupation,
            age=age,
            location=location
        )
        
        # Generate tokens
        access_token = create_access_token({"sub": user["id"], "email": user["email"]})
        refresh_token = create_refresh_token({"sub": user["id"]})
        
        # Store refresh token in database
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO refresh_tokens (user_id, token, expires_at)
                VALUES (?, ?, ?)
            """, (
                user["id"],
                refresh_token,
                datetime.now(timezone.utc) + timedelta(days=30)
            ))
        
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    @staticmethod
    def login(email: str, password: str) -> Dict:
        """
        Authenticate user and return tokens
        Returns: user dict and tokens
        """
        user = UserModel.authenticate_user(email, password)
        if not user:
            raise ValueError("Invalid email or password")
        
        if not user.get("is_active"):
            raise ValueError("Account is deactivated")
        
        # Generate tokens
        access_token = create_access_token({"sub": user["id"], "email": user["email"]})
        refresh_token = create_refresh_token({"sub": user["id"]})
        
        # Store refresh token
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO refresh_tokens (user_id, token, expires_at)
                VALUES (?, ?, ?)
            """, (
                user["id"],
                refresh_token,
                datetime.now(timezone.utc) + timedelta(days=30)
            ))
        
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> Tuple[str, str]:
        """
        Generate new access token from refresh token
        Returns: (new_access_token, new_refresh_token)
        """
        # Verify refresh token
        payload = verify_token(refresh_token, "refresh")
        if not payload:
            raise ValueError("Invalid or expired refresh token")
        
        user_id = payload.get("sub")
        
        # Check if token is in database and not revoked
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM refresh_tokens 
                WHERE user_id = ? AND token = ? AND is_revoked = 0
                AND expires_at > ?
            """, (user_id, refresh_token, datetime.now(timezone.utc)))
            
            token_record = cursor.fetchone()
            if not token_record:
                raise ValueError("Refresh token not found or revoked")
            
            # Revoke old refresh token
            cursor.execute("""
                UPDATE refresh_tokens SET is_revoked = 1 WHERE token = ?
            """, (refresh_token,))
        
        # Get user
        user = UserModel.get_user_by_id(user_id)
        if not user or not user.get("is_active"):
            raise ValueError("User not found or inactive")
        
        # Generate new tokens
        new_access_token = create_access_token({"sub": user["id"], "email": user["email"]})
        new_refresh_token = create_refresh_token({"sub": user["id"]})
        
        # Store new refresh token
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO refresh_tokens (user_id, token, expires_at)
                VALUES (?, ?, ?)
            """, (
                user["id"],
                new_refresh_token,
                datetime.now(timezone.utc) + timedelta(days=30)
            ))
        
        return new_access_token, new_refresh_token
    
    @staticmethod
    def logout(user_id: str, refresh_token: Optional[str] = None):
        """
        Logout user by revoking refresh tokens
        """
        with get_db() as conn:
            cursor = conn.cursor()
            if refresh_token:
                # Revoke specific token
                cursor.execute("""
                    UPDATE refresh_tokens 
                    SET is_revoked = 1 
                    WHERE user_id = ? AND token = ?
                """, (user_id, refresh_token))
            else:
                # Revoke all tokens for user
                cursor.execute("""
                    UPDATE refresh_tokens 
                    SET is_revoked = 1 
                    WHERE user_id = ?
                """, (user_id,))
    
    @staticmethod
    def change_password(user_id: str, current_password: str, new_password: str) -> bool:
        """
        Change user password
        """
        # Get user with password hash
        user = UserModel.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Get password hash
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("User not found")
            
            password_hash = row[0]
        
        # Verify current password
        if not verify_password(current_password, password_hash):
            raise ValueError("Current password is incorrect")
        
        # Change password
        success = UserModel.change_password(user_id, new_password)
        
        if success:
            # Revoke all refresh tokens (force re-login on all devices)
            AuthService.logout(user_id)
        
        return success
    
    @staticmethod
    def get_user_profile(user_id: str) -> Dict:
        """Get user profile"""
        user = UserModel.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user
    
    @staticmethod
    def update_user_profile(user_id: str, **kwargs) -> Dict:
        """Update user profile"""
        user = UserModel.update_user(user_id, **kwargs)
        if not user:
            raise ValueError("User not found")
        return user
