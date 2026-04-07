"""
Application configuration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "SGI"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    server_host: str = "127.0.0.1"  # Default to localhost for security
    server_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
