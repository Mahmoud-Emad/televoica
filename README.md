# Televoica Robot

A modular, high-accuracy speech-to-text library with optional Telegram bot integration. Built with Python and designed for flexibility and ease of use.

## Features

- **Dual Mode Operation**: Use as a standalone library or as a Telegram bot
- **Modular Architecture**: Core STT functionality separated from bot integration
- **Multiple STT Providers**: Support for OpenAI Whisper and Google Cloud Televoica
- **Flexible Configuration**: Environment variables, config files, or programmatic setup
- **Easy to Use**: Simple CLI and Python API
- **Production Ready**: Proper error handling, logging, and type hints

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
