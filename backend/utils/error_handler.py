"""
Centralized Error Handling and Custom Exceptions
"""
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Union, Dict, Any
import traceback
import logging

logger = logging.getLogger(__name__)


# ── Custom Exceptions ──────────────────────────────────────────────────────

class AurexisException(Exception):
    """Base exception for Aurexis application"""
    def __init__(self, message: str, status_code: int = 500, details: Dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(AurexisException):
    """Authentication failed"""
    def __init__(self, message: str = "Authentication failed", details: Dict = None):
        super().__init__(message, status_code=401, details=details)


class AuthorizationError(AurexisException):
    """User not authorized"""
    def __init__(self, message: str = "Not authorized", details: Dict = None):
        super().__init__(message, status_code=403, details=details)


class ResourceNotFoundError(AurexisException):
    """Resource not found"""
    def __init__(self, resource: str, resource_id: str = None):
        message = f"{resource} not found"
        if resource_id:
            message += f": {resource_id}"
        super().__init__(message, status_code=404, details={"resource": resource, "id": resource_id})


class ValidationError(AurexisException):
    """Data validation failed"""
    def __init__(self, message: str, field: str = None, details: Dict = None):
        details = details or {}
        if field:
            details["field"] = field
        super().__init__(message, status_code=422, details=details)


class BusinessLogicError(AurexisException):
    """Business logic constraint violated"""
    def __init__(self, message: str, details: Dict = None):
        super().__init__(message, status_code=400, details=details)


class ExternalServiceError(AurexisException):
    """External service call failed"""
    def __init__(self, service: str, message: str = None, details: Dict = None):
        message = message or f"{service} service unavailable"
        details = details or {}
        details["service"] = service
        super().__init__(message, status_code=503, details=details)


class RateLimitError(AurexisException):
    """Rate limit exceeded"""
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None):
        details = {}
        if retry_after:
            details["retry_after"] = retry_after
        super().__init__(message, status_code=429, details=details)


class DataEncryptionError(AurexisException):
    """Data encryption/decryption failed"""
    def __init__(self, message: str = "Encryption operation failed", details: Dict = None):
        super().__init__(message, status_code=500, details=details)


# ── Error Response Formatter ───────────────────────────────────────────────

def format_error_response(
    status_code: int,
    message: str,
    details: Dict = None,
    request_id: str = None
) -> Dict[str, Any]:
    """
    Format error response consistently
    
    Args:
        status_code: HTTP status code
        message: Error message
        details: Additional error details
        request_id: Request tracking ID
        
    Returns:
        Formatted error response dictionary
    """
    response = {
        "success": False,
        "error": {
            "code": status_code,
            "message": message,
            "type": get_error_type(status_code)
        }
    }
    
    if details:
        response["error"]["details"] = details
    
    if request_id:
        response["request_id"] = request_id
    
    return response


def get_error_type(status_code: int) -> str:
    """Get error type from status code"""
    error_types = {
        400: "bad_request",
        401: "authentication_error",
        403: "authorization_error",
        404: "not_found",
        422: "validation_error",
        429: "rate_limit_error",
        500: "internal_server_error",
        503: "service_unavailable"
    }
    return error_types.get(status_code, "unknown_error")


# ── Exception Handlers ─────────────────────────────────────────────────────

async def aurexis_exception_handler(request: Request, exc: AurexisException):
    """Handle custom Aurexis exceptions"""
    request_id = request.headers.get("X-Request-ID")
    
    # Log error
    logger.error(
        f"AurexisException: {exc.message}",
        extra={
            "status_code": exc.status_code,
            "details": exc.details,
            "request_id": request_id,
            "path": request.url.path
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            status_code=exc.status_code,
            message=exc.message,
            details=exc.details,
            request_id=request_id
        )
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions"""
    request_id = request.headers.get("X-Request-ID")
    
    logger.warning(
        f"HTTPException: {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "request_id": request_id,
            "path": request.url.path
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            status_code=exc.status_code,
            message=str(exc.detail),
            request_id=request_id
        )
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    request_id = request.headers.get("X-Request-ID")
    
    # Format validation errors
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(
        f"ValidationError: {len(errors)} validation errors",
        extra={
            "errors": errors,
            "request_id": request_id,
            "path": request.url.path
        }
    )
    
    return JSONResponse(
        status_code=422,
        content=format_error_response(
            status_code=422,
            message="Validation error",
            details={"errors": errors},
            request_id=request_id
        )
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    request_id = request.headers.get("X-Request-ID")
    
    # Log full traceback
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "request_id": request_id,
            "path": request.url.path,
            "traceback": traceback.format_exc()
        }
    )
    
    # Don't expose internal errors in production
    from config_manager import get_settings
    settings = get_settings()
    
    if settings.is_production:
        message = "An internal error occurred"
        details = None
    else:
        message = str(exc)
        details = {"traceback": traceback.format_exc()}
    
    return JSONResponse(
        status_code=500,
        content=format_error_response(
            status_code=500,
            message=message,
            details=details,
            request_id=request_id
        )
    )


# ── Error Handler Registration ─────────────────────────────────────────────

def register_error_handlers(app):
    """Register all error handlers with FastAPI app"""
    app.add_exception_handler(AurexisException, aurexis_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
