"""
EdgeRelay Core Configuration Management
MESSS Compliant - Modular, Efficient, Scalable, Secure, Stable
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    MESSS Compliant: Secure configuration management.
    """
    
    # Application Settings
    APP_NAME: str = Field(default="EdgeRelay Core API Service", description="Application name")
    ENVIRONMENT: str = Field(default="production", description="Environment (development/production)")
    DEBUG: bool = Field(default=False, description="Debug mode")
    VERSION: str = Field(default="1.0.0", description="Application version")
    
    # Server Settings
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    WORKERS: int = Field(default=1, description="Number of workers")
    
    # Security Settings
    SECRET_KEY: str = Field(default="EdgeRelay@JWT#Secret#2025!", description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="JWT token expiry in minutes")
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="JWT refresh token expiry in days")
    
    # Database Settings - Admin Database
    ADMIN_DB_HOST: str = Field(default="edgerelay-postgres", description="Admin database host")
    ADMIN_DB_PORT: int = Field(default=5432, description="Admin database port")
    ADMIN_DB_NAME: str = Field(default="admin_db", description="Admin database name")
    ADMIN_DB_USER: str = Field(default="edgerelay_user", description="Admin database user")
    ADMIN_DB_PASSWORD: str = Field(default="EdgeRelay@Secure#2025!", description="Admin database password")
    
    # Database Settings - Client Database
    CLIENT_DB_HOST: str = Field(default="edgerelay-postgres", description="Client database host")
    CLIENT_DB_PORT: int = Field(default=5432, description="Client database port")
    CLIENT_DB_NAME: str = Field(default="client_db", description="Client database name")
    CLIENT_DB_USER: str = Field(default="edgerelay_user", description="Client database user")
    CLIENT_DB_PASSWORD: str = Field(default="EdgeRelay@Secure#2025!", description="Client database password")
    
    # Redis Settings
    REDIS_HOST: str = Field(default="edgerelay-redis", description="Redis host")
    REDIS_PORT: int = Field(default=6379, description="Redis port")
    REDIS_PASSWORD: str = Field(default="EdgeRelay@Redis#2025!", description="Redis password")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    
    # MQTT Settings
    MQTT_BROKER_HOST: str = Field(default="edgerelay-mqtt", description="MQTT broker host")
    MQTT_BROKER_PORT: int = Field(default=1883, description="MQTT broker port")
    MQTT_BROKER_USERNAME: Optional[str] = Field(default=None, description="MQTT broker username")
    MQTT_BROKER_PASSWORD: Optional[str] = Field(default=None, description="MQTT broker password")
    
    # CORS Settings
    CORS_ORIGINS: List[str] = Field(
        default=["https://admin.navachar.com", "https://www.navachar.com"],
        description="Allowed CORS origins"
    )
    
    # Security Settings
    ALLOWED_HOSTS: List[str] = Field(
        default=["*"],
        description="Allowed hosts for trusted host middleware"
    )
    
    # Logging Settings
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(default="json", description="Log format (json/text)")
    
    # Timezone Settings
    TIMEZONE: str = Field(default="Asia/Kolkata", description="Application timezone")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get application settings singleton.
    MESSS Compliant: Efficient singleton pattern.
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# Database URL helpers
def get_admin_db_url() -> str:
    """Get admin database URL."""
    settings = get_settings()
    return (
        f"postgresql://{settings.ADMIN_DB_USER}:{settings.ADMIN_DB_PASSWORD}"
        f"@{settings.ADMIN_DB_HOST}:{settings.ADMIN_DB_PORT}/{settings.ADMIN_DB_NAME}"
    )


def get_client_db_url() -> str:
    """Get client database URL."""
    settings = get_settings()
    return (
        f"postgresql://{settings.CLIENT_DB_USER}:{settings.CLIENT_DB_PASSWORD}"
        f"@{settings.CLIENT_DB_HOST}:{settings.CLIENT_DB_PORT}/{settings.CLIENT_DB_NAME}"
    )


def get_redis_url() -> str:
    """Get Redis URL."""
    settings = get_settings()
    return f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
