# Televoica

[![CI - Tests and Linting](https://github.com/Mahmoud-Emad/televoica/actions/workflows/ci.yml/badge.svg)](https://github.com/Mahmoud-Emad/televoica/actions/workflows/ci.yml)
[![Deploy Bot with Docker](https://github.com/Mahmoud-Emad/televoica/actions/workflows/deploy-docker.yml/badge.svg)](https://github.com/Mahmoud-Emad/televoica/actions/workflows/deploy-docker.yml)
[![Bot Health Check](https://github.com/Mahmoud-Emad/televoica/actions/workflows/health-check.yml/badge.svg)](https://github.com/Mahmoud-Emad/televoica/actions/workflows/health-check.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A Telegram bot that transcribes voice messages using OpenAI Whisper.**

Send a voice message → Get text back. Simple as that.

## Features

- **Voice to Text**: Transcribe voice messages and audio files
- **Telegram Bot**: Easy to use via Telegram
- **Fast & Accurate**: Powered by OpenAI Whisper
- **Docker Ready**: One-command deployment
- **Auto Monitoring**: Health checks every 30 minutes
- **Easy Setup**: Just add your bot token

## Quick Start

### 1. Get a Bot Token

1. Open [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow the instructions
3. Copy your bot token

### 2. Run the Bot

**Option A: Docker (Recommended)**

```bash
# Clone the repo
git clone https://github.com/Mahmoud-Emad/televoica.git
cd televoica

# Create .env file
cp .env.example .env
# Edit .env and add your TELEGRAM_BOT_TOKEN

# Start the bot
docker compose up -d

# Check logs
docker compose logs -f
```

**Option B: Local Installation**

```bash
# Clone the repo
git clone https://github.com/Mahmoud-Emad/televoica.git
cd televoica

# Install FFmpeg (required)
brew install ffmpeg  # macOS
# or: sudo apt install ffmpeg  # Ubuntu

# Install dependencies
poetry install

# Create .env file
cp .env.example .env
# Edit .env and add your TELEGRAM_BOT_TOKEN

# Run the bot
poetry run python examples/bot_usage.py
```

### 3. Test It

1. Find your bot on Telegram
2. Send `/start`
3. Send a voice message
4. Get your transcription!

## Configuration

All configuration is done via the `.env` file:

```bash
# Required
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Optional - Whisper Settings
STT_WHISPER_MODEL=base          # tiny, base, small, medium, large
STT_WHISPER_DEVICE=cpu          # cpu or cuda
STT_WHISPER_LANGUAGE=           # Leave empty for auto-detect

# Optional - Bot Settings
TELEGRAM_MAX_FILE_SIZE_MB=20    # Max audio file size
TELEGRAM_ALLOWED_USERS=         # Comma-separated user IDs (empty = all users)
```

**Model Comparison:**

| Model  | Speed    | Accuracy | RAM   | Best For              |
|--------|----------|----------|-------|-----------------------|
| tiny   | Fastest  | Low      | ~1GB  | Testing               |
| base   | Fast     | Good     | ~1GB  | **Recommended**       |
| small  | Medium   | Better   | ~2GB  | Better accuracy       |
| medium | Slow     | High     | ~5GB  | High accuracy needed  |
| large  | Slowest  | Highest  | ~10GB | Maximum accuracy      |

## Deployment

### GitHub Actions (Automated)

1. Fork this repository
2. Add `TELEGRAM_BOT_TOKEN` to GitHub Secrets:
   - Go to **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: Your bot token
3. Go to **Actions** tab → **Deploy Bot with Docker** → **Run workflow**

The bot will be automatically deployed and monitored!

## Development

```bash
# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=televoica

# Format code
poetry run black .

# Lint code
poetry run ruff check .
```

## License

MIT License - see the [LICENSE](LICENSE) file for details.
