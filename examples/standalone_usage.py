"""
Example: Using the speech-to-text engine as a standalone library.

This example demonstrates how to use the core SpeechToTextEngine
without the Telegram bot integration.
"""

from pathlib import Path
from televoica.core.engine import SpeechToTextEngine
from televoica.core.providers import WhisperProvider, GoogleCloudSTTProvider


def example_basic_usage():
    """Basic usage with default Whisper provider."""
    print("Example 1: Basic usage with default Whisper provider")
    print("-" * 50)
    
    # Create engine with default provider (Whisper base model)
    engine = SpeechToTextEngine()
    
    # Transcribe an audio file
    audio_file = Path("path/to/your/audio.mp3")
    
    if audio_file.exists():
        text = engine.transcribe_file(audio_file)
        print(f"Transcription: {text}")
    else:
        print(f"Audio file not found: {audio_file}")
    
    print()


def example_custom_whisper():
    """Using Whisper with custom configuration."""
    print("Example 2: Custom Whisper configuration")
    print("-" * 50)
    
    # Create Whisper provider with custom settings
    whisper_provider = WhisperProvider({
        "model": "medium",  # Use larger model for better accuracy
        "device": "cpu",    # Use "cuda" for GPU acceleration
        "language": "en",   # Specify language for better accuracy
    })
    
    # Create engine with custom provider
    engine = SpeechToTextEngine(provider=whisper_provider)
    
    # Transcribe
    audio_file = Path("path/to/your/audio.mp3")
    
    if audio_file.exists():
        text = engine.transcribe_file(audio_file)
        print(f"Transcription: {text}")
    else:
        print(f"Audio file not found: {audio_file}")
    
    print()


def example_google_cloud():
    """Using Google Cloud Televoica."""
    print("Example 3: Google Cloud Televoica")
    print("-" * 50)
    
    # Create Google Cloud provider
    google_provider = GoogleCloudSTTProvider({
        "credentials_path": "path/to/credentials.json",
        "language_code": "en-US",
    })
    
    # Create engine with Google Cloud provider
    engine = SpeechToTextEngine(provider=google_provider)
    
    # Transcribe
    audio_file = Path("path/to/your/audio.mp3")
    
    if audio_file.exists():
        text = engine.transcribe_file(audio_file)
        print(f"Transcription: {text}")
    else:
        print(f"Audio file not found: {audio_file}")
    
    print()


def example_transcribe_bytes():
    """Transcribing audio from bytes (e.g., from API, download, etc.)."""
    print("Example 4: Transcribing audio bytes")
    print("-" * 50)
    
    # Create engine
    engine = SpeechToTextEngine()
    
    # Read audio file as bytes
    audio_file = Path("path/to/your/audio.mp3")
    
    if audio_file.exists():
        audio_bytes = audio_file.read_bytes()
        
        # Transcribe bytes
        text = engine.transcribe_bytes(audio_bytes, format="mp3")
        print(f"Transcription: {text}")
    else:
        print(f"Audio file not found: {audio_file}")
    
    print()


def example_switching_providers():
    """Switching between different providers."""
    print("Example 5: Switching providers")
    print("-" * 50)
    
    # Create engine with Whisper
    engine = SpeechToTextEngine()
    
    audio_file = Path("path/to/your/audio.mp3")
    
    if audio_file.exists():
        # Transcribe with Whisper
        print("Using Whisper...")
        text1 = engine.transcribe_file(audio_file)
        print(f"Whisper result: {text1}")
        
        # Switch to Google Cloud
        print("\nSwitching to Google Cloud...")
        google_provider = GoogleCloudSTTProvider({
            "credentials_path": "path/to/credentials.json",
            "language_code": "en-US",
        })
        engine.set_provider(google_provider)
        
        # Transcribe with Google Cloud
        text2 = engine.transcribe_file(audio_file)
        print(f"Google Cloud result: {text2}")
    else:
        print(f"Audio file not found: {audio_file}")
    
    print()


if __name__ == "__main__":
    print("Televoica Robot - Standalone Usage Examples")
    print("=" * 50)
    print()
    
    # Run examples
    example_basic_usage()
    # example_custom_whisper()
    # example_google_cloud()
    # example_transcribe_bytes()
    # example_switching_providers()
    
    print("\nNote: Uncomment the examples you want to run and provide valid audio file paths.")

