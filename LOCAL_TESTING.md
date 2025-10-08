# Local Testing Guide

Quick guide to test the bot locally before deploying to GitHub Actions.

## Prerequisites

- Python 3.10+
- Poetry installed
- FFmpeg installed
- Bot token from [@BotFather](https://t.me/BotFather)

## Quick Start

### 1. Install Dependencies

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

### 2. Set Environment Variables

```bash
# Set your bot token
export TELEGRAM_BOT_TOKEN="7606854595:AAGL74_XD5LiffVY7bu5aCUc6QcY2tz1QXc"

# Enable bot mode
export STT_TELEGRAM_BOT=true

# Optional: Configure STT settings
export STT_PROVIDER=whisper
export STT_WHISPER_MODEL=base
export STT_WHISPER_DEVICE=cpu
export STT_LOG_LEVEL=INFO
```

### 3. Run the Bot

```bash
# Run with Poetry
poetry run televoica bot

# Or activate virtual environment first
poetry shell
televoica bot
```

### 4. Test the Bot

1. Open Telegram
2. Search for your bot
3. Send `/start`
4. Send a voice message
5. Receive transcription!

## Testing Individual Components

### Test Configuration Loading

```bash
poetry run python -c "
from televoica.config.settings import load_config

settings = load_config()
print(f'Bot token configured: {bool(settings.telegram.bot_token)}')
print(f'Provider: {settings.stt.provider}')
print(f'Model: {settings.stt.whisper_model}')
print(f'Device: {settings.stt.whisper_device}')
"
```

### Test STT Engine

```bash
poetry run python -c "
from televoica.core.engine import SpeechToTextEngine
from televoica.core.providers import WhisperProvider

provider = WhisperProvider({'model': 'base', 'device': 'cpu'})
engine = SpeechToTextEngine(provider=provider)
print('STT engine initialized successfully!')
"
```

### Test Bot Initialization

```bash
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
export STT_TELEGRAM_BOT=true

poetry run python -c "
from televoica.config.settings import load_config
from televoica.core.engine import SpeechToTextEngine
from televoica.core.providers import WhisperProvider
from televoica.bot.telegram_bot import TelegramSTTBot

settings = load_config()
provider = WhisperProvider({
    'model': settings.stt.whisper_model,
    'device': settings.stt.whisper_device,
})
engine = SpeechToTextEngine(provider=provider)
bot = TelegramSTTBot(settings=settings, engine=engine)
print('Bot initialized successfully!')
"
```

### Run Health Check

```bash
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
python scripts/health_check.py
```

## Docker Testing

### Build and Run with Docker

```bash
# Build image
docker build -t televoica-bot .

# Run container
docker run -d \
  --name televoica-bot \
  -e TELEGRAM_BOT_TOKEN="YOUR_TOKEN" \
  -e STT_TELEGRAM_BOT=true \
  -e STT_PROVIDER=whisper \
  -e STT_WHISPER_MODEL=base \
  -e STT_WHISPER_DEVICE=cpu \
  televoica-bot

# View logs
docker logs -f televoica-bot

# Stop container
docker stop televoica-bot
docker rm televoica-bot
```

### Using Docker Compose

```bash
# Create .env file
cat > .env << EOF
TELEGRAM_BOT_TOKEN=YOUR_TOKEN
STT_PROVIDER=whisper
STT_WHISPER_MODEL=base
STT_WHISPER_DEVICE=cpu
EOF

# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## Troubleshooting

### Bot Token Not Found

```bash
# Check if token is set
echo $TELEGRAM_BOT_TOKEN

# Set it if missing
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
```

### FFmpeg Not Found

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

### Import Errors

```bash
# Reinstall dependencies
poetry install --no-cache

# Or clear cache and reinstall
rm -rf .venv
poetry install
```

### Bot Not Responding

```bash
# Check if bot is running
ps aux | grep televoica

# Check logs
# (if running in background, check the terminal output)

# Test bot token with health check
python scripts/health_check.py
```

### High CPU/Memory Usage

```bash
# Use smaller model
export STT_WHISPER_MODEL=tiny

# Or use base model (default)
export STT_WHISPER_MODEL=base
```

## Model Comparison

| Model | Size | Speed | Accuracy | RAM Usage |
|-------|------|-------|----------|-----------|
| tiny | 39M | Fastest | Low | ~1GB |
| base | 74M | Fast | Good | ~1GB |
| small | 244M | Medium | Better | ~2GB |
| medium | 769M | Slow | High | ~5GB |
| large | 1550M | Slowest | Highest | ~10GB |

## Environment Variables Reference

```bash
# Required
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Bot Mode
STT_TELEGRAM_BOT=true                    # Enable bot mode

# STT Provider
STT_PROVIDER=whisper                     # whisper or google_cloud

# Whisper Settings
STT_WHISPER_MODEL=base                   # tiny, base, small, medium, large
STT_WHISPER_DEVICE=cpu                   # cpu or cuda
STT_WHISPER_LANGUAGE=                    # en, ar, es, etc. (empty = auto)

# Telegram Settings
TELEGRAM_ALLOWED_USERS=                  # Comma-separated user IDs (empty = all)
TELEGRAM_MAX_FILE_SIZE_MB=20             # Max file size in MB

# Logging
STT_LOG_LEVEL=INFO                       # DEBUG, INFO, WARNING, ERROR

# Storage
STT_TEMP_DIR=/tmp/televoica              # Temporary files directory
```

## Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=televoica

# Run specific test file
poetry run pytest tests/test_config.py

# Run with verbose output
poetry run pytest -v
```

## Code Quality Checks

```bash
# Format code
poetry run black .

# Lint code
poetry run ruff check .

# Type checking
poetry run mypy televoica
```

## Useful Commands

```bash
# Show installed packages
poetry show

# Update dependencies
poetry update

# Add new dependency
poetry add package-name

# Remove dependency
poetry remove package-name

# Show virtual environment info
poetry env info

# Activate virtual environment
poetry shell

# Deactivate virtual environment
exit
```

## Next Steps

Once local testing is successful:

1. **Commit changes:**
   ```bash
   git add .
   git commit -m "Test bot locally - working"
   git push
   ```

2. **Deploy with GitHub Actions:**
   - Go to Actions tab
   - Run "Deploy Bot (Simple)" workflow
   - If successful, run "Deploy Bot with Docker"

3. **Monitor:**
   - Health checks run automatically every 30 minutes
   - Check Actions tab for status

## Support

- [GitHub Actions Setup Guide](docs/GITHUB_ACTIONS_SETUP.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Troubleshooting](.github/TROUBLESHOOTING.md)
- [Quick Reference](.github/QUICK_REFERENCE.md)

