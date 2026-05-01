"""
Enhanced Configuration Management for AUREXIS AI
Environment-specific settings with validation and defaults
"""

import os
from typing import List, Optional, Union
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from enum import Enum


class Environment(str, Enum):
    """Supported environments"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Supported log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EnhancedSettings(BaseSettings):
    """Enhanced settings with validation and environment awareness"""
    
    model_config = {"extra": "ignore"}
    
    # Environment configuration
    ENVIRONMENT: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Application environment"
    )
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    API_V2_PREFIX: str = "/api/v2"
    LEGACY_API_PREFIX: str = "/api"
    DOCS_URL: str = "/api/docs"
    REDOC_URL: str = "/api/redoc"
    OPENAPI_URL: str = "/api/openapi.json"
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    WORKERS: int = Field(default=1, description="Number of worker processes")
    
    # Security Configuration
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production-32chars-min", 
        min_length=32, 
        description="Secret key for security"
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_EXPIRE_DAYS: int = 7
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="sqlite:///./aurexis.db",
        description="Database connection URL"
    )
    DATABASE_POOL_SIZE: int = Field(default=5, description="Database connection pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=10, description="Database max overflow connections")
    DATABASE_POOL_TIMEOUT: int = Field(default=30, description="Database pool timeout")
    
    # Redis Configuration (optional)
    REDIS_HOST: str = Field(default="localhost", description="Redis host")
    REDIS_PORT: int = Field(default=6379, description="Redis port")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")
    REDIS_URL: Optional[str] = Field(default=None, description="Full Redis URL")
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000", 
            "http://localhost:5173", 
            "http://localhost:8080",
            "http://localhost:8081",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:8080",
            "http://127.0.0.1:8081"
        ],
        description="Allowed CORS origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = Field(default_factory=lambda: ["*"])
    CORS_ALLOW_HEADERS: List[str] = Field(default_factory=lambda: ["*"])
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 100
    RATE_LIMIT_AUTH_REQUESTS_PER_MINUTE: int = 5
    RATE_LIMIT_CHAT_PER_MINUTE: int = 20
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434",
        description="Ollama API base URL"
    )
    OLLAMA_MODEL: str = Field(
        default="deepseek-v3.1:671b-cloud",
        description="Default Ollama model"
    )
    OLLAMA_TIMEOUT: int = Field(default=30, description="Ollama request timeout")
    
    # Logging Configuration
    LOG_LEVEL: LogLevel = Field(default=LogLevel.INFO, description="Application log level")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE_PATH: Optional[str] = Field(default=None, description="Log file path")
    LOG_MAX_BYTES: int = Field(default=10485760, description="Max log file size in bytes")
    LOG_BACKUP_COUNT: int = Field(default=5, description="Number of log backup files")
    
    # Monitoring Configuration
    METRICS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    SENTRY_DSN: Optional[str] = Field(default=None, description="Sentry DSN for error tracking")
    PROMETHEUS_ENABLED: bool = True
    
    # Cache Configuration
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = Field(default=300, description="Cache TTL in seconds")
    CACHE_MAX_SIZE: int = Field(default=1000, description="Maximum cache size")
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = Field(default=10485760, description="Max file size in bytes (10MB)")
    UPLOAD_DIR: str = Field(default="uploads", description="Upload directory")
    
    # Email Configuration (optional)
    SMTP_HOST: Optional[str] = Field(default=None, description="SMTP host")
    SMTP_PORT: int = Field(default=587, description="SMTP port")
    SMTP_USERNAME: Optional[str] = Field(default=None, description="SMTP username")
    SMTP_PASSWORD: Optional[str] = Field(default=None, description="SMTP password")
    SMTP_TLS: bool = True
    
    # Background Tasks (Celery)
    CELERY_BROKER_URL: Optional[str] = Field(default=None, description="Celery broker URL")
    CELERY_RESULT_BACKEND: Optional[str] = Field(default=None, description="Celery result backend")
    
    # Feature Flags
    ENABLE_WEBSOCKETS: bool = True
    ENABLE_ANALYTICS: bool = True
    ENABLE_ML_FORECASTING: bool = True
    ENABLE_MULTI_AGENT: bool = True
    ENABLE_EXPORT_FEATURES: bool = True
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("REDIS_URL", pre=True)
    def assemble_redis_url(cls, v, values):
        if v:
            return v
        redis_host = values.get("REDIS_HOST", "localhost")
        redis_port = values.get("REDIS_PORT", 6379)
        redis_db = values.get("REDIS_DB", 0)
        redis_password = values.get("REDIS_PASSWORD")
        
        if redis_password:
            return f"redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db}"
        return f"redis://{redis_host}:{redis_port}/{redis_db}"
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == Environment.DEVELOPMENT
    
    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == Environment.TESTING
    
    @property
    def is_staging(self) -> bool:
        return self.ENVIRONMENT == Environment.STAGING
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == Environment.PRODUCTION
    
    @property
    def cors_origins_for_environment(self) -> List[str]:
        """Get CORS origins based on environment"""
        if self.is_production:
            # In production, use specific domains
            return [
                "https://yourdomain.com",
                "https://www.yourdomain.com",
                "https://app.yourdomain.com"
            ]
        elif self.is_staging:
            return [
                "https://staging.yourdomain.com",
                "https://staging-admin.yourdomain.com"
            ]
        else:
            # Development - allow local origins
            return self.CORS_ORIGINS
    
    def get_database_config(self) -> dict:
        """Get database configuration based on environment"""
        config = {
            "url": self.DATABASE_URL,
            "pool_size": self.DATABASE_POOL_SIZE,
            "max_overflow": self.DATABASE_MAX_OVERFLOW,
            "pool_timeout": self.DATABASE_POOL_TIMEOUT,
        }
        
        if self.is_testing:
            config["echo"] = False
        elif self.is_development:
            config["echo"] = True
        
        return config


# Create settings instance
settings = EnhancedSettings()


def get_settings_for_env() -> EnhancedSettings:
    """Get settings for current environment"""
    return settings


def validate_production_settings() -> List[str]:
    """Validate production settings and return list of issues"""
    issues = []
    
    if not settings.is_production:
        return issues
    
    # Check for production-specific requirements
    if settings.SECRET_KEY == "change-this-in-production":
        issues.append("SECRET_KEY must be changed in production")
    
    if len(settings.CORS_ORIGINS) == 1 and settings.CORS_ORIGINS[0] == "*":
        issues.append("CORS origins must be specific in production")
    
    if not settings.DATABASE_URL.startswith("postgresql://"):
        issues.append("PostgreSQL is recommended for production")
    
    if not settings.SENTRY_DSN:
        issues.append("SENTRY_DSN should be configured for production error tracking")
    
    if not settings.REDIS_URL:
        issues.append("Redis should be configured for production caching")
    
    return issues
