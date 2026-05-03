"""
Enhanced Configuration Manager with Validation
"""
from pydantic_settings import BaseSettings
from pydantic import Field, validator, SecretStr
from typing import List, Optional
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Application
    app_name: str = Field(default="AUREXIS AI", env="APP_NAME")
    app_version: str = Field(default="2.0.0", env="APP_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Security
    jwt_secret_key: SecretStr = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_days: int = Field(default=7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    data_encryption_key: Optional[SecretStr] = Field(None, env="DATA_ENCRYPTION_KEY")
    
    # Database
    database_url: str = Field(default="sqlite+aiosqlite:///./aurexis.db", env="DATABASE_URL")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    redis_enabled: bool = Field(default=False, env="REDIS_ENABLED")
    cache_ttl: int = Field(default=300, env="CACHE_TTL")
    
    # AI / Ollama
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="deepseek-v3.1:671b-cloud", env="OLLAMA_MODEL")
    ollama_enabled: bool = Field(default=False, env="OLLAMA_ENABLED")
    
    # Email
    smtp_host: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_user: Optional[str] = Field(None, env="SMTP_USER")
    smtp_password: Optional[SecretStr] = Field(None, env="SMTP_PASSWORD")
    smtp_from: str = Field(default="noreply@aurexis.ai", env="SMTP_FROM")
    email_enabled: bool = Field(default=False, env="EMAIL_ENABLED")
    
    # SMS
    twilio_account_sid: Optional[str] = Field(None, env="TWILIO_ACCOUNT_SID")
    twilio_auth_token: Optional[SecretStr] = Field(None, env="TWILIO_AUTH_TOKEN")
    twilio_phone_number: Optional[str] = Field(None, env="TWILIO_PHONE_NUMBER")
    sms_enabled: bool = Field(default=False, env="SMS_ENABLED")
    
    # Monitoring
    sentry_dsn: Optional[str] = Field(None, env="SENTRY_DSN")
    sentry_enabled: bool = Field(default=False, env="SENTRY_ENABLED")
    prometheus_enabled: bool = Field(default=False, env="PROMETHEUS_ENABLED")
    prometheus_port: int = Field(default=9090, env="PROMETHEUS_PORT")
    
    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    rate_limit_per_hour: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    
    # CORS
    cors_origins: str = Field(default="http://localhost:5173,http://localhost:3000", env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    
    # File Storage
    upload_dir: str = Field(default="./uploads", env="UPLOAD_DIR")
    max_upload_size: int = Field(default=10485760, env="MAX_UPLOAD_SIZE")  # 10MB
    allowed_extensions: str = Field(default=".pdf,.csv,.xlsx,.json", env="ALLOWED_EXTENSIONS")
    
    # Backup
    backup_enabled: bool = Field(default=True, env="BACKUP_ENABLED")
    backup_dir: str = Field(default="./backups", env="BACKUP_DIR")
    backup_retention_days: int = Field(default=30, env="BACKUP_RETENTION_DAYS")
    auto_backup_interval_hours: int = Field(default=24, env="AUTO_BACKUP_INTERVAL_HOURS")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="./logs/aurexis.log", env="LOG_FILE")
    log_max_size: int = Field(default=10485760, env="LOG_MAX_SIZE")
    log_backup_count: int = Field(default=5, env="LOG_BACKUP_COUNT")
    
    # Feature Flags
    feature_2fa_enabled: bool = Field(default=True, env="FEATURE_2FA_ENABLED")
    feature_biometric_enabled: bool = Field(default=False, env="FEATURE_BIOMETRIC_ENABLED")
    feature_portfolio_optimizer: bool = Field(default=True, env="FEATURE_PORTFOLIO_OPTIMIZER")
    feature_budget_planner: bool = Field(default=True, env="FEATURE_BUDGET_PLANNER")
    feature_advanced_analytics: bool = Field(default=True, env="FEATURE_ADVANCED_ANALYTICS")
    feature_pdf_reports: bool = Field(default=True, env="FEATURE_PDF_REPORTS")
    feature_global_search: bool = Field(default=True, env="FEATURE_GLOBAL_SEARCH")
    
    @validator("environment")
    def validate_environment(cls, v):
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"Log level must be one of {allowed}")
        return v.upper()
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Parse allowed extensions into list"""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment == "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Validate settings on import
try:
    settings = get_settings()
    
    # Warn about missing critical settings in production
    if settings.is_production:
        if settings.jwt_secret_key.get_secret_value() == "your-secret-key-here-change-in-production":
            raise ValueError("JWT_SECRET_KEY must be changed in production!")
        
        if not settings.data_encryption_key:
            print("⚠️  WARNING: DATA_ENCRYPTION_KEY not set - sensitive data will not be encrypted")
        
        if settings.debug:
            print("⚠️  WARNING: DEBUG mode is enabled in production")
    
    print(f"✅ Configuration loaded successfully ({settings.environment} mode)")
    
except Exception as e:
    print(f"❌ Configuration error: {e}")
    raise
