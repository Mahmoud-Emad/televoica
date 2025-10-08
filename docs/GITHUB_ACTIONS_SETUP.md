# GitHub Actions Setup Guide

Quick guide to set up automated deployment and health checks for your Televoica bot.

## 🚀 Quick Start (5 Minutes)

### Step 1: Get Your Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. **Copy the token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Add Token to GitHub

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `TELEGRAM_BOT_TOKEN`
5. Value: Paste your bot token
6. Click **Add secret**

### Step 3: Deploy the Bot

**Option A: Using Docker (Recommended)**

1. Go to **Actions** tab
2. Click **Deploy Bot with Docker**
3. Click **Run workflow** → **Run workflow**
4. Wait 2-3 minutes for deployment

**Option B: Using Systemd (Linux Server)**

1. Set up a self-hosted runner (see below)
2. Go to **Actions** tab
3. Click **Deploy Bot Service (Production)**
4. Click **Run workflow** → **Run workflow**

### Step 4: Test Your Bot

1. Open Telegram
2. Search for your bot by username
3. Send `/start` command
4. Send a voice message
5. Bot should transcribe it!

## 📋 Available Workflows

### 1. Deploy Bot with Docker

**File**: `.github/workflows/deploy-docker.yml`

**What it does**:
- Builds Docker image
- Pushes to GitHub Container Registry
- Deploys container
- Runs health checks

**When it runs**:
- On push to `main` branch
- Manual trigger via Actions tab

**Best for**: Production deployment, easy management

### 2. Deploy Bot Service (Production)

**File**: `.github/workflows/deploy-bot-service.yml`

**What it does**:
- Installs dependencies
- Creates systemd service
- Starts bot as system service
- Enables auto-start on boot

**When it runs**:
- On push to `main` branch
- Manual trigger via Actions tab

**Best for**: Linux servers with systemd

### 3. Bot Health Check

**File**: `.github/workflows/health-check.yml`

**What it does**:
- Checks bot connection
- Verifies bot can receive updates
- Monitors system resources
- Creates GitHub issue on failure

**When it runs**:
- Every 30 minutes (cron schedule)
- Manual trigger via Actions tab

**Best for**: Monitoring bot uptime

## 🔧 Configuration

### Required Secrets

| Secret Name | Required | Description | Example |
|------------|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | Your bot token from BotFather | `1234567890:ABC...` |

### Optional Secrets

| Secret Name | Required | Description | Example |
|------------|----------|-------------|---------|
| `HEALTH_CHECK_CHAT_ID` | ❌ No | Chat ID for health check messages | `123456789` |
| `TELEGRAM_ALLOWED_USERS` | ❌ No | Comma-separated user IDs | `123,456,789` |

### Environment Variables

You can customize bot behavior by editing the workflow files:

```yaml
environment:
  STT_PROVIDER: whisper              # STT provider (whisper, google_cloud)
  STT_WHISPER_MODEL: base            # Model size (tiny, base, small, medium, large)
  STT_WHISPER_DEVICE: cpu            # Device (cpu, cuda)
  STT_WHISPER_LANGUAGE: ""           # Language code (en, ar, es, etc.) or empty for auto
  TELEGRAM_MAX_FILE_SIZE_MB: 20      # Max file size in MB
  STT_LOG_LEVEL: INFO                # Log level (DEBUG, INFO, WARNING, ERROR)
```

## 🖥️ Self-Hosted Runner Setup

For deploying to your own server:

### 1. Prepare Your Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.10 python3-pip ffmpeg git

# Install Docker (optional, for Docker deployment)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### 2. Add Self-Hosted Runner

1. Go to repository **Settings** → **Actions** → **Runners**
2. Click **New self-hosted runner**
3. Choose **Linux** and **x64**
4. Follow the commands shown:

```bash
# Download
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure
./config.sh --url https://github.com/YOUR_USERNAME/televoica --token YOUR_TOKEN

# Install as service
sudo ./svc.sh install
sudo ./svc.sh start
```

### 3. Update Workflow

Edit `.github/workflows/deploy-bot-service.yml`:

```yaml
jobs:
  deploy-to-server:
    runs-on: self-hosted  # Change from ubuntu-latest
```

## 📊 Monitoring

### View Workflow Runs

1. Go to **Actions** tab
2. Click on a workflow
3. View logs and status

### Check Bot Status

**Via GitHub Actions**:
1. Go to **Actions** → **Bot Health Check**
2. Click **Run workflow**
3. View results

**Via Command Line** (if using self-hosted runner):

```bash
# Docker
docker compose ps
docker compose logs -f

# Systemd
sudo systemctl status televoica-bot
sudo journalctl -u televoica-bot -f
```

### Health Check Schedule

The health check runs automatically every 30 minutes. To change:

Edit `.github/workflows/health-check.yml`:

```yaml
on:
  schedule:
    - cron: '*/30 * * * *'  # Every 30 minutes
    # - cron: '0 * * * *'   # Every hour
    # - cron: '0 */6 * * *' # Every 6 hours
```

## 🐛 Troubleshooting

### Workflow Fails with "Secret not found"

**Solution**: Make sure you added `TELEGRAM_BOT_TOKEN` to repository secrets (not environment variables)

### Bot Doesn't Respond

1. Check workflow logs in Actions tab
2. Verify bot token is correct
3. Run health check workflow manually
4. Check if bot is running:
   ```bash
   docker compose ps  # For Docker
   sudo systemctl status televoica-bot  # For systemd
   ```

### "Permission denied" Errors

**For Docker**:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

**For systemd**:
```bash
sudo chmod +x /path/to/televoica
```

### High Resource Usage

Use a smaller Whisper model:

Edit workflow file:
```yaml
environment:
  STT_WHISPER_MODEL: tiny  # Smallest, fastest
  # STT_WHISPER_MODEL: base  # Default
  # STT_WHISPER_MODEL: small  # Better accuracy
```

## 🔄 Updating the Bot

### Automatic Updates

The bot automatically redeploys when you push to `main` branch:

```bash
git add .
git commit -m "Update bot"
git push origin main
```

### Manual Update

1. Go to **Actions** tab
2. Select deployment workflow
3. Click **Run workflow**
4. Click **Run workflow** button

## 📝 Best Practices

### 1. Use Docker for Production

Docker provides:
- Consistent environment
- Easy rollbacks
- Resource limits
- Health checks

### 2. Enable Health Checks

Keep the health check workflow enabled to:
- Monitor bot uptime
- Get alerts on failures
- Track performance

### 3. Secure Your Secrets

- Never commit tokens to git
- Use GitHub Secrets for sensitive data
- Rotate tokens periodically

### 4. Monitor Logs

Regularly check logs for:
- Errors and warnings
- Usage patterns
- Performance issues

### 5. Set Resource Limits

In `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
```

## 📚 Additional Resources

- [Full Deployment Guide](DEPLOYMENT.md)
- [Main README](../README.md)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🆘 Getting Help

If you encounter issues:

1. Check [Troubleshooting](#troubleshooting) section
2. Review workflow logs in Actions tab
3. [Create an issue](https://github.com/YOUR_USERNAME/televoica/issues)
4. Include:
   - Error message
   - Workflow logs
   - Steps to reproduce

