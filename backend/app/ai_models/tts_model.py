import base64
import io
import re
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# 50 verified languages supported natively by Google Text-to-Speech (gTTS)
GTTS_LANG_MAP = {
    "en": "en", "hi": "hi", "ta": "ta", "te": "te", "bn": "bn", "ml": "ml",
    "mr": "mr", "gu": "gu", "kn": "kn", "pa": "pa", "ur": "ur", "ne": "ne",
    "si": "si", "my": "my", "es": "es", "fr": "fr", "de": "de", "zh": "zh-CN",
    "ar": "ar", "ru": "ru", "ja": "ja", "pt": "pt", "it": "it", "ko": "ko",
    "tr": "tr", "nl": "nl", "vi": "vi", "pl": "pl", "uk": "uk", "th": "th",
    "id": "id", "ms": "ms", "tl": "tl", "iw": "iw", "sv": "sv", "no": "no",
    "da": "da", "fi": "fi", "cs": "cs", "el": "el", "hu": "hu", "ro": "ro",
    "sk": "sk", "bg": "bg", "hr": "hr", "sr": "sr", "lt": "lt", "lv": "lv",
    "et": "et", "sw": "sw"
}


class MultilingualTTSModel:
    """
    Multilingual Text-to-Speech (TTS) Voice Synthesis Engine using gTTS.
    Converts clinical model output into authentic human voice across 50 languages.
    """

    def __init__(self, engine_name: str = "Google-Multilingual-TTS-50"):
        self.engine_name = engine_name
        logger.info(f"Initialized Multilingual TTS Engine with 50 verified languages: {self.engine_name}")

    def normalize_clinical_text(self, text: str) -> str:
        """
        Normalize clinical abbreviations and symbols for natural speech phonetics.
        """
        clean = re.sub(r"[\*#_`>\[\]]", "", text)
        clean = re.sub(r"(?i)\bBP\s*(\d{2,3})/(\d{2,3})\b", r"blood pressure \1 over \2", clean)
        clean = re.sub(r"(?i)\bHb\s*(\d+(\.\d+)?)\b", r"hemoglobin \1", clean)
        clean = re.sub(r"\s+", " ", clean).strip()
        return clean

    def synthesize(
        self,
        text: str,
        language: str = "en",
        voice_gender: str = "female",
        speaking_rate: float = 1.0
    ) -> Dict[str, Any]:
        """
        Synthesizes authentic human speech in any of the 50 requested languages using gTTS.
        """
        normalized_text = self.normalize_clinical_text(text)
        
        # Limit text length for TTS to prevent excessive processing time
        if len(normalized_text) > 400:
            sentences = re.split(r'(?<=[.!?।])\s+', normalized_text)
            normalized_text = " ".join(sentences[:3])

        clean_lang = language.lower().split("-")[0].strip()
        target_gtts_lang = GTTS_LANG_MAP.get(clean_lang, "en")

        try:
            from gtts import gTTS
            tts = gTTS(text=normalized_text, lang=target_gtts_lang, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            audio_bytes = fp.read()
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
            
            return {
                "engine": self.engine_name,
                "language": target_gtts_lang,
                "format": "audio/mp3",
                "audio_base64": audio_b64,
                "duration_seconds": round(len(audio_bytes) / 16000.0, 2),
                "sample_rate": 24000,
                "synthesized_text": normalized_text
            }
        except Exception as e:
            logger.error(f"gTTS Synthesis error for language {target_gtts_lang}: {e}")
            return {
                "engine": self.engine_name,
                "language": target_gtts_lang,
                "format": None,
                "audio_base64": None,
                "duration_seconds": 0,
                "sample_rate": 0,
                "synthesized_text": normalized_text,
                "error": str(e)
            }


tts_engine = MultilingualTTSModel()
