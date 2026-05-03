"""
Standardized Error Handling for AUREXIS AI
Provides consistent error responses with proper HTTP status codes
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response format"""
    success: bool = False
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: str
    path: Optional[str] = None


class AUREXISError(Exception):
    """Base exception class for AUREXIS AI"""
    
    def __init__(
        self,
        error_code: str,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class ValidationError(AUREXISError):
    """Validation related errors"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="VALIDATION_ERROR",
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class AuthenticationError(AUREXISError):
    """Authentication related errors"""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="AUTHENTICATION_ERROR",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )


class AuthorizationError(AUREXISError):
    """Authorization related errors"""
    
    def __init__(self, message: str = "Access denied", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="AUTHORIZATION_ERROR",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            details=details
        )


class NotFoundError(AUREXISError):
    """Resource not found errors"""
    
    def __init__(self, resource: str, identifier: str = "", details: Optional[Dict[str, Any]] = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(
            error_code="NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )


class ConflictError(AUREXISError):
    """Resource conflict errors"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="CONFLICT",
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            details=details
        )


class RateLimitError(AUREXISError):
    """Rate limiting errors"""
    
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="RATE_LIMIT_EXCEEDED",
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details=details
        )


class DatabaseError(AUREXISError):
    """Database related errors"""
    
    def __init__(self, message: str = "Database operation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="DATABASE_ERROR",
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class ExternalServiceError(AUREXISError):
    """External service (e.g., Ollama) errors"""
    
    def __init__(self, service: str, message: str = "External service unavailable", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="EXTERNAL_SERVICE_ERROR",
            message=f"{service}: {message}",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )


class BusinessLogicError(AUREXISError):
    """Business logic validation errors"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="BUSINESS_LOGIC_ERROR",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


# Error code to HTTP status mapping
ERROR_STATUS_MAP = {
    "VALIDATION_ERROR": status.HTTP_422_UNPROCESSABLE_ENTITY,
    "AUTHENTICATION_ERROR": status.HTTP_401_UNAUTHORIZED,
    "AUTHORIZATION_ERROR": status.HTTP_403_FORBIDDEN,
    "NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "CONFLICT": status.HTTP_409_CONFLICT,
    "RATE_LIMIT_EXCEEDED": status.HTTP_429_TOO_MANY_REQUESTS,
    "DATABASE_ERROR": status.HTTP_500_INTERNAL_SERVER_ERROR,
    "EXTERNAL_SERVICE_ERROR": status.HTTP_503_SERVICE_UNAVAILABLE,
    "BUSINESS_LOGIC_ERROR": status.HTTP_400_BAD_REQUEST,
    "INTERNAL_ERROR": status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def create_error_response(
    error_code: str,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    path: Optional[str] = None
) -> ErrorResponse:
    """Create a standardized error response"""
    from datetime import datetime
    
    return ErrorResponse(
        error_code=error_code,
        message=message,
        details=details,
        timestamp=datetime.now().isoformat(),
        path=path
    )


def handle_aurexis_error(error: AUREXISError, path: Optional[str] = None) -> HTTPException:
    """Convert AUREXIS error to HTTPException"""
    return HTTPException(
        status_code=error.status_code,
        detail=create_error_response(
            error_code=error.error_code,
            message=error.message,
            details=error.details,
            path=path
        ).dict()
    )
