# Televoica Bot Deployment Guide

This guide explains how to deploy and manage the Televoica Telegram bot using GitHub Actions.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [GitHub Secrets Setup](#github-secrets-setup)
- [Deployment Methods](#deployment-methods)
- [Health Checks](#health-checks)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Overview

The Televoica bot can be deployed using three different methods:

1. **Systemd Service** - Traditional Linux service deployment
2. **Docker** - Containerized deployment (recommended)
3. **Manual** - Direct Python execution

## Prerequisites

### System Requirements

- Python 3.10 or higher
- FFmpeg (for audio processing)
- 2GB RAM minimum (4GB recommended)
- 2 CPU cores recommended

### Required Accounts

- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- GitHub account with Actions enabled

## GitHub Secrets Setup

### Required Secrets

Navigate to your repository → Settings → Secrets and variables → Actions, then add:

1. **TELEGRAM_BOT_TOKEN** (Required)
   - Your Telegram bot token from BotFather
   - Example: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### Optional Secrets

2. **HEALTH_CHECK_CHAT_ID** (Optional)
   - Chat ID to receive health check messages
   - Get your chat ID by messaging [@userinfobot](https://t.me/userinfobot)
   - Example: `123456789`

3. **TELEGRAM_ALLOWED_USERS** (Optional)
   - Comma-separated list of allowed user IDs
   - Leave empty to allow all users
   - Example: `123456789,987654321`

### How to Get Your Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the token provided by BotFather
5. Add it to GitHub Secrets as `TELEGRAM_BOT_TOKEN`

## Deployment Methods

### Method 1: Docker Deployment (Recommended)

This is the easiest and most reliable method.

#### Setup

1. **Add the secret to GitHub**:
   - Go to Settings → Secrets → Actions
   - Add `TELEGRAM_BOT_TOKEN` with your bot token

2. **Trigger deployment**:
   - Push to `main` branch, or
   - Go to Actions → "Deploy Bot with Docker" → Run workflow

3. **The workflow will**:
   - Build a Docker image
   - Push it to GitHub Container Registry
   - Deploy the container
   - Run health checks

#### Local Docker Deployment

```bash
# Create .env file
cat > .env << EOF
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
STT_PROVIDER=whisper
STT_WHISPER_MODEL=base
STT_WHISPER_DEVICE=cpu
STT_LOG_LEVEL=INFO
EOF

# Start the bot
docker compose up -d

# Check logs
docker compose logs -f

# Check status
docker compose ps

# Stop the bot
docker compose down
```

### Method 2: Systemd Service Deployment

For deployment on a Linux server with systemd.

#### Setup

1. **Configure self-hosted runner** (optional):
   - Settings → Actions → Runners → New self-hosted runner
   - Follow instructions to set up on your server

2. **Trigger deployment**:
   - Push to `main` branch, or
   - Go to Actions → "Deploy Bot Service (Production)" → Run workflow

3. **The workflow will**:
   - Install dependencies
   - Create systemd service
   - Start the bot
   - Enable auto-start on boot

#### Manual Systemd Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/televoica.git
cd televoica

# Install dependencies
poetry install

# Create systemd service
sudo tee /etc/systemd/system/televoica-bot.service > /dev/null << EOF
[Unit]
Description=Televoica Telegram Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment="TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE"
Environment="STT_TELEGRAM_BOT=true"
Environment="STT_PROVIDER=whisper"
Environment="STT_WHISPER_MODEL=base"
Environment="STT_WHISPER_DEVICE=cpu"
ExecStart=$(poetry env info --path)/bin/python -m televoica.cli.main bot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl enable televoica-bot
sudo systemctl start televoica-bot

# Check status
sudo systemctl status televoica-bot

# View logs
sudo journalctl -u televoica-bot -f
```

### Method 3: Manual Deployment

For development or testing.

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/televoica.git
cd televoica

# Install dependencies
poetry install

# Set environment variables
export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
export STT_TELEGRAM_BOT=true
export STT_PROVIDER=whisper
export STT_WHISPER_MODEL=base
export STT_WHISPER_DEVICE=cpu

# Run bot
poetry run televoica bot
```

## Health Checks

### Automated Health Checks

The bot includes automated health checks that run every 30 minutes:

- **What it checks**:
  - Bot connection to Telegram API
  - Ability to receive updates
  - System resources (CPU, memory, disk)
  - Optional: Send test message

- **On failure**:
  - Creates GitHub issue
  - Logs error details
  - Can send notifications (configure in workflow)

### Manual Health Check

```bash
# Set environment variable
export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"

# Run health check
python scripts/health_check.py

# With test message
export HEALTH_CHECK_CHAT_ID="YOUR_CHAT_ID"
python scripts/health_check.py
```

### Trigger Manual Health Check

Go to Actions → "Bot Health Check" → Run workflow

## Monitoring

### View Logs

**Docker:**
```bash
docker compose logs -f
docker compose logs --tail=100
```

**Systemd:**
```bash
sudo journalctl -u televoica-bot -f
sudo journalctl -u televoica-bot -n 100
```

### Check Status

**Docker:**
```bash
docker compose ps
docker compose exec televoica-bot python scripts/health_check.py
```

**Systemd:**
```bash
sudo systemctl status televoica-bot
```

### Resource Usage

**Docker:**
```bash
docker stats televoica-bot
```

**System:**
```bash
htop
free -h
df -h
```

## Troubleshooting

### Bot Not Starting

1. **Check token**:
   ```bash
   # Verify token is set
   echo $TELEGRAM_BOT_TOKEN
   ```

2. **Check logs**:
   ```bash
   # Docker
   docker compose logs
   
   # Systemd
   sudo journalctl -u televoica-bot -n 50
   ```

3. **Verify dependencies**:
   ```bash
   # Check FFmpeg
   ffmpeg -version
   
   # Check Python
   python --version
   ```

### Bot Not Responding

1. **Check if running**:
   ```bash
   # Docker
   docker compose ps
   
   # Systemd
   sudo systemctl status televoica-bot
   ```

2. **Run health check**:
   ```bash
   python scripts/health_check.py
   ```

3. **Restart bot**:
   ```bash
   # Docker
   docker compose restart
   
   # Systemd
   sudo systemctl restart televoica-bot
   ```

### High Resource Usage

1. **Check model size**:
   - Use smaller Whisper model: `tiny`, `base`, or `small`
   - Set `STT_WHISPER_MODEL=tiny` for lowest resource usage

2. **Limit resources** (Docker):
   - Edit `docker-compose.yml`
   - Adjust CPU and memory limits

3. **Monitor usage**:
   ```bash
   docker stats televoica-bot
   ```

### GitHub Actions Failing

1. **Check secrets**:
   - Verify `TELEGRAM_BOT_TOKEN` is set in repository secrets
   - Check secret name matches exactly

2. **Check workflow logs**:
   - Go to Actions tab
   - Click on failed workflow
   - Review error messages

3. **Test locally**:
   ```bash
   # Run the same commands locally
   poetry install
   poetry run televoica bot
   ```

## Advanced Configuration

### Custom Whisper Model

```bash
# Use larger model for better accuracy
export STT_WHISPER_MODEL=medium

# Use GPU acceleration
export STT_WHISPER_DEVICE=cuda
```

### User Restrictions

```bash
# Only allow specific users
export TELEGRAM_ALLOWED_USERS=123456789,987654321
```

### File Size Limits

```bash
# Increase max file size to 50MB
export TELEGRAM_MAX_FILE_SIZE_MB=50
```

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/YOUR_USERNAME/televoica/issues)
- Documentation: [README.md](../README.md)

