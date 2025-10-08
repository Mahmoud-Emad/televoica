# GitHub Actions Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: `--no-dev` option does not exist

**Error:**

```
The option "--no-dev" does not exist
Error: Process completed with exit code 1.
```

**Cause:** Poetry 1.2+ deprecated `--no-dev` in favor of `--only main` or `--without dev`

**Solution:** ✅ **FIXED** - Updated all workflows to use `--only main`

---

### Issue 2: Systemd service fails to start

**Error:**

```
❌ Bot service failed to start
Main process exited, code=exited, status=1/FAILURE
```

**Possible Causes:**

1. Incorrect Python/televoica path in ExecStart
2. Missing dependencies
3. Bot token not properly passed to service
4. Virtual environment not activated

**Solution:** ✅ **FIXED** - Updated systemd service configuration

**To debug further:**

```bash
# Check service status
sudo systemctl status televoica-bot

# View detailed logs
sudo journalctl -u televoica-bot -n 100 --no-pager

# Check log files
sudo cat /var/log/televoica-bot.log
sudo cat /var/log/televoica-bot-error.log

# Test command manually
cd /path/to/televoica
poetry run televoica bot
```

---

### Issue 3: Docker permission denied on logs directory

**Error:**

```
error while creating mount source path '/Users/mahmoud/work/research/televoica/logs': 
chown /Users/mahmoud/work/research/televoica/logs: permission denied
```

**Solution:** ✅ **FIXED** - Commented out logs volume in docker-compose.yml

**Alternative solutions:**

```bash
# Option 1: Create logs directory first
mkdir -p logs
chmod 755 logs

# Option 2: Use Docker logs instead
docker compose logs -f
```

---

## Recommended Deployment Approach

Based on the issues encountered, here's the recommended approach:

### 1. Test First (Recommended)

Use the new **Deploy Bot (Simple)** workflow to test your configuration:

```
Actions → Deploy Bot (Simple) → Run workflow
```

This workflow:

- ✅ Tests installation
- ✅ Verifies configuration
- ✅ Runs health check
- ✅ Doesn't require systemd
- ✅ Easy to debug

### 2. Deploy with Docker (Production)

Once testing passes, use Docker for production:

```
Actions → Deploy Bot with Docker → Run workflow
```

Or locally:

```bash
docker compose up -d
```

### 3. Alternative: Manual Deployment

For maximum control:

```bash
# On your server
git clone https://github.com/YOUR_USERNAME/televoica.git
cd televoica

# Install dependencies
poetry install

# Set environment variables
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
export STT_TELEGRAM_BOT=true

# Run bot
poetry run televoica bot
```

---

## Workflow Comparison

| Workflow | Use Case | Complexity | Reliability |
|----------|----------|------------|-------------|
| **Deploy Bot (Simple)** | Testing | Low | High ✅ |
| **Deploy Bot with Docker** | Production | Medium | High ✅ |
| **Deploy Bot Service** | Self-hosted | High | Medium ⚠️ |

---

## Debugging Checklist

When a workflow fails, check:

- [ ] **Secrets configured?**
  - Settings → Secrets → Actions
  - `TELEGRAM_BOT_TOKEN` is set

- [ ] **Bot token valid?**
  - Test with [@BotFather](https://t.me/BotFather)
  - Send `/mybots` to verify

- [ ] **Dependencies installed?**
  - Check workflow logs
  - Look for Poetry installation errors

- [ ] **FFmpeg available?**
  - Required for audio processing
  - Should be installed in workflow

- [ ] **Python version correct?**
  - Should be 3.10+
  - Check workflow configuration

---

## Getting More Help

### 1. Check Workflow Logs

1. Go to **Actions** tab
2. Click on failed workflow
3. Click on failed job
4. Expand failed step
5. Read error messages

### 2. Run Health Check

```bash
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
python scripts/health_check.py
```

### 3. Test Locally

```bash
# Clone and test
git clone https://github.com/YOUR_USERNAME/televoica.git
cd televoica
poetry install
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
poetry run televoica bot
```

### 4. Enable Debug Logging

Edit workflow to add:

```yaml
env:
  STT_LOG_LEVEL: DEBUG
```

---

## Fixed Issues Summary

✅ **Poetry `--no-dev` deprecated** - Updated to `--only main`
✅ **Systemd ExecStart path** - Fixed to use correct virtual env path
✅ **Docker logs permission** - Made logs volume optional
✅ **Added simple test workflow** - For easier debugging

---

## Current Status

All workflows have been updated and should work correctly:

1. ✅ **deploy-simple.yml** - New, simplified testing workflow
2. ✅ **deploy-docker.yml** - Docker deployment (recommended)
3. ✅ **deploy-bot-service.yml** - Systemd deployment (fixed)
4. ✅ **health-check.yml** - Health monitoring

---

## Next Steps

1. **Try the simple workflow first:**

   ```
   Actions → Deploy Bot (Simple) → Run workflow
   ```

2. **If that passes, deploy with Docker:**

   ```
   Actions → Deploy Bot with Docker → Run workflow
   ```

3. **Monitor with health checks:**

   ```
   Actions → Bot Health Check → Run workflow
   ```

---

## Support

If you still encounter issues:

1. Check this troubleshooting guide
2. Review workflow logs
3. Test locally first
4. Create a GitHub issue with:
   - Error message
   - Workflow logs
   - Steps to reproduce
