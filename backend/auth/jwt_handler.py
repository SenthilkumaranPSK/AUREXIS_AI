"""
JWT Token Handler
Generate and validate JWT tokens
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import jwt
from passlib.context import CryptContext
import os
import logging
from uuid import uuid4

logger = logging.getLogger(__name__)

# JWT Configuration - REQUIRE environment variable
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    # Check if we're in development
    if os.getenv("ENVIRONMENT", "development") == "production":
        raise ValueError("JWT_SECRET_KEY environment variable must be set in production")
    else:
        logger.warning("⚠️  JWT_SECRET_KEY not set - using default for development only!")
        SECRET_KEY = "dev-jwt-secret-CHANGE-IN-PRODUCTION"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30

# Password hashing
# Use pbkdf2_sha256 to avoid bcrypt backend incompatibilities in some environments.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    # Add a unique identifier so refresh tokens are never duplicated.
    # This avoids DB constraint violations on `refresh_tokens.token` (UNIQUE).
    to_encode.update({"exp": expire, "type": "refresh", "jti": uuid4().hex})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict]:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None


def verify_token(token: str, token_type: str = "access") -> Optional[Dict]:
    """Verify token and check type"""
    payload = decode_token(token)
    if payload and payload.get("type") == token_type:
        return payload
    return None


class JWTHandler:
    """Backward-compatible class wrapper around JWT helper functions."""

    def create_access_token(self, data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        return create_access_token(data, expires_delta)

    def create_refresh_token(self, data: Dict) -> str:
        return create_refresh_token(data)

    def decode_token(self, token: str) -> Optional[Dict]:
        return decode_token(token)

    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict]:
        return verify_token(token, token_type)

    def hash_password(self, password: str) -> str:
        return hash_password(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)
