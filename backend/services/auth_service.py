"""
Authentication Service
Business logic for authentication operations
"""

from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta, timezone
from user_manager_json import UserManagerJSON
from auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    verify_token,
    verify_password
)
import logging

logger = logging.getLogger(__name__)


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
        # Note: Signup not fully supported in JSON mode
        # This is a placeholder for future implementation
        raise NotImplementedError("Signup is not available in JSON-based mode. Please contact administrator.")
    
    @staticmethod
    def login(identifier: str, password: str) -> Dict:
        """
        Authenticate user and return tokens
        Returns: user dict and tokens
        """
        user = UserManagerJSON.authenticate_user(identifier, password)
        if not user:
            raise ValueError("Invalid credentials")
        
        if not user.get("is_active", True):
            raise ValueError("Account is deactivated")
        
        # Generate tokens
        user_id = user.get("id") or user.get("user_id") or user.get("user_number")
        access_token = create_access_token({"sub": user_id, "email": user.get("email", "")})
        refresh_token = create_refresh_token({"sub": user_id})
        
        # Note: Refresh tokens are not persisted in JSON mode
        logger.info(f"User logged in: {user.get('name')}")
        
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
        
        # Get user
        user = UserManagerJSON.get_user_by_id(user_id)
        if not user or not user.get("is_active", True):
            raise ValueError("User not found or inactive")
        
        # Generate new tokens
        new_access_token = create_access_token({"sub": user["id"], "email": user.get("email", "")})
        new_refresh_token = create_refresh_token({"sub": user["id"]})
        
        return new_access_token, new_refresh_token
    
    @staticmethod
    def logout(user_id: str, refresh_token: Optional[str] = None):
        """
        Logout user
        Note: In JSON mode, tokens are not persisted, so logout is client-side only
        """
        logger.info(f"User logged out: {user_id}")
        return True
    
    @staticmethod
    def change_password(user_id: str, current_password: str, new_password: str) -> bool:
        """
        Change user password
        Note: Not supported in JSON mode
        """
        raise NotImplementedError("Password change is not available in JSON-based mode. Please contact administrator.")
    
    @staticmethod
    def get_user_profile(user_id: str) -> Dict:
        """Get user profile"""
        user = UserManagerJSON.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user
    
    @staticmethod
    def update_user_profile(user_id: str, **kwargs) -> Dict:
        """Update user profile"""
        # Note: Profile updates not supported in JSON mode
        raise NotImplementedError("Profile updates are not available in JSON-based mode. Please contact administrator.")
