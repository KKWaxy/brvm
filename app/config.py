"""
Application configuration and environment settings.
This file uses pydantic-settings for environment parsing and exposes a
single `settings` instance for the whole application.
"""

from typing import List, Optional
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings.

    Notes:
    - Keep safe defaults for development, but fail-fast in production for missing secrets.
    - CORS origins are provided as a comma-separated list in the CORS_ORIGINS env var.
    """

    app_name: str = "BRVM SGI API"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    server_host: str = "127.0.0.1"
    server_port: int = 8000

    # JWT Configuration: use SecretStr to avoid accidental leakage in logs
    jwt_secret_key: SecretStr = SecretStr("change-me-dev-secret")
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # CORS configuration. Prefer explicit origins in production.
    cors_origins: List[str] = []  # set via CORS_ORIGINS="https://a.com,https://b.com"
    allow_credentials: bool = False

    # Trusted hosts for TrustedHostMiddleware
    trusted_hosts: List[str] = ["127.0.0.1", "localhost"]

    # Enforce HTTPS redirect in production behind a proper reverse proxy
    enforce_https: bool = False

    # Optional Redis URL for rate limiter backend (redis://...)
    rate_limit_redis_url: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Instantiate singleton settings
settings = Settings()

# Startup validations (fail-fast if insecure settings are used in production)
try:
    # If not in debug and secret is default-ish, refuse to start
    secret_value = settings.jwt_secret_key.get_secret_value() if settings.jwt_secret_key else ""
    if not settings.debug and (not secret_value or secret_value in ("change-me-dev-secret", "your-super-secret-key-change-in-production", "")):
        logger.critical("JWT secret key is not set or is insecure. Set JWT_SECRET_KEY env var before starting in production.")
        raise RuntimeError("JWT secret key must be configured in production via env var JWT_SECRET_KEY")
except Exception:
    # Re-raise so the process fails to start loudly
    raise
