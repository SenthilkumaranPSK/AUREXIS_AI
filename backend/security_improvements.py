"""
Security Improvements for AUREXIS AI
Implement these enhancements for better security
"""

from passlib.context import CryptContext
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
import re
from typing import Optional
import redis
import json

# 1. Use bcrypt instead of SHA-256
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Secure password hashing with bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against bcrypt hash"""
    return pwd_context.verify(plain_password, hashed_password)

# 2. JWT Token Management
SECRET_KEY = "your-secret-key-change-in-production"  # Use env variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class JWTHandler:
    """JWT Token handler for secure authentication"""
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

# 3. Input Validation
class InputValidator:
    """Input validation utilities"""
    
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        return bool(InputValidator.EMAIL_REGEX.match(email))
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain digit"
        if not re.search(r'[@$!%*?&]', password):
            return False, "Password must contain special character"
        return True, "Password is strong"
    
    @staticmethod
    def sanitize_input(value: str, max_length: int = 255) -> str:
        """Sanitize user input"""
        if not value:
            return ""
        # Remove potential XSS characters
        value = re.sub(r'[<>\"\'&]', '', value)
        return value[:max_length].strip()

# 4. Rate Limiting
class RateLimiter:
    """Redis-based rate limiting"""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.requests = {}  # Fallback to memory if Redis not available
    
    def is_allowed(self, key: str, max_requests: int = 100, window: int = 60) -> bool:
        """Check if request is allowed under rate limit"""
        current_time = datetime.utcnow().timestamp()
        
        if self.redis:
            # Use Redis for distributed rate limiting
            pipe = self.redis.pipeline()
            pipe.zremrangebyscore(key, 0, current_time - window)
            pipe.zcard(key)
            pipe.zadd(key, {str(current_time): current_time})
            pipe.expire(key, window)
            _, current_count, _, _ = pipe.execute()
            return current_count <= max_requests
        else:
            # Memory-based rate limiting (for development)
            if key not in self.requests:
                self.requests[key] = []
            
            # Clean old requests
            self.requests[key] = [t for t in self.requests[key] if t > current_time - window]
            
            if len(self.requests[key]) >= max_requests:
                return False
            
            self.requests[key].append(current_time)
            return True

# 5. Session Management with Redis
class SessionManager:
    """Redis-based session management"""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.sessions = {}  # Fallback
    
    def create_session(self, user_id: str, data: dict, expire_hours: int = 24) -> str:
        """Create new session"""
        import uuid
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id": user_id,
            "data": data,
            "created_at": datetime.utcnow().isoformat()
        }
        
        if self.redis:
            self.redis.setex(f"session:{session_id}", expire_hours * 3600, json.dumps(session_data))
        else:
            self.sessions[session_id] = session_data
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session data"""
        if self.redis:
            data = self.redis.get(f"session:{session_id}")
            return json.loads(data) if data else None
        return self.sessions.get(session_id)
    
    def delete_session(self, session_id: str):
        """Delete session"""
        if self.redis:
            self.redis.delete(f"session:{session_id}")
        else:
            self.sessions.pop(session_id, None)

# 6. Audit Logging
class AuditLogger:
    """Security audit logging"""
    
    @staticmethod
    def log_event(event_type: str, user_id: Optional[str], details: dict, request: Request):
        """Log security event"""
        from datetime import datetime
        import logging
        
        audit_log = logging.getLogger("audit")
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "ip_address": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "details": details
        }
        
        audit_log.info(json.dumps(log_entry))

# Implementation Example for server.py:
"""
from security_improvements import (
    JWTHandler, InputValidator, RateLimiter, 
    SessionManager, AuditLogger, hash_password, verify_password
)

# Initialize components
jwt_handler = JWTHandler()
rate_limiter = RateLimiter()
session_manager = SessionManager()

@app.post("/api/login")
async def login(request: Request, credentials: LoginRequest):
    # Rate limiting
    client_ip = request.client.host
    if not rate_limiter.is_allowed(f"login:{client_ip}", max_requests=5, window=300):
        AuditLogger.log_event("rate_limit_exceeded", None, {"endpoint": "login"}, request)
        raise HTTPException(status_code=429, detail="Too many login attempts")
    
    # Input validation
    if not InputValidator.validate_email(credentials.username):
        # Try as username
        pass
    
    # Authenticate
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        AuditLogger.log_event("failed_login", None, {"username": credentials.username}, request)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    access_token = jwt_handler.create_access_token(
        data={"sub": user["id"], "email": user["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Create session
    session_id = session_manager.create_session(user["id"], user)
    
    # Log successful login
    AuditLogger.log_event("successful_login", user["id"], {}, request)
    
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "session_id": session_id,
        "user": user
    }
"""
