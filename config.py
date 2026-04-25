"""Configuration management for MiroFish.

Handles loading and validation of environment variables and application settings.
"""

import os
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


@dataclass
class AppConfig:
    """Application configuration loaded from environment variables."""

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = False

    # API settings
    api_key: Optional[str] = None
    api_base_url: str = "https://api.openai.com/v1"
    model_name: str = "gpt-3.5-turbo"

    # Proxy settings
    proxy_url: Optional[str] = None
    request_timeout: int = 30

    # Rate limiting
    max_requests_per_minute: int = 60
    max_tokens_per_request: int = 4096

    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None

    # Feature flags
    enable_streaming: bool = True
    enable_cache: bool = False
    cache_ttl: int = 300  # seconds


def load_config() -> AppConfig:
    """Load configuration from environment variables.

    Returns:
        AppConfig: Populated configuration object.

    Raises:
        ValueError: If required environment variables are missing or invalid.
    """
    config = AppConfig(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=os.getenv("DEBUG", "false").lower() in ("true", "1", "yes"),
        api_key=os.getenv("API_KEY"),
        api_base_url=os.getenv("API_BASE_URL", "https://api.openai.com/v1"),
        model_name=os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
        proxy_url=os.getenv("PROXY_URL"),
        request_timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
        max_requests_per_minute=int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60")),
        max_tokens_per_request=int(os.getenv("MAX_TOKENS_PER_REQUEST", "4096")),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        log_file=os.getenv("LOG_FILE"),
        enable_streaming=os.getenv("ENABLE_STREAMING", "true").lower() in ("true", "1", "yes"),
        enable_cache=os.getenv("ENABLE_CACHE", "false").lower() in ("true", "1", "yes"),
        cache_ttl=int(os.getenv("CACHE_TTL", "300")),
    )

    _validate_config(config)
    return config


def _validate_config(config: AppConfig) -> None:
    """Validate the loaded configuration.

    Args:
        config: Configuration object to validate.

    Raises:
        ValueError: If any configuration value is invalid.
    """
    if not config.api_key:
        raise ValueError(
            "API_KEY environment variable is required but not set. "
            "Please copy .env.example to .env and fill in your API key."
        )

    if not (1 <= config.port <= 65535):
        raise ValueError(f"PORT must be between 1 and 65535, got {config.port}")

    if config.request_timeout <= 0:
        raise ValueError(f"REQUEST_TIMEOUT must be positive, got {config.request_timeout}")

    if config.max_tokens_per_request <= 0:
        raise ValueError(
            f"MAX_TOKENS_PER_REQUEST must be positive, got {config.max_tokens_per_request}"
        )

    valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if config.log_level not in valid_log_levels:
        raise ValueError(
            f"LOG_LEVEL must be one of {valid_log_levels}, got {config.log_level!r}"
        )


# Module-level singleton — lazily initialized
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Return the global application configuration (singleton).

    Returns:
        AppConfig: The application configuration.
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config
