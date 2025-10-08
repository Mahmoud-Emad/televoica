# Televoica Examples

This directory contains example scripts demonstrating how to use Televoica in different ways.

## Prerequisites

Before running any examples:

1. **Install dependencies:**

   ```bash
   poetry install
   ```

2. **Get a Telegram bot token:**
   - Open [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` and follow instructions
   - Copy the bot token

3. **Set up environment variables:**

   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your bot token
   # TELEGRAM_BOT_TOKEN=your_token_here
   ```

## Available Examples

### 1. bot_usage.py - Telegram Bot Example

Demonstrates how to run the Telegram bot programmatically.

**Features:**

- Automatically loads configuration from .env file
- Simple and straightforward
- Shows bot configuration before starting
- Easy to customize via .env file

**Usage:**

```bash
# Create .env file from example
cp .env.example .env

# Edit .env and add your bot token
# TELEGRAM_BOT_TOKEN=your_token_here

# Run the example
python examples/bot_usage.py
```

**What it does:**

- Loads all settings from .env file
- Displays configuration summary
- Starts the bot
- Handles Ctrl+C gracefully

### 2. standalone_usage.py - Standalone STT Examples

Demonstrates using Televoica as a standalone library without Telegram.

**Features:**

- Transcribe audio files directly
- Use different STT providers
- Process audio bytes
- No Telegram bot required

**Usage:**

```bash
# Transcribe an audio file
python examples/standalone_usage.py path/to/audio.mp3

# Or run the example with sample code
python examples/standalone_usage.py
```

## Environment Variables

All examples support these environment variables:

### Required

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### Optional

```bash
# Bot mode
STT_TELEGRAM_BOT=true

# STT Provider
STT_PROVIDER=whisper                     # whisper or google_cloud

# Whisper settings
STT_WHISPER_MODEL=base                   # tiny, base, small, medium, large
STT_WHISPER_DEVICE=cpu                   # cpu or cuda
STT_WHISPER_LANGUAGE=                    # en, ar, es, etc. (empty = auto)

# Telegram settings
TELEGRAM_ALLOWED_USERS=                  # Comma-separated user IDs
TELEGRAM_MAX_FILE_SIZE_MB=20             # Max file size in MB

# Logging
STT_LOG_LEVEL=INFO                       # DEBUG, INFO, WARNING, ERROR
```

## Quick Start

### Run Bot with Default Settings

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your token
# TELEGRAM_BOT_TOKEN=your_token_here

# Run bot
python examples/bot_usage.py
```

### Run Bot with Custom Model

```bash
# Edit .env file and change the model
# STT_WHISPER_MODEL=medium

# Run bot
python examples/bot_usage.py
```

### Transcribe Audio File (No Bot)

```bash
# No token needed for standalone mode
python examples/standalone_usage.py audio.mp3
```

## Using .env File

The easiest way to manage configuration:

```bash
# Create .env file
cat > .env << EOF
TELEGRAM_BOT_TOKEN=your_token_here
STT_TELEGRAM_BOT=true
STT_PROVIDER=whisper
STT_WHISPER_MODEL=base
STT_WHISPER_DEVICE=cpu
STT_LOG_LEVEL=INFO
EOF

# Run any example - it will automatically load .env
python examples/bot_usage.py
```

## Troubleshooting

### "TELEGRAM_BOT_TOKEN not set"

**Solution:**

```bash
# Set environment variable
export TELEGRAM_BOT_TOKEN="your_token_here"

# Or create .env file
echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env
```

### "FFmpeg not found"

**Solution:**

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### "Module not found"

**Solution:**

```bash
# Install dependencies
poetry install

# Or with pip
pip install -e .
```

### Bot not responding

**Solution:**

1. Check if token is correct
2. Verify bot is running
3. Test with `/start` command
4. Check logs for errors

## Model Comparison

| Model | Size | Speed | Accuracy | RAM | Best For |
|-------|------|-------|----------|-----|----------|
| tiny | 39M | Fastest | Low | ~1GB | Testing, low resources |
| base | 74M | Fast | Good | ~1GB | **Recommended default** |
| small | 244M | Medium | Better | ~2GB | Better accuracy needed |
| medium | 769M | Slow | High | ~5GB | High accuracy required |
| large | 1550M | Slowest | Highest | ~10GB | Maximum accuracy |

## Tips

1. **Start with `base` model** - Good balance of speed and accuracy
2. **Use `.env` file** - Easier than setting environment variables
3. **Test locally first** - Before deploying to production
4. **Check logs** - Set `STT_LOG_LEVEL=DEBUG` for troubleshooting
5. **Use smaller models** - If you have limited resources

## Next Steps

After running examples:

1. **Deploy to production:**
   - See [Deployment Guide](../docs/DEPLOYMENT.md)
   - Use Docker for easy deployment
   - Set up GitHub Actions for automation

2. **Customize:**
   - Adjust model size for your needs
   - Set user restrictions
   - Configure file size limits

3. **Monitor:**
   - Use health checks
   - Check logs regularly
   - Monitor resource usage

## Additional Resources

- [Main README](../README.md)
- [Deployment Guide](../docs/DEPLOYMENT.md)
- [GitHub Actions Setup](../docs/GITHUB_ACTIONS_SETUP.md)
- [Local Testing Guide](../LOCAL_TESTING.md)
- [API Documentation](../docs/)

## Support

If you need help:

1. Check this README
2. Review [Troubleshooting Guide](../.github/TROUBLESHOOTING.md)
3. Test with examples first
4. Create an issue on GitHub
