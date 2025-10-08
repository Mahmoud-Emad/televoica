# GitHub Actions Setup Summary

## ✅ What Has Been Created

This repository now includes complete GitHub Actions workflows for automated deployment and monitoring of your Televoica Telegram bot.

## 📁 Files Created

### GitHub Actions Workflows

1. **`.github/workflows/deploy-docker.yml`**
   - Builds Docker image
   - Pushes to GitHub Container Registry
   - Deploys containerized bot
   - Runs health checks

2. **`.github/workflows/deploy-bot-service.yml`**
   - Deploys bot as systemd service
   - Configures auto-start on boot
   - Manages service lifecycle

3. **`.github/workflows/health-check.yml`**
   - Runs every 30 minutes
   - Checks bot health
   - Creates GitHub issues on failure
   - Monitors system resources

### Docker Configuration

4. **`Dockerfile`**
   - Multi-stage build for efficiency
   - Includes FFmpeg and dependencies
   - Non-root user for security
   - Health check support

5. **`docker-compose.yml`**
   - Easy local deployment
   - Environment variable configuration
   - Resource limits
   - Volume management

### Scripts

6. **`scripts/health_check.py`**
   - Comprehensive health monitoring
   - Telegram API connectivity check
   - System resource monitoring
   - Optional test message sending

7. **`scripts/README.md`**
   - Documentation for utility scripts

### Documentation

8. **`docs/DEPLOYMENT.md`**
   - Complete deployment guide
   - Multiple deployment methods
   - Troubleshooting section
   - Configuration examples

9. **`docs/GITHUB_ACTIONS_SETUP.md`**
   - Quick start guide
   - Step-by-step instructions
   - Workflow explanations
   - Best practices

10. **`README.md`** (Updated)
    - Added deployment section
    - GitHub Actions quick start
    - Docker instructions
    - Health monitoring info

## 🚀 Quick Start

### 1. Add Your Bot Token

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `TELEGRAM_BOT_TOKEN`
4. Value: Your bot token from [@BotFather](https://t.me/BotFather)
5. Click **Add secret**

### 2. Deploy

**Option A: Docker (Recommended)**

- Go to **Actions** → **Deploy Bot with Docker** → **Run workflow**

**Option B: Systemd Service**

- Set up self-hosted runner first
- Go to **Actions** → **Deploy Bot Service** → **Run workflow**

**Option C: Local Docker**

```bash
echo "TELEGRAM_BOT_TOKEN=YOUR_TOKEN" > .env
docker compose up -d
```

### 3. Monitor

- Health checks run automatically every 30 minutes
- View status in **Actions** tab
- Check logs in workflow runs

## 🔧 Configuration

### Required Secrets

| Secret | Description |
|--------|-------------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token (required) |

### Optional Secrets

| Secret | Description |
|--------|-------------|
| `HEALTH_CHECK_CHAT_ID` | Chat ID for health check messages |
| `TELEGRAM_ALLOWED_USERS` | Comma-separated user IDs |

### Environment Variables

Edit workflow files to customize:

```yaml
environment:
  STT_WHISPER_MODEL: base    # tiny, base, small, medium, large
  STT_WHISPER_DEVICE: cpu    # cpu or cuda
  STT_LOG_LEVEL: INFO        # DEBUG, INFO, WARNING, ERROR
```

## 📊 Workflows Explained

### Deploy Bot with Docker

**Triggers**:

- Push to `main` branch
- Manual trigger

**Steps**:

1. Build Docker image
2. Push to GitHub Container Registry
3. Deploy container
4. Run health check
5. Verify deployment

**Best for**: Production deployment

### Deploy Bot Service

**Triggers**:

- Push to `main` branch
- Manual trigger

**Steps**:

1. Install dependencies
2. Create systemd service
3. Start service
4. Enable auto-start
5. Verify status

**Best for**: Linux servers with systemd

### Bot Health Check

**Triggers**:

- Every 30 minutes (cron)
- Manual trigger

**Steps**:

1. Check bot connection
2. Verify updates
3. Monitor resources
4. Create issue on failure

**Best for**: Continuous monitoring

## 🎯 Next Steps

1. **Test the bot**:
   - Send `/start` to your bot
   - Send a voice message
   - Verify transcription works

2. **Monitor health**:
   - Check Actions tab regularly
   - Review health check results
   - Address any issues

3. **Customize**:
   - Adjust Whisper model size
   - Configure user restrictions
   - Set resource limits

4. **Scale**:
   - Use GPU for faster processing
   - Increase file size limits
   - Add more monitoring

## 📚 Documentation

- **[GitHub Actions Setup Guide](../docs/GITHUB_ACTIONS_SETUP.md)** - Detailed setup instructions
- **[Deployment Guide](../docs/DEPLOYMENT.md)** - Complete deployment guide
- **[Main README](../README.md)** - Project overview

## 🆘 Troubleshooting

### Workflow fails with "Secret not found"

**Solution**: Add `TELEGRAM_BOT_TOKEN` to repository secrets

### Bot doesn't respond

**Solution**:

1. Check workflow logs
2. Run health check manually
3. Verify bot token is correct

### High resource usage

**Solution**: Use smaller Whisper model (`tiny` or `base`)

## 💡 Tips

1. **Start with Docker** - Easiest deployment method
2. **Enable health checks** - Catch issues early
3. **Monitor logs** - Review regularly for errors
4. **Use smaller models** - Start with `base` or `tiny`
5. **Test locally first** - Verify before deploying

## 🔗 Useful Links

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [OpenAI Whisper](https://github.com/openai/whisper)

## ✨ Features

- ✅ Automated deployment
- ✅ Health monitoring
- ✅ Docker support
- ✅ Systemd integration
- ✅ Resource monitoring
- ✅ Error notifications
- ✅ Easy configuration
- ✅ Comprehensive documentation

---

**Ready to deploy?** Follow the [Quick Start](#-quick-start) above!
