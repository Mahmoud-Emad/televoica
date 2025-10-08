# Televoica Robot

A modular, high-accuracy speech-to-text library with optional Telegram bot integration. Built with Python and designed for flexibility and ease of use.

## Features

- **Dual Mode Operation**: Use as a standalone library or as a Telegram bot
- **Modular Architecture**: Core STT functionality separated from bot integration
- **Multiple STT Providers**: Support for OpenAI Whisper and Google Cloud Televoica
- **Flexible Configuration**: Environment variables, config files, or programmatic setup
- **Easy to Use**: Simple CLI and Python API
- **Production Ready**: Proper error handling, logging, and type hints
- **Automated Deployment**: GitHub Actions for CI/CD and health monitoring
- **Docker Support**: Containerized deployment for easy scaling

## Installation

### Prerequisites

**FFmpeg is required** for audio processing:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows (using Chocolatey)
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/Mahmoud-Emad/televoica.git
cd televoica

# Install dependencies
poetry install
```

### Using Docker

```bash
# Create .env file with your bot token
echo "TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE" > .env

# Start the bot
docker compose up -d

# View logs
docker compose logs -f
```

## Quick Start

### 1. Get a Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command and follow instructions
3. Copy the bot token provided

### 2. Run the Bot

**Using Docker (Easiest)**:

```bash
# Set your bot token
export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"

# Start with docker-compose
docker compose up -d
```

**Using Poetry**:

```bash
# Set your bot token
export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
export STT_TELEGRAM_BOT=true

# Run the bot
poetry run televoica bot
```

**Using Python directly**:

```bash
# Install dependencies
pip install -e .

# Run the bot
televoica bot
```

### 3. Test Your Bot

1. Open Telegram and search for your bot
2. Send `/start` command
3. Send a voice message or audio file
4. Receive the transcription!

## Deployment

### GitHub Actions (Automated)

This project includes GitHub Actions workflows for automated deployment and monitoring.

**Quick Setup**:

1. Fork/clone this repository
2. Add `TELEGRAM_BOT_TOKEN` to GitHub Secrets:
   - Go to Settings → Secrets and variables → Actions
   - Add new secret: `TELEGRAM_BOT_TOKEN`
3. Push to `main` branch or manually trigger workflow
4. Bot will be automatically deployed!

**Available Workflows**:

- **Deploy Bot with Docker**: Builds and deploys containerized bot
- **Deploy Bot Service**: Deploys as systemd service (requires self-hosted runner)
- **Bot Health Check**: Runs every 30 minutes to monitor bot health

📚 **[Complete GitHub Actions Setup Guide](docs/GITHUB_ACTIONS_SETUP.md)**

### Manual Deployment

See the **[Deployment Guide](docs/DEPLOYMENT.md)** for detailed instructions on:

- Docker deployment
- Systemd service setup
- Manual deployment
- Configuration options
- Monitoring and troubleshooting

## Configuration

### Environment Variables

```bash
# Required
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Optional
STT_TELEGRAM_BOT=true                    # Enable bot mode
STT_PROVIDER=whisper                     # STT provider (whisper, google_cloud)
STT_WHISPER_MODEL=base                   # Model size (tiny, base, small, medium, large)
STT_WHISPER_DEVICE=cpu                   # Device (cpu, cuda)
STT_WHISPER_LANGUAGE=                    # Language code or empty for auto-detect
TELEGRAM_ALLOWED_USERS=                  # Comma-separated user IDs
TELEGRAM_MAX_FILE_SIZE_MB=20             # Max file size in MB
STT_LOG_LEVEL=INFO                       # Log level
```

### Configuration File

Create `config.yaml`:

```yaml
telegram_bot: true
log_level: INFO

stt_provider: whisper
whisper_model: base
whisper_device: cpu

telegram_allowed_users: []  # Empty = allow all
telegram_max_file_size_mb: 20
```

Run with config file:

```bash
televoica bot --config config.yaml
```

## Usage Examples

### As a Telegram Bot

See [Quick Start](#quick-start) above.

### As a Python Library

```python
from televoica.core.engine import SpeechToTextEngine
from televoica.core.providers import WhisperProvider

# Create engine
provider = WhisperProvider({"model": "base", "device": "cpu"})
engine = SpeechToTextEngine(provider=provider)

# Transcribe file
text = engine.transcribe_file("audio.mp3")
print(text)

# Transcribe bytes
with open("audio.mp3", "rb") as f:
    audio_bytes = f.read()
text = engine.transcribe_bytes(audio_bytes, format="mp3")
print(text)
```

### CLI Usage

```bash
# Transcribe a file
televoica transcribe audio.mp3

# Transcribe with specific model
televoica transcribe audio.mp3 --whisper-model medium

# Save to file
televoica transcribe audio.mp3 -o transcription.txt

# Run bot
televoica bot

# Run bot with config
televoica bot --config config.yaml
```

## Health Monitoring

The project includes a health check script for monitoring:

```bash
# Run health check
export TELEGRAM_BOT_TOKEN="your_token"
python scripts/health_check.py

# With test message
export HEALTH_CHECK_CHAT_ID="your_chat_id"
python scripts/health_check.py
```

Health checks verify:

- ✅ Bot connection to Telegram API
- ✅ Bot can receive updates
- ✅ System resources (CPU, memory, disk)
- ✅ Optional: Send test message

## Project Structure

```
televoica/
├── .github/
│   └── workflows/          # GitHub Actions workflows
│       ├── deploy-docker.yml
│       ├── deploy-bot-service.yml
│       └── health-check.yml
├── docs/                   # Documentation
│   ├── DEPLOYMENT.md
│   └── GITHUB_ACTIONS_SETUP.md
├── scripts/                # Utility scripts
│   ├── health_check.py
│   └── README.md
├── televoica/              # Main package
│   ├── bot/               # Telegram bot integration
│   ├── cli/               # Command-line interface
│   ├── config/            # Configuration management
│   └── core/              # Core STT engine
├── examples/              # Usage examples
├── tests/                 # Test suite
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
└── pyproject.toml         # Project dependencies
```

## Documentation

- **[GitHub Actions Setup Guide](docs/GITHUB_ACTIONS_SETUP.md)** - Quick start for automated deployment
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Comprehensive deployment instructions
- **[Scripts README](scripts/README.md)** - Utility scripts documentation

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=televoica

# Run specific test
poetry run pytest tests/test_config.py
```

### Code Quality

```bash
# Format code
poetry run black .

# Lint code
poetry run ruff check .

# Type checking
poetry run mypy televoica
```

## Troubleshooting

### Bot not responding?

1. Check if bot is running:

   ```bash
   docker compose ps  # For Docker
   sudo systemctl status televoica-bot  # For systemd
   ```

2. Check logs:

   ```bash
   docker compose logs -f  # For Docker
   sudo journalctl -u televoica-bot -f  # For systemd
   ```

3. Run health check:

   ```bash
   python scripts/health_check.py
   ```

### High resource usage?

Use a smaller Whisper model:

```bash
export STT_WHISPER_MODEL=tiny  # Smallest and fastest
```

### More help?

See the **[Deployment Guide](docs/DEPLOYMENT.md)** for detailed troubleshooting.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for Telegram integration

## Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/Mahmoud-Emad/televoica/issues)
- 💬 [Discussions](https://github.com/Mahmoud-Emad/televoica/discussions)
