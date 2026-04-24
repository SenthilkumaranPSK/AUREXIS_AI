"""
Logging Configuration

Centralized logging configuration for the application.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from datetime import datetime, timezone
import json


# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)


class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging"""
    
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
            log_data["duration"] = record.duration
        
        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """Colored console formatter"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        # Format message
        message = super().format(record)
        
        return f"{color}[{timestamp}] {record.levelname:8s}{reset} {record.name:20s} | {message}"


def setup_logging(
    level: str = "INFO",
    log_file: str = "aurexis.log",
    json_log_file: str = "aurexis.json.log",
    error_log_file: str = "errors.log",
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5
):
    """
    Setup logging configuration
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Main log file name
        json_log_file: JSON log file name
        error_log_file: Error log file name
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
    """
    
    # Convert level string to logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Console handler with colored output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_formatter = ColoredFormatter(
        '%(name)s | %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for all logs
    file_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(numeric_level)
    file_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s %(name)-20s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # JSON file handler for structured logs
    json_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / json_log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    json_handler.setLevel(numeric_level)
    json_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(json_handler)
    
    # Error file handler for errors only
    error_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / error_log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    root_logger.addHandler(error_handler)
    
    # Set levels for third-party loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    # Log startup message
    root_logger.info("=" * 80)
    root_logger.info("AUREXIS AI Backend Starting")
    root_logger.info(f"Log Level: {level}")
    root_logger.info(f"Log Directory: {LOGS_DIR}")
    root_logger.info("=" * 80)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Convenience functions for logging with context
def log_with_context(logger: logging.Logger, level: str, message: str, **context):
    """
    Log message with additional context
    
    Args:
        logger: Logger instance
        level: Log level (debug, info, warning, error, critical)
        message: Log message
        **context: Additional context fields
    """
    log_func = getattr(logger, level.lower())
    
    # Create a log record with extra fields
    extra = {}
    for key, value in context.items():
        extra[key] = value
    
    log_func(message, extra=extra)


def log_request(logger: logging.Logger, method: str, path: str, status: int, duration: float, user_id: str = None):
    """
    Log HTTP request
    
    Args:
        logger: Logger instance
        method: HTTP method
        path: Request path
        status: Response status code
        duration: Request duration in seconds
        user_id: User ID (optional)
    """
    extra = {
        "request_id": f"{method}:{path}",
        "duration": duration
    }
    if user_id:
        extra["user_id"] = user_id
    
    level = "info" if status < 400 else "warning" if status < 500 else "error"
    message = f"{method} {path} - {status} ({duration:.3f}s)"
    
    log_with_context(logger, level, message, **extra)


def log_agent_execution(logger: logging.Logger, agent_name: str, duration: float, status: str, user_id: str = None):
    """
    Log agent execution
    
    Args:
        logger: Logger instance
        agent_name: Agent name
        duration: Execution duration in seconds
        status: Execution status (success, error)
        user_id: User ID (optional)
    """
    extra = {
        "duration": duration
    }
    if user_id:
        extra["user_id"] = user_id
    
    level = "info" if status == "success" else "error"
    message = f"Agent '{agent_name}' executed - {status} ({duration:.3f}s)"
    
    log_with_context(logger, level, message, **extra)


# Initialize logging on module import
setup_logging()
