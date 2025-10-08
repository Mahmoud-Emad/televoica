"""
Telegram bot implementation for speech-to-text conversion.

This module implements the Telegram bot that receives voice messages
and uses the SpeechToTextEngine to transcribe them.
"""

import logging
from pathlib import Path
from typing import Optional
import asyncio

from televoica.core.engine import SpeechToTextEngine
from televoica.config.settings import Settings

logger = logging.getLogger(__name__)


class TelegramSTTBot:
    """
    Telegram bot for speech-to-text conversion.
    
    This bot receives voice messages and audio files, transcribes them
    using the SpeechToTextEngine, and sends back the transcribed text.
    """

    def __init__(self, settings: Settings, engine: Optional[SpeechToTextEngine] = None):
        """
        Initialize the Telegram bot.

        Args:
            settings: Application settings
            engine: Optional SpeechToTextEngine instance. If None, creates a new one.
        """
        self.settings = settings
        self.engine = engine or SpeechToTextEngine()
        self.bot_token = settings.telegram.bot_token
        self.allowed_users = set(settings.telegram.allowed_users)
        self.max_file_size = settings.telegram.max_file_size_mb * 1024 * 1024  # Convert to bytes
        
        # Will be initialized in run()
        self.application = None
        
        logger.info("TelegramSTTBot initialized")

    def _is_user_allowed(self, user_id: int) -> bool:
        """
        Check if a user is allowed to use the bot.

        Args:
            user_id: Telegram user ID

        Returns:
            True if user is allowed (or if no restrictions are set)
        """
        if not self.allowed_users:
            return True  # No restrictions
        return user_id in self.allowed_users

    async def start_command(self, update, context):
        """Handle /start command."""
        try:
            from telegram import Update
            from telegram.ext import ContextTypes
        except ImportError:
            raise ImportError(
                "python-telegram-bot is not installed. "
                "Install it with: pip install python-telegram-bot"
            )
        
        user_id = update.effective_user.id
        
        if not self._is_user_allowed(user_id):
            await update.message.reply_text(
                "⛔ Sorry, you are not authorized to use this bot."
            )
            return
        
        welcome_message = (
            "👋 Welcome to Televoica Bot!\n\n"
            "Send me a voice message or audio file, and I'll transcribe it for you.\n\n"
            "Commands:\n"
            "/start - Show this message\n"
            "/help - Show help information\n"
            "/info - Show bot information"
        )
        
        await update.message.reply_text(welcome_message)

    async def help_command(self, update, context):
        """Handle /help command."""
        user_id = update.effective_user.id
        
        if not self._is_user_allowed(user_id):
            await update.message.reply_text(
                "⛔ Sorry, you are not authorized to use this bot."
            )
            return
        
        help_message = (
            "ℹ️ How to use this bot:\n\n"
            "1. Send a voice message (record using Telegram's voice recorder)\n"
            "2. Or send an audio file (MP3, OGG, WAV, etc.)\n"
            "3. Wait for the transcription\n\n"
            f"Maximum file size: {self.settings.telegram.max_file_size_mb} MB\n\n"
            "The bot uses advanced speech recognition to provide accurate transcriptions."
        )
        
        await update.message.reply_text(help_message)

    async def info_command(self, update, context):
        """Handle /info command."""
        user_id = update.effective_user.id
        
        if not self._is_user_allowed(user_id):
            await update.message.reply_text(
                "⛔ Sorry, you are not authorized to use this bot."
            )
            return
        
        provider_name = self.engine.provider.__class__.__name__
        info_message = (
            f"🤖 Bot Information:\n\n"
            f"STT Provider: {provider_name}\n"
            f"Max File Size: {self.settings.telegram.max_file_size_mb} MB\n"
            f"Version: 0.1.0"
        )
        
        await update.message.reply_text(info_message)

    async def handle_voice(self, update, context):
        """Handle voice messages."""
        user_id = update.effective_user.id
        
        if not self._is_user_allowed(user_id):
            await update.message.reply_text(
                "⛔ Sorry, you are not authorized to use this bot."
            )
            return
        
        voice = update.message.voice
        
        # Check file size
        if voice.file_size > self.max_file_size:
            await update.message.reply_text(
                f"⚠️ File too large. Maximum size is {self.settings.telegram.max_file_size_mb} MB."
            )
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text("🎙️ Processing your voice message...")
        
        try:
            # Download voice file
            file = await context.bot.get_file(voice.file_id)
            file_path = self.settings.temp_dir / f"{voice.file_id}.ogg"
            await file.download_to_drive(file_path)
            
            logger.info(f"Downloaded voice message from user {user_id}: {file_path}")
            
            # Transcribe
            text = self.engine.transcribe_file(file_path)
            
            # Clean up
            file_path.unlink(missing_ok=True)
            
            # Send result
            if text:
                await processing_msg.edit_text(f"📝 Transcription:\n\n{text}")
                logger.info(f"Transcription sent to user {user_id}")
            else:
                await processing_msg.edit_text("⚠️ No speech detected in the audio.")
        
        except Exception as e:
            logger.error(f"Error processing voice message: {e}", exc_info=True)
            await processing_msg.edit_text(
                f"❌ Error processing voice message: {str(e)}"
            )

    async def handle_audio(self, update, context):
        """Handle audio files."""
        user_id = update.effective_user.id
        
        if not self._is_user_allowed(user_id):
            await update.message.reply_text(
                "⛔ Sorry, you are not authorized to use this bot."
            )
            return
        
        audio = update.message.audio
        
        # Check file size
        if audio.file_size > self.max_file_size:
            await update.message.reply_text(
                f"⚠️ File too large. Maximum size is {self.settings.telegram.max_file_size_mb} MB."
            )
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text("🎵 Processing your audio file...")
        
        try:
            # Download audio file
            file = await context.bot.get_file(audio.file_id)
            
            # Determine file extension
            file_ext = Path(audio.file_name).suffix if audio.file_name else ".mp3"
            file_path = self.settings.temp_dir / f"{audio.file_id}{file_ext}"
            
            await file.download_to_drive(file_path)
            
            logger.info(f"Downloaded audio file from user {user_id}: {file_path}")
            
            # Transcribe
            text = self.engine.transcribe_file(file_path)
            
            # Clean up
            file_path.unlink(missing_ok=True)
            
            # Send result
            if text:
                await processing_msg.edit_text(f"📝 Transcription:\n\n{text}")
                logger.info(f"Transcription sent to user {user_id}")
            else:
                await processing_msg.edit_text("⚠️ No speech detected in the audio.")
        
        except Exception as e:
            logger.error(f"Error processing audio file: {e}", exc_info=True)
            await processing_msg.edit_text(
                f"❌ Error processing audio file: {str(e)}"
            )

    async def error_handler(self, update, context):
        """Handle errors."""
        logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)

    def run(self):
        """
        Start the Telegram bot.
        
        This method blocks until the bot is stopped.
        """
        try:
            from telegram.ext import Application, CommandHandler, MessageHandler, filters
        except ImportError:
            raise ImportError(
                "python-telegram-bot is not installed. "
                "Install it with: pip install python-telegram-bot"
            )
        
        logger.info("Starting Telegram bot...")
        
        # Create application
        self.application = Application.builder().token(self.bot_token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("info", self.info_command))
        self.application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        self.application.add_handler(MessageHandler(filters.AUDIO, self.handle_audio))
        
        # Add error handler
        self.application.add_error_handler(self.error_handler)
        
        # Start bot
        logger.info("Bot is running. Press Ctrl+C to stop.")
        self.application.run_polling(allowed_updates=["message"])

    def stop(self):
        """Stop the Telegram bot."""
        if self.application:
            logger.info("Stopping Telegram bot...")
            self.application.stop()

