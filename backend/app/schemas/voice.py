from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AudioTranscriptionRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64-encoded audio data (WAV, MP3, OGG, WebM)")
    audio_format: str = Field("wav", description="Audio format/container: wav, mp3, ogg, webm")
    source_language: Optional[str] = Field(None, description="Optional ISO language code or auto-detect")


class AudioTranscriptionResponse(BaseModel):
    text: str
    detected_language: str
    language_confidence: float
    duration_seconds: float
    model_name: str


class VoiceSynthesizeRequest(BaseModel):
    text: str = Field(..., description="Text to synthesize into natural speech")
    language: str = Field("en", description="Target ISO language code: en, hi, ta, te, kn, bn, mr, es, fr, sw")
    voice_gender: str = Field("female", description="Voice gender: female (soothing maternal tone) or male")
    speaking_rate: float = Field(1.0, description="Speed of speech (0.8 - 1.2)")


class VoiceSynthesizeResponse(BaseModel):
    audio_base64: str
    audio_format: str = "audio/wav"
    language: str
    duration_seconds: float
    sample_rate: int


class VoiceConsultationRequest(BaseModel):
    patient_id: Optional[str] = Field(None, description="Optional patient ID to ground response in longitudinal history")
    pregnancy_id: Optional[str] = Field(None, description="Optional pregnancy ID for trimester-specific clinical context")
    audio_base64: Optional[str] = Field(None, description="Audio recording of patient/health worker question")
    text_query: Optional[str] = Field(None, description="Or text question if voice already transcribed")
    input_language: Optional[str] = Field(None, description="Preferred language code (auto-detected if None)")
    output_audio: bool = Field(True, description="Whether to return synthesized voice response")


class ClinicalFindingItem(BaseModel):
    symptom_or_sign: str
    concern_level: str  # ROUTINE, MONITOR, CLINICAL_REVIEW_RECOMMENDED, URGENT_EMERGENCY
    recommendation: str


class VoiceConsultationResponse(BaseModel):
    transcribed_query: str
    detected_language: str
    medical_advice_text: str
    patient_friendly_text: str
    clinical_review_recommended: bool
    potential_risk_flags: List[str] = []
    clinical_findings: List[ClinicalFindingItem] = []
    suggested_actions: List[str] = []
    audio_response_base64: Optional[str] = None
    audio_format: Optional[str] = "audio/wav"
    model_pipeline_trace: Dict[str, Any] = {}
