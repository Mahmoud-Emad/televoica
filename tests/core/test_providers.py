"""Tests for STT providers."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from televoica.core.providers import (
    STTProvider,
    WhisperProvider,
    GoogleCloudSTTProvider,
)


class TestSTTProvider:
    """Test cases for the abstract STTProvider."""
    
    def test_cannot_instantiate_abstract_class(self):
        """Test that STTProvider cannot be instantiated directly."""
        with pytest.raises(TypeError):
            STTProvider()


class TestWhisperProvider:
    """Test cases for WhisperProvider."""
    
    def test_init_with_defaults(self):
        """Test initialization with default configuration."""
        provider = WhisperProvider()
        
        assert provider.model_size == "base"
        assert provider.device == "cpu"
        assert provider.language is None
    
    def test_init_with_custom_config(self):
        """Test initialization with custom configuration."""
        config = {
            "model": "medium",
            "device": "cuda",
            "language": "en",
        }
        provider = WhisperProvider(config)
        
        assert provider.model_size == "medium"
        assert provider.device == "cuda"
        assert provider.language == "en"
    
    @patch('televoica.core.providers.whisper')
    def test_load_model(self, mock_whisper):
        """Test lazy loading of Whisper model."""
        mock_model = MagicMock()
        mock_whisper.load_model.return_value = mock_model
        
        provider = WhisperProvider({"model": "base"})
        assert provider._model is None
        
        provider._load_model()
        
        assert provider._model == mock_model
        mock_whisper.load_model.assert_called_once_with("base", device="cpu")
    
    @patch('televoica.core.providers.whisper')
    def test_transcribe(self, mock_whisper, tmp_path):
        """Test transcription of audio file."""
        # Setup mock
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {"text": "  Test transcription  "}
        mock_whisper.load_model.return_value = mock_model
        
        # Create temporary audio file
        audio_file = tmp_path / "test.mp3"
        audio_file.write_text("fake audio")
        
        # Transcribe
        provider = WhisperProvider()
        result = provider.transcribe(audio_file)
        
        assert result == "Test transcription"
        mock_model.transcribe.assert_called_once()
    
    @patch('televoica.core.providers.whisper')
    def test_transcribe_bytes(self, mock_whisper, tmp_path):
        """Test transcription of audio bytes."""
        # Setup mock
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {"text": "Test transcription"}
        mock_whisper.load_model.return_value = mock_model
        
        # Transcribe bytes
        provider = WhisperProvider()
        audio_bytes = b"fake audio data"
        result = provider.transcribe_bytes(audio_bytes, format="ogg")
        
        assert result == "Test transcription"


class TestGoogleCloudSTTProvider:
    """Test cases for GoogleCloudSTTProvider."""
    
    def test_init_with_defaults(self):
        """Test initialization with default configuration."""
        provider = GoogleCloudSTTProvider()
        
        assert provider.credentials_path is None
        assert provider.language_code == "en-US"
    
    def test_init_with_custom_config(self):
        """Test initialization with custom configuration."""
        config = {
            "credentials_path": "/path/to/creds.json",
            "language_code": "ar-SA",
        }
        provider = GoogleCloudSTTProvider(config)
        
        assert provider.credentials_path == "/path/to/creds.json"
        assert provider.language_code == "ar-SA"
    
    @patch('televoica.core.providers.speech')
    def test_load_client(self, mock_speech):
        """Test lazy loading of Google Cloud client."""
        mock_client = MagicMock()
        mock_speech.SpeechClient.return_value = mock_client
        
        provider = GoogleCloudSTTProvider()
        assert provider._client is None
        
        provider._load_client()
        
        assert provider._client == mock_client
        mock_speech.SpeechClient.assert_called_once()

