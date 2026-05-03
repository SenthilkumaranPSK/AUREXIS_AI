"""
AUREXIS AI — Logging Configuration
Structured logging with rotation and multiple handlers
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime, timezone
from typing import Optional
import json

from config import settings


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "duration"):
            log_data["duration_ms"] = record.duration
        
        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


def build_formatter(format_string: str) -> logging.Formatter:
    """Return a formatter object, supporting `json` as a config shortcut."""
    if format_string.strip().lower() == "json":
        return JSONFormatter()
    return logging.Formatter(format_string)


def setup_logger(name: str = "aurexis") -> logging.Logger:
    """
    Setup application logger with multiple handlers
    
    Handlers:
    - Console: Colored output for development
    - File: Rotating file handler for all logs
    - Error File: Separate file for errors only
    - JSON File: Structured JSON logs for production
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create logs directory
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)
    
    # ── Console Handler ────────────────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    
    if settings.ENVIRONMENT == "development":
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
    else:
        console_formatter = build_formatter(settings.LOG_FORMAT)
    
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # ── File Handler (All Logs) ────────────────────────────────────────────
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = build_formatter(settings.LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # ── Error File Handler ─────────────────────────────────────────────────
    error_file = log_dir / "errors.log"
    error_handler = RotatingFileHandler(
        error_file,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    logger.addHandler(error_handler)
    
    # ── JSON Handler (Production) ──────────────────────────────────────────
    if settings.ENVIRONMENT == "production":
        json_file = log_dir / "aurexis.json.log"
        json_handler = TimedRotatingFileHandler(
            json_file,
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        json_handler.setLevel(logging.INFO)
        json_handler.setFormatter(JSONFormatter())
        logger.addHandler(json_handler)
    
    return logger


# Global logger instance
logger = setup_logger()


# ── Logging Utilities ──────────────────────────────────────────────────────

def log_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    user_id: Optional[str] = None
):
    """Log HTTP request with structured data"""
    extra = {
        "duration": duration_ms,
        "user_id": user_id,
    }
    
    if status_code >= 500:
        logger.error(
            f"{method} {path} - {status_code} - {duration_ms:.2f}ms",
            extra=extra
        )
    elif status_code >= 400:
        logger.warning(
            f"{method} {path} - {status_code} - {duration_ms:.2f}ms",
            extra=extra
        )
    else:
        logger.info(
            f"{method} {path} - {status_code} - {duration_ms:.2f}ms",
            extra=extra
        )


def log_exception(
    exc: Exception,
    context: Optional[str] = None,
    user_id: Optional[str] = None
):
    """Log exception with context"""
    extra = {"user_id": user_id} if user_id else {}
    
    if context:
        logger.exception(f"{context}: {str(exc)}", extra=extra)
    else:
        logger.exception(f"Unhandled exception: {str(exc)}", extra=extra)


def log_security_event(event: str, user_id: Optional[str] = None, details: Optional[str] = None):
    """Log security-related events"""
    extra = {"user_id": user_id} if user_id else {}
    message = f"SECURITY: {event}"
    if details:
        message += f" - {details}"
    logger.warning(message, extra=extra)
