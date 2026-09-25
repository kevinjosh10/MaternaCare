from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.ai_models.asr_model import asr_engine, LANGUAGE_NAMES
from app.ai_models.tts_model import tts_engine
from app.schemas.voice import (
    AudioTranscriptionRequest, AudioTranscriptionResponse,
    VoiceSynthesizeRequest, VoiceSynthesizeResponse,
    VoiceConsultationRequest, VoiceConsultationResponse
)
from app.services.voice_service import voice_service

router = APIRouter(prefix="/voice", tags=["Multilingual Voice-to-Voice AI Pipeline"])


@router.get("/languages", response_model=Dict[str, str])
def list_supported_voice_languages():
    """
    Returns list of all supported speech recognition and synthesis languages.
    """
    return LANGUAGE_NAMES


@router.post("/transcribe", response_model=AudioTranscriptionResponse)
def transcribe_voice_audio(
    req: AudioTranscriptionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Multilingual Automatic Speech Recognition (ASR):
    Recognizes all kinds of languages through voice and converts to text.
    """
    try:
        res = asr_engine.transcribe(
            audio_base64=req.audio_base64,
            audio_format=req.audio_format,
            target_language=req.source_language
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Voice transcription failed: {str(e)}")


@router.post("/synthesize", response_model=VoiceSynthesizeResponse)
def synthesize_voice_speech(
    req: VoiceSynthesizeRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Multilingual Text-to-Speech (TTS):
    Converts clinical text into natural, empathetic voice audio in the specified language.
    """
    try:
        res = tts_engine.synthesize(
            text=req.text,
            language=req.language,
            voice_gender=req.voice_gender,
            speaking_rate=req.speaking_rate
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Voice synthesis failed: {str(e)}")


@router.post("/consult", response_model=VoiceConsultationResponse)
def voice_consultation(
    req: VoiceConsultationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Multi-Model Voice-to-Voice Pregnancy Intelligence Pipeline:
    1. ASR Model: Listens to voice in any language and transcribes it.
    2. Medical Knowledge Model: Evaluates symptoms against maternal protocols and patient history.
    3. Clinical Guardrail: Flags concerning patterns for human review without claiming diagnosis.
    4. TTS Model: Converts plain-language explanation into voice in the patient's language.
    5. Returns audio response + structured clinical findings.
    """
    try:
        return voice_service.process_consultation(
            db=db,
            request=req,
            user_id=current_user.id,
            role=current_user.role
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice consultation failed: {str(e)}")
