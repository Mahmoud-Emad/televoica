#!/usr/bin/env python3
"""
Health check script for Televoica Telegram Bot.

This script checks if the bot is running and responsive by:
1. Checking if the bot can connect to Telegram API
2. Sending a test message to verify bot is processing commands
3. Optionally checking system resources

Usage:
    python scripts/health_check.py
    
Environment variables:
    TELEGRAM_BOT_TOKEN: Bot token for authentication
    HEALTH_CHECK_CHAT_ID: (Optional) Chat ID to send test messages to
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BotHealthChecker:
    """Health checker for Telegram bot."""
    
    def __init__(self, bot_token: str, chat_id: Optional[str] = None):
        """
        Initialize health checker.
        
        Args:
            bot_token: Telegram bot token
            chat_id: Optional chat ID for sending test messages
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = None
        
    async def check_bot_connection(self) -> bool:
        """
        Check if bot can connect to Telegram API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            from telegram import Bot
            
            self.bot = Bot(token=self.bot_token)
            bot_info = await self.bot.get_me()

            logger.info(f"Bot connection successful")
            logger.info(f"   Bot username: @{bot_info.username}")
            logger.info(f"   Bot name: {bot_info.first_name}")
            logger.info(f"   Bot ID: {bot_info.id}")

            return True

        except Exception as e:
            logger.error(f"Bot connection failed: {e}")
            return False
    
    async def check_bot_updates(self) -> bool:
        """
        Check if bot can receive updates.
        
        Returns:
            True if bot can receive updates, False otherwise
        """
        try:
            if not self.bot:
                logger.error("Bot not initialized")
                return False
            
            # Get recent updates
            updates = await self.bot.get_updates(limit=1)
            logger.info(f"Bot can receive updates (last update count: {len(updates)})")

            return True

        except Exception as e:
            logger.error(f"Failed to get updates: {e}")
            return False
    
    async def send_test_message(self) -> bool:
        """
        Send a test message to verify bot is working.
        
        Returns:
            True if message sent successfully, False otherwise
        """
        if not self.chat_id:
            logger.warning("No chat ID provided, skipping test message")
            return True

        try:
            if not self.bot:
                logger.error("Bot not initialized")
                return False

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"Health check at {timestamp}\n\nBot is operational"

            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message
            )

            logger.info(f"Test message sent successfully to chat {self.chat_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to send test message: {e}")
            return False
    
    async def check_system_resources(self) -> bool:
        """
        Check system resources (CPU, memory, disk).
        
        Returns:
            True if resources are within acceptable limits
        """
        try:
            import psutil
            
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            logger.info(f"   CPU usage: {cpu_percent}%")
            
            # Check memory usage
            memory = psutil.virtual_memory()
            logger.info(f"   Memory usage: {memory.percent}% ({memory.used / 1024**3:.2f}GB / {memory.total / 1024**3:.2f}GB)")
            
            # Check disk usage
            disk = psutil.disk_usage('/')
            logger.info(f"   Disk usage: {disk.percent}% ({disk.used / 1024**3:.2f}GB / {disk.total / 1024**3:.2f}GB)")
            
            # Warning thresholds
            if cpu_percent > 90:
                logger.warning(f"High CPU usage: {cpu_percent}%")
            if memory.percent > 90:
                logger.warning(f"High memory usage: {memory.percent}%")
            if disk.percent > 90:
                logger.warning(f"High disk usage: {disk.percent}%")

            return True

        except ImportError:
            logger.warning("psutil not installed, skipping system resource check")
            return True
        except Exception as e:
            logger.error(f"Failed to check system resources: {e}")
            return False
    
    async def run_health_check(self) -> bool:
        """
        Run complete health check.
        
        Returns:
            True if all checks pass, False otherwise
        """
        logger.info("=" * 60)
        logger.info("Starting Televoica Bot Health Check")
        logger.info("=" * 60)
        
        checks = []
        
        # Check bot connection
        logger.info("\n1. Checking bot connection...")
        checks.append(await self.check_bot_connection())
        
        # Check bot updates
        logger.info("\n2. Checking bot updates...")
        checks.append(await self.check_bot_updates())
        
        # Send test message
        logger.info("\n3. Sending test message...")
        checks.append(await self.send_test_message())
        
        # Check system resources
        logger.info("\n4. Checking system resources...")
        checks.append(await self.check_system_resources())
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("Health Check Summary")
        logger.info("=" * 60)
        
        passed = sum(checks)
        total = len(checks)
        
        logger.info(f"Checks passed: {passed}/{total}")

        if all(checks):
            logger.info("All health checks passed!")
            logger.info("=" * 60)
            return True
        else:
            logger.error("Some health checks failed!")
            logger.info("=" * 60)
            return False
    
    async def close(self):
        """Close bot connection."""
        if self.bot:
            # No explicit close needed for python-telegram-bot v20+
            pass


async def main():
    """Main entry point."""
    # Get bot token from environment
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        sys.exit(1)
    
    # Get optional chat ID for test messages
    chat_id = os.getenv("HEALTH_CHECK_CHAT_ID")
    
    # Create health checker
    checker = BotHealthChecker(bot_token=bot_token, chat_id=chat_id)
    
    try:
        # Run health check
        success = await checker.run_health_check()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"Health check failed with exception: {e}", exc_info=True)
        sys.exit(1)
        
    finally:
        await checker.close()


if __name__ == "__main__":
    asyncio.run(main())

