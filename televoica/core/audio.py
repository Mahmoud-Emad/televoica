"""Audio inspection and chunking utilities using ffmpeg/ffprobe."""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

# Default chunk length (seconds). 5 minutes balances Whisper RAM usage,
# per-chunk progress granularity, and the 30s Whisper window cost overhead.
DEFAULT_CHUNK_SECONDS = 300


def _require_binary(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(
            f"{name} is required but was not found on PATH. "
            f"Install it (e.g. `apt install ffmpeg`)."
        )
    return path


def probe_duration_seconds(audio_file: Path) -> Optional[float]:
    """Return the duration of an audio file in seconds, or None if unknown."""
    ffprobe = _require_binary("ffprobe")
    try:
        result = subprocess.run(
            [
                ffprobe,
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json",
                str(audio_file),
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.CalledProcessError as e:
        logger.warning("ffprobe failed for %s: %s", audio_file, e.stderr.strip())
        return None
    except subprocess.TimeoutExpired:
        logger.warning("ffprobe timed out for %s", audio_file)
        return None

    try:
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except (KeyError, ValueError, json.JSONDecodeError):
        return None


def split_into_chunks(
    audio_file: Path,
    output_dir: Path,
    chunk_seconds: int = DEFAULT_CHUNK_SECONDS,
) -> List[Path]:
    """Split an audio file into mono 16kHz wav chunks of `chunk_seconds`.

    Returns the list of chunk paths in order. The output format (wav, mono,
    16kHz) matches what Whisper resamples to internally, so we avoid a second
    pass during transcription.
    """
    ffmpeg = _require_binary("ffmpeg")
    output_dir.mkdir(parents=True, exist_ok=True)
    pattern = output_dir / f"{audio_file.stem}_chunk_%03d.wav"

    cmd = [
        ffmpeg,
        "-y",
        "-i", str(audio_file),
        "-f", "segment",
        "-segment_time", str(chunk_seconds),
        "-ac", "1",
        "-ar", "16000",
        "-c:a", "pcm_s16le",
        str(pattern),
    ]
    logger.info("Splitting %s into %ds chunks", audio_file.name, chunk_seconds)
    subprocess.run(cmd, check=True, capture_output=True, text=True)

    return sorted(output_dir.glob(f"{audio_file.stem}_chunk_*.wav"))
