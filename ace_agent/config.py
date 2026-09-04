from dataclasses import dataclass
import os
from dotenv import load_dotenv

@dataclass
class Settings:
    max_steps: int = 10
    action_delay: float = 0.2
    screenshot_scale: float = 1.0
    safety_confirmation: bool = True
    voice_enabled: bool = True
    auto_language_detection: bool = True
    whisper_model: str = "small"
    whisper_device: str = "auto"
    whisper_compute_type: str = "auto"
    tts_provider: str = "edge"
    tts_voice_en: str = "en-IN-NeerjaNeural"
    tts_voice_hi: str = "hi-IN-SwaraNeural"
    tts_voice_te: str = "te-IN-ShrutiNeural"
    speaking_speed: float = 1.0
    wake_word_enabled: bool = False
    wake_word: str = "Hey Ace"
    mock_mode: bool = False

    @classmethod
    def from_env(cls):
        load_dotenv()
        return cls(
            max_steps=int(os.getenv("MAX_AGENT_STEPS", "50")),
            action_delay=float(os.getenv("ACTION_DELAY", "0.2")),
            screenshot_scale=float(os.getenv("SCREENSHOT_SCALE", "1.0")),
            safety_confirmation=os.getenv("SAFETY_CONFIRMATION", "true").lower()=="true",
            voice_enabled=os.getenv("VOICE_ENABLED", "true").lower()=="true",
            auto_language_detection=os.getenv("AUTO_LANGUAGE_DETECTION", "true").lower()=="true",
            whisper_model=os.getenv("WHISPER_MODEL", "small"),
            whisper_device=os.getenv("WHISPER_DEVICE", "auto"),
            whisper_compute_type=os.getenv("WHISPER_COMPUTE_TYPE", "auto"),
            tts_provider=os.getenv("TTS_PROVIDER", "edge"),
            tts_voice_en=os.getenv("TTS_VOICE_EN", "en-IN-NeerjaNeural"),
            tts_voice_hi=os.getenv("TTS_VOICE_HI", "hi-IN-SwaraNeural"),
            tts_voice_te=os.getenv("TTS_VOICE_TE", "te-IN-ShrutiNeural"),
            speaking_speed=float(os.getenv("SPEAKING_SPEED", "1.0")),
            wake_word_enabled=os.getenv("WAKE_WORD_ENABLED", "false").lower()=="true",
            wake_word=os.getenv("WAKE_WORD", "Hey Ace"),
            mock_mode=os.getenv("MOCK_MODE", "false").lower()=="true",
        )
