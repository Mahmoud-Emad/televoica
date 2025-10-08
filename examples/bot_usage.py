"""
Example: Running the Telegram bot programmatically.

This example demonstrates how to run the Telegram bot from Python code
instead of using the CLI.
"""

import logging
from televoica.core.engine import SpeechToTextEngine
from televoica.core.providers import WhisperProvider
from televoica.bot.telegram_bot import TelegramSTTBot
from televoica.config.settings import Settings, STTConfig, TelegramConfig


def run_bot_basic():
    """Run bot with basic configuration."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create settings
    settings = Settings(
        telegram_bot=True,
        stt=STTConfig(
            provider="whisper",
            whisper_model="base",
            whisper_device="cpu",
        ),
        telegram=TelegramConfig(
            enabled=True,
            bot_token="YOUR_BOT_TOKEN_HERE",  # Replace with your bot token
            allowed_users=[],  # Empty list = allow all users
            max_file_size_mb=20,
        ),
    )
    
    # Create STT engine
    provider = WhisperProvider({
        "model": settings.stt.whisper_model,
        "device": settings.stt.whisper_device,
    })
    engine = SpeechToTextEngine(provider=provider)
    
    # Create and run bot
    bot = TelegramSTTBot(settings=settings, engine=engine)
    
    try:
        print("Starting Telegram bot...")
        bot.run()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
        bot.stop()


def run_bot_with_restrictions():
    """Run bot with user restrictions."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create settings with user restrictions
    settings = Settings(
        telegram_bot=True,
        stt=STTConfig(
            provider="whisper",
            whisper_model="medium",  # Use larger model
            whisper_device="cpu",
            whisper_language="en",  # Specify language
        ),
        telegram=TelegramConfig(
            enabled=True,
            bot_token="YOUR_BOT_TOKEN_HERE",  # Replace with your bot token
            allowed_users=[123456789, 987654321],  # Only allow specific users
            max_file_size_mb=50,  # Allow larger files
        ),
    )
    
    # Create STT engine
    provider = WhisperProvider({
        "model": settings.stt.whisper_model,
        "device": settings.stt.whisper_device,
        "language": settings.stt.whisper_language,
    })
    engine = SpeechToTextEngine(provider=provider)
    
    # Create and run bot
    bot = TelegramSTTBot(settings=settings, engine=engine)
    
    try:
        print("Starting Telegram bot with user restrictions...")
        bot.run()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
        bot.stop()


if __name__ == "__main__":
    print("Televoica Robot - Telegram Bot Examples")
    print("=" * 50)
    print()
    print("Make sure to:")
    print("1. Replace 'YOUR_BOT_TOKEN_HERE' with your actual Telegram bot token")
    print("2. Get a bot token from @BotFather on Telegram")
    print()
    
    # Run the basic example
    run_bot_basic()
    
    # Or run with restrictions
    # run_bot_with_restrictions()

