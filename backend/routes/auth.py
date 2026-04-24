"""
Authentication Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Dict
from schemas.auth import (
    SignupRequest,
    LoginRequest,
    LoginResponse,
    TokenResponse,
    RefreshTokenRequest,
    ChangePasswordRequest,
    UserResponse
)
from services.auth_service import AuthService
from auth.dependencies import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

# Rate limiter for auth endpoints (stricter limits)
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def signup(request: Request, signup_request: SignupRequest):
    """Register a new user (Rate limited: 5 requests/minute)"""
    try:
        result = AuthService.signup(
            name=signup_request.name,
            email=signup_request.email,
            password=signup_request.password,
            occupation=signup_request.occupation,
            age=signup_request.age,
            location=signup_request.location
        )

        return LoginResponse(
            success=True,
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            user=UserResponse(**result["user"])
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create account"
        )


@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")
async def login(request: Request, login_request: LoginRequest):
    """Authenticate user and return tokens (Rate limited: 5 requests/minute)"""
    try:
        result = AuthService.login(login_request.email, login_request.password)

        return LoginResponse(
            success=True,
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            user=UserResponse(**result["user"])
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token"""
    try:
        access_token, refresh_token = AuthService.refresh_access_token(request.refresh_token)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout")
async def logout(
    refresh_token: str = None,
    current_user: Dict = Depends(get_current_user)
):
    """Logout user by revoking tokens"""
    try:
        user_id = current_user.get("sub")
        AuthService.logout(user_id, refresh_token)
        
        return {"success": True, "message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Change user password"""
    try:
        user_id = current_user.get("sub")
        success = AuthService.change_password(
            user_id,
            request.current_password,
            request.new_password
        )
        
        if success:
            return {"success": True, "message": "Password changed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to change password"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: Dict = Depends(get_current_user)):
    """Get current user profile"""
    try:
        user_id = current_user.get("sub")
        user = AuthService.get_user_profile(user_id)
        
        return UserResponse(**user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch profile"
        )


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    name: str = None,
    occupation: str = None,
    age: int = None,
    location: str = None,
    current_user: Dict = Depends(get_current_user)
):
    """Update user profile"""
    try:
        user_id = current_user.get("sub")
        
        # Build update dict
        updates = {}
        if name is not None:
            updates["name"] = name
        if occupation is not None:
            updates["occupation"] = occupation
        if age is not None:
            updates["age"] = age
        if location is not None:
            updates["location"] = location
        
        user = AuthService.update_user_profile(user_id, **updates)
        
        return UserResponse(**user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )
