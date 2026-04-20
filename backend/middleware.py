"""
AUREXIS AI — Middleware
Request tracking, rate limiting, CORS, and security headers
"""

import time
import uuid
from typing import Callable
from fastapi import Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from config import settings
from logger import logger, log_request, log_security_event
from cache import rate_limiter
from security import get_client_ip


# ── Request ID Middleware ──────────────────────────────────────────────────

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to each request"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response


# ── Logging Middleware ─────────────────────────────────────────────────────

class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests with timing"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        # Get user ID if available
        user_id = getattr(request.state, "user_id", None)
        
        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000
            
            # Log request
            log_request(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
                user_id=user_id
            )
            
            # Add timing header
            response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"
            
            return response
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.exception(f"Request failed: {request.method} {request.url.path}")
            
            # Log failed request
            log_request(
                method=request.method,
                path=request.url.path,
                status_code=500,
                duration_ms=duration_ms,
                user_id=user_id
            )
            raise


# ── Rate Limiting Middleware ───────────────────────────────────────────────

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limit requests per IP address"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.enabled = settings.RATE_LIMIT_ENABLED
    
    async def dispatch(self, request: Request, call_next: Callable):
        if not self.enabled:
            return await call_next(request)
        
        # Skip rate limiting for health checks
        if request.url.path in ["/", "/health", "/metrics"]:
            return await call_next(request)
        
        # Get client identifier
        client_ip = get_client_ip(request)
        
        # Different limits for different endpoints
        if "/api/chat" in request.url.path:
            max_requests = settings.RATE_LIMIT_CHAT_PER_MINUTE
            window = 60
        elif "/api/user/" in request.url.path and "/forecast/ml" in request.url.path:
            max_requests = settings.RATE_LIMIT_ML_PER_HOUR
            window = 3600
        else:
            max_requests = settings.RATE_LIMIT_PER_MINUTE
            window = 60
        
        # Check rate limit
        is_allowed, remaining = rate_limiter.is_allowed(
            identifier=f"{client_ip}:{request.url.path}",
            max_requests=max_requests,
            window=window
        )
        
        if not is_allowed:
            log_security_event(
                "Rate limit exceeded",
                details=f"IP: {client_ip}, Path: {request.url.path}"
            )
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later.",
                headers={"Retry-After": str(window)}
            )
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(window)
        
        return response


# ── Security Headers Middleware ────────────────────────────────────────────

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Content Security Policy
        if settings.ENVIRONMENT == "production":
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self' http://localhost:11434"
            )
        
        return response


# ── Error Handler Middleware ───────────────────────────────────────────────

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Global error handler"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        try:
            return await call_next(request)
        except HTTPException:
            # Let FastAPI handle HTTP exceptions
            raise
        except Exception as e:
            logger.exception(f"Unhandled exception: {str(e)}")
            
            # Return generic error in production
            if settings.ENVIRONMENT == "production":
                return Response(
                    content='{"detail": "Internal server error"}',
                    status_code=500,
                    media_type="application/json"
                )
            else:
                # Return detailed error in development
                return Response(
                    content=f'{{"detail": "Internal server error: {str(e)}"}}',
                    status_code=500,
                    media_type="application/json"
                )


# ── CORS Configuration ─────────────────────────────────────────────────────

def setup_cors(app):
    """Configure CORS middleware"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
        expose_headers=["X-Request-ID", "X-Process-Time", "X-RateLimit-*"],
    )


# ── Middleware Setup ───────────────────────────────────────────────────────

def setup_middleware(app):
    """Setup all middleware in correct order"""
    
    # Order matters! First added = outermost layer
    
    # 1. Error handling (outermost)
    app.add_middleware(ErrorHandlerMiddleware)
    
    # 2. Security headers
    app.add_middleware(SecurityHeadersMiddleware)
    
    # 3. Rate limiting
    app.add_middleware(RateLimitMiddleware)
    
    # 4. Logging
    app.add_middleware(LoggingMiddleware)
    
    # 5. Request ID (innermost)
    app.add_middleware(RequestIDMiddleware)
    
    # 6. CORS (handled separately)
    setup_cors(app)
    
    logger.info("Middleware configured successfully")
