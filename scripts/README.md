# Scripts Directory

This directory contains utility scripts for managing and monitoring the Televoica bot.

## Available Scripts

### health_check.py

Health check script for monitoring bot status.

**Purpose**: Verify that the bot is running and responsive.

**Usage**:

```bash
# Basic health check
export TELEGRAM_BOT_TOKEN="your_token_here"
python scripts/health_check.py

# With test message
export TELEGRAM_BOT_TOKEN="your_token_here"
export HEALTH_CHECK_CHAT_ID="your_chat_id"
python scripts/health_check.py
```

**What it checks**:

- Bot connection to Telegram API
- Bot can receive updates
- System resources (CPU, memory, disk)
- Optional: Send test message to verify bot is responding

**Exit codes**:

- `0`: All checks passed
- `1`: One or more checks failed

**Environment variables**:

- `TELEGRAM_BOT_TOKEN` (required): Your bot token
- `HEALTH_CHECK_CHAT_ID` (optional): Chat ID to send test messages

**Example output**:

```
============================================================
Starting Televoica Bot Health Check
============================================================

1. Checking bot connection...
Bot connection successful
   Bot username: @your_bot
   Bot name: Your Bot Name
   Bot ID: 1234567890

2. Checking bot updates...
Bot can receive updates (last update count: 5)

3. Sending test message...
Test message sent successfully to chat 123456789

4. Checking system resources...
   CPU usage: 15.2%
   Memory usage: 45.3% (3.62GB / 8.00GB)
   Disk usage: 62.1% (124.2GB / 200.0GB)

============================================================
Health Check Summary
============================================================
Checks passed: 4/4
All health checks passed!
============================================================
```

## Adding New Scripts

When adding new scripts to this directory:

1. Add a shebang line: `#!/usr/bin/env python3`
2. Make it executable: `chmod +x scripts/your_script.py`
3. Add documentation to this README
4. Include usage examples
5. Document environment variables
6. Add error handling

## Dependencies

Scripts may require additional dependencies:

```bash
# For health_check.py
pip install python-telegram-bot psutil
```

Or install all project dependencies:

```bash
poetry install
```
