"""
Configuration management for Televoica.

This module provides configuration loading and management for both
standalone and Telegram bot modes.
"""

from televoica.config.settings import Settings, load_config

__all__ = ["Settings", "load_config"]

