"""
Input Validation Middleware

Additional validation for request data.
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import re


class ValidationMiddleware(BaseHTTPMiddleware):
    """Middleware for additional input validation"""
    
    # Maximum request body size (10 MB)
    MAX_BODY_SIZE = 10 * 1024 * 1024
    
    # Suspicious patterns (basic XSS/SQL injection detection)
    SUSPICIOUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'\bon\w+\s*=',
        r'\bDROP\s+TABLE\b',
        r'\bDELETE\s+FROM\b',
        r'\bINSERT\s+INTO\b',
        r'\bUPDATE\s+.*\bSET\b',
        r'\bUNION\s+SELECT\b',
    ]
    
    async def dispatch(self, request: Request, call_next):
        # Check request body size
        if request.headers.get("content-length"):
            content_length = int(request.headers["content-length"])
            if content_length > self.MAX_BODY_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail=f"Request body too large. Maximum size is {self.MAX_BODY_SIZE / 1024 / 1024}MB"
                )
        
        # Check for suspicious patterns in query parameters
        query_string = str(request.url.query)
        for pattern in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, query_string, re.IGNORECASE):
                raise HTTPException(
                    status_code=400,
                    detail="Suspicious input detected"
                )
        
        response = await call_next(request)
        return response
