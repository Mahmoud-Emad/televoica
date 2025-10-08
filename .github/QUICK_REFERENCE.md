# Quick Reference Card

## 🚀 Deploy in 3 Steps

### Step 1: Add Secret
```
Settings → Secrets → Actions → New secret
Name: TELEGRAM_BOT_TOKEN
Value: YOUR_BOT_TOKEN_HERE
```

### Step 2: Run Workflow
```
Actions → Deploy Bot with Docker → Run workflow
```

### Step 3: Test Bot
```
Open Telegram → Search for your bot → Send /start
```

## 📋 Common Commands

### Docker

```bash
# Start bot
docker compose up -d

# View logs
docker compose logs -f

# Stop bot
docker compose down

# Restart bot
docker compose restart

# Check status
docker compose ps
```

### Systemd

```bash
# Start bot
sudo systemctl start televoica-bot

# Stop bot
sudo systemctl stop televoica-bot

# Restart bot
sudo systemctl restart televoica-bot

# Check status
sudo systemctl status televoica-bot

# View logs
sudo journalctl -u televoica-bot -f
```

### Health Check

```bash
# Run health check
export TELEGRAM_BOT_TOKEN="your_token"
python scripts/health_check.py

# With test message
export HEALTH_CHECK_CHAT_ID="your_chat_id"
python scripts/health_check.py
```

## 🔧 Configuration Quick Reference

### Environment Variables

```bash
# Required
TELEGRAM_BOT_TOKEN=your_token_here

# Optional
STT_TELEGRAM_BOT=true
STT_PROVIDER=whisper
STT_WHISPER_MODEL=base          # tiny, base, small, medium, large
STT_WHISPER_DEVICE=cpu          # cpu or cuda
STT_WHISPER_LANGUAGE=           # en, ar, es, etc. or empty
TELEGRAM_ALLOWED_USERS=         # 123,456,789 or empty
TELEGRAM_MAX_FILE_SIZE_MB=20
STT_LOG_LEVEL=INFO
```

### Whisper Models

| Model | Size | Speed | Accuracy | RAM |
|-------|------|-------|----------|-----|
| tiny | 39M | Fastest | Low | ~1GB |
| base | 74M | Fast | Good | ~1GB |
| small | 244M | Medium | Better | ~2GB |
| medium | 769M | Slow | High | ~5GB |
| large | 1550M | Slowest | Highest | ~10GB |

## 🔍 Troubleshooting Quick Fixes

### Bot Not Starting

```bash
# Check token
echo $TELEGRAM_BOT_TOKEN

# Check logs
docker compose logs
# or
sudo journalctl -u televoica-bot -n 50

# Verify FFmpeg
ffmpeg -version
```

### Bot Not Responding

```bash
# Check if running
docker compose ps
# or
sudo systemctl status televoica-bot

# Run health check
python scripts/health_check.py

# Restart
docker compose restart
# or
sudo systemctl restart televoica-bot
```

### High Resource Usage

```bash
# Use smaller model
export STT_WHISPER_MODEL=tiny

# Check resources
docker stats televoica-bot
# or
htop
```

## 📊 Workflow Triggers

### Deploy Bot with Docker
- ✅ Push to main
- ✅ Manual trigger

### Deploy Bot Service
- ✅ Push to main
- ✅ Manual trigger

### Health Check
- ✅ Every 30 minutes
- ✅ Manual trigger

## 🔗 Quick Links

- [Full Setup Guide](../docs/GITHUB_ACTIONS_SETUP.md)
- [Deployment Guide](../docs/DEPLOYMENT.md)
- [Main README](../README.md)
- [Setup Summary](SETUP_SUMMARY.md)

## 📞 Get Bot Token

1. Open [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow instructions
4. Copy token

## 🎯 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Show welcome message |
| `/help` | Show help information |
| `/info` | Show bot information |

## 📁 Important Files

| File | Purpose |
|------|---------|
| `.github/workflows/deploy-docker.yml` | Docker deployment |
| `.github/workflows/deploy-bot-service.yml` | Systemd deployment |
| `.github/workflows/health-check.yml` | Health monitoring |
| `Dockerfile` | Docker image config |
| `docker-compose.yml` | Docker Compose config |
| `scripts/health_check.py` | Health check script |

## 🆘 Emergency Commands

```bash
# Stop everything
docker compose down
sudo systemctl stop televoica-bot

# Check what's using resources
docker stats
htop

# View all logs
docker compose logs --tail=100
sudo journalctl -u televoica-bot -n 100

# Clean up
docker system prune -a
```

## ✅ Pre-Deployment Checklist

- [ ] Bot token obtained from BotFather
- [ ] Token added to GitHub Secrets
- [ ] FFmpeg installed (for local deployment)
- [ ] Docker installed (for Docker deployment)
- [ ] Workflow triggered
- [ ] Bot tested with /start command
- [ ] Voice message tested
- [ ] Health check verified

## 🎨 Status Indicators

| Symbol | Meaning |
|--------|---------|
| ✅ | Success / Completed |
| ❌ | Failed / Error |
| ⚠️ | Warning |
| 🔄 | In Progress |
| 🏥 | Health Check |
| 🚀 | Deployment |

---

**Need more help?** Check the [full documentation](../docs/)

