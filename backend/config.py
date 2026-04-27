"""
AUREXIS AI — Configuration Management
Centralized settings with validation and environment-specific configs
"""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings with validation"""
    
    # ── Application ────────────────────────────────────────────────────────
    APP_NAME: str = "AUREXIS AI"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # ── Server ─────────────────────────────────────────────────────────────
    HOST: str = "127.0.0.1"  # Changed from 0.0.0.0 for Windows compatibility
    PORT: int = 8000
    WORKERS: int = 4
    RELOAD: bool = True
    
    # ── Security ───────────────────────────────────────────────────────────
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-CHANGE-IN-PRODUCTION")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    PASSWORD_MIN_LENGTH: int = 8
    
    # ── CORS ───────────────────────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
    ]
    ALLOWED_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    ALLOWED_HEADERS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    
    # ── Database ───────────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./aurexis.db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # ── Redis Cache ────────────────────────────────────────────────────────
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    CACHE_TTL: int = 3600  # 1 hour
    CACHE_ENABLED: bool = True
    
    # ── Ollama AI ──────────────────────────────────────────────────────────
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "deepseek-v3.1:671b-cloud"
    OLLAMA_TIMEOUT: int = 120
    OLLAMA_MAX_RETRIES: int = 3
    OLLAMA_CONTEXT_WINDOW: int = 10  # Last N conversation turns
    
    # ── Rate Limiting ──────────────────────────────────────────────────────
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_CHAT_PER_MINUTE: int = 10
    RATE_LIMIT_ML_PER_HOUR: int = 20
    
    # ── Logging ────────────────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/aurexis.log"
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # ── ML & Analytics ─────────────────────────────────────────────────────
    ML_FORECAST_STEPS: int = 6
    ML_CACHE_HOURS: int = 24
    ANALYTICS_CACHE_MINUTES: int = 30
    BACKGROUND_TASKS_ENABLED: bool = True
    
    # ── File Storage ───────────────────────────────────────────────────────
    USER_DATA_DIR: str = "user_data"
    UPLOAD_MAX_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".json", ".csv", ".pdf"]
    
    # ── Monitoring ─────────────────────────────────────────────────────────
    METRICS_ENABLED: bool = True
    SENTRY_DSN: Optional[str] = None
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1
    
    # ── Email (Future) ─────────────────────────────────────────────────────
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@aurexis.ai"
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()


# Environment-specific overrides
if settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.RELOAD = False
    settings.DATABASE_ECHO = False
    settings.LOG_LEVEL = "WARNING"
    
    # Validate critical security settings in production
    if settings.SECRET_KEY == "dev-secret-key-CHANGE-IN-PRODUCTION":
        raise ValueError(
            "SECRET_KEY must be set via environment variable in production. "
            "Generate one with: openssl rand -hex 32"
        )
elif settings.ENVIRONMENT == "testing":
    settings.DATABASE_URL = "sqlite:///./test_aurexis.db"
    settings.CACHE_ENABLED = False
    settings.RATE_LIMIT_ENABLED = False
