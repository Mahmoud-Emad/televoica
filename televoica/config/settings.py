"""
Settings and configuration management.

This module handles loading configuration from environment variables,
config files, and provides default settings.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, Literal
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class STTConfig:
    """Configuration for speech-to-text provider."""
    
    provider: Literal["whisper", "google_cloud"] = "whisper"
    
    # Whisper-specific settings
    whisper_model: str = "base"
    whisper_device: str = "cpu"
    whisper_language: Optional[str] = None
    
    # Google Cloud-specific settings
    google_credentials_path: Optional[str] = None
    google_language_code: str = "en-US"


@dataclass
class TelegramConfig:
    """Configuration for Telegram bot."""
    
    enabled: bool = False
    bot_token: Optional[str] = None
    allowed_users: list[int] = field(default_factory=list)
    max_file_size_mb: int = 20


@dataclass
class Settings:
    """Main application settings."""
    
    # Mode configuration
    telegram_bot: bool = False
    
    # STT configuration
    stt: STTConfig = field(default_factory=STTConfig)
    
    # Telegram configuration
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    
    # Logging
    log_level: str = "INFO"
    
    # Storage
    temp_dir: Path = field(default_factory=lambda: Path("/tmp/televoica"))

    def __post_init__(self):
        """Validate and process settings after initialization."""
        # Ensure temp directory exists
        self.temp_dir = Path(self.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # If telegram_bot mode is enabled, ensure telegram is also enabled
        if self.telegram_bot:
            self.telegram.enabled = True
            
            # Validate bot token
            if not self.telegram.bot_token:
                raise ValueError(
                    "Telegram bot token is required when telegram_bot=True. "
                    "Set TELEGRAM_BOT_TOKEN environment variable."
                )


def load_config(
    config_file: Optional[Path] = None,
    env_prefix: str = "STT_"
) -> Settings:
    """
    Load configuration from environment variables and optional config file.

    Args:
        config_file: Optional path to configuration file (YAML or JSON)
        env_prefix: Prefix for environment variables (default: "STT_")

    Returns:
        Settings object with loaded configuration

    Environment variables:
        STT_TELEGRAM_BOT: Enable Telegram bot mode (true/false)
        STT_LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR)
        STT_PROVIDER: STT provider to use (whisper, google_cloud)
        STT_WHISPER_MODEL: Whisper model size (tiny, base, small, medium, large)
        STT_WHISPER_DEVICE: Device to run Whisper on (cpu, cuda)
        STT_WHISPER_LANGUAGE: Language code for Whisper
        TELEGRAM_BOT_TOKEN: Telegram bot token
        TELEGRAM_ALLOWED_USERS: Comma-separated list of allowed user IDs
    """
    config_dict: Dict[str, Any] = {}
    
    # Load from config file if provided
    if config_file and config_file.exists():
        logger.info(f"Loading configuration from {config_file}")
        config_dict = _load_config_file(config_file)
    
    # Load from environment variables (overrides config file)
    env_config = _load_from_env(env_prefix)
    config_dict.update(env_config)
    
    # Build Settings object
    settings = Settings(
        telegram_bot=config_dict.get("telegram_bot", False),
        log_level=config_dict.get("log_level", "INFO"),
        temp_dir=Path(config_dict.get("temp_dir", "/tmp/televoica")),
        stt=STTConfig(
            provider=config_dict.get("stt_provider", "whisper"),
            whisper_model=config_dict.get("whisper_model", "base"),
            whisper_device=config_dict.get("whisper_device", "cpu"),
            whisper_language=config_dict.get("whisper_language"),
            google_credentials_path=config_dict.get("google_credentials_path"),
            google_language_code=config_dict.get("google_language_code", "en-US"),
        ),
        telegram=TelegramConfig(
            enabled=config_dict.get("telegram_bot", False),
            bot_token=config_dict.get("telegram_bot_token"),
            allowed_users=config_dict.get("telegram_allowed_users", []),
            max_file_size_mb=config_dict.get("telegram_max_file_size_mb", 20),
        ),
    )
    
    logger.info(f"Configuration loaded: telegram_bot={settings.telegram_bot}, provider={settings.stt.provider}")
    return settings


def _load_config_file(config_file: Path) -> Dict[str, Any]:
    """Load configuration from YAML or JSON file."""
    import json
    
    suffix = config_file.suffix.lower()
    
    if suffix == ".json":
        with open(config_file) as f:
            return json.load(f)
    elif suffix in [".yaml", ".yml"]:
        try:
            import yaml
            with open(config_file) as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            raise ImportError(
                "PyYAML is not installed. Install it with: pip install pyyaml"
            )
    else:
        raise ValueError(f"Unsupported config file format: {suffix}")


def _load_from_env(prefix: str = "STT_") -> Dict[str, Any]:
    """Load configuration from environment variables."""
    config = {}
    
    # Telegram bot mode
    if os.getenv(f"{prefix}TELEGRAM_BOT"):
        config["telegram_bot"] = os.getenv(f"{prefix}TELEGRAM_BOT", "").lower() in ["true", "1", "yes"]
    
    # Logging
    if os.getenv(f"{prefix}LOG_LEVEL"):
        config["log_level"] = os.getenv(f"{prefix}LOG_LEVEL", "INFO")
    
    # STT provider
    if os.getenv(f"{prefix}PROVIDER"):
        config["stt_provider"] = os.getenv(f"{prefix}PROVIDER", "whisper")
    
    # Whisper settings
    if os.getenv(f"{prefix}WHISPER_MODEL"):
        config["whisper_model"] = os.getenv(f"{prefix}WHISPER_MODEL", "base")
    if os.getenv(f"{prefix}WHISPER_DEVICE"):
        config["whisper_device"] = os.getenv(f"{prefix}WHISPER_DEVICE", "cpu")
    if os.getenv(f"{prefix}WHISPER_LANGUAGE"):
        config["whisper_language"] = os.getenv(f"{prefix}WHISPER_LANGUAGE")
    
    # Google Cloud settings
    if os.getenv(f"{prefix}GOOGLE_CREDENTIALS_PATH"):
        config["google_credentials_path"] = os.getenv(f"{prefix}GOOGLE_CREDENTIALS_PATH")
    if os.getenv(f"{prefix}GOOGLE_LANGUAGE_CODE"):
        config["google_language_code"] = os.getenv(f"{prefix}GOOGLE_LANGUAGE_CODE", "en-US")
    
    # Telegram settings
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        config["telegram_bot_token"] = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if os.getenv("TELEGRAM_ALLOWED_USERS"):
        users_str = os.getenv("TELEGRAM_ALLOWED_USERS", "")
        config["telegram_allowed_users"] = [
            int(uid.strip()) for uid in users_str.split(",") if uid.strip()
        ]
    
    if os.getenv("TELEGRAM_MAX_FILE_SIZE_MB"):
        config["telegram_max_file_size_mb"] = int(os.getenv("TELEGRAM_MAX_FILE_SIZE_MB", "20"))
    
    # Temp directory
    if os.getenv(f"{prefix}TEMP_DIR"):
        config["temp_dir"] = os.getenv(f"{prefix}TEMP_DIR", "/tmp/televoica")
    
    return config

