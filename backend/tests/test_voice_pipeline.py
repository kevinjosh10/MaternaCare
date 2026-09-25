import base64
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_voice_pipeline_and_multi_model_communication():
    # 1. Test Supported Languages Endpoint
    lang_res = client.get("/api/v1/voice/languages")
    assert lang_res.status_code == 200
    languages = lang_res.json()
    assert "hi" in languages
    assert "en" in languages
    assert "ta" in languages

    # 2. Test Multilingual Speech Synthesis (TTS Model)
    tts_payload = {
        "text": "नमस्ते। आपकी गर्भावस्था का 28वां हफ्ता चल रहा है। कृपया अपना रक्तचाप नियमित जांचें।",
        "language": "hi",
        "voice_gender": "female",
        "speaking_rate": 1.0
    }
    tts_res = client.post("/api/v1/voice/synthesize", json=tts_payload)
    assert tts_res.status_code == 200
    tts_data = tts_res.json()
    assert "audio_base64" in tts_data
    assert tts_data["audio_format"] == "audio/wav"
    assert tts_data["sample_rate"] == 16000

    # 3. Test Speech Recognition (ASR Model)
    # Use the generated audio from TTS to test ASR
    sample_audio_b64 = tts_data["audio_base64"]
    asr_res = client.post("/api/v1/voice/transcribe", json={
        "audio_base64": sample_audio_b64,
        "audio_format": "wav",
        "source_language": "hi"
    })
    assert asr_res.status_code == 200
    asr_data = asr_res.json()
    assert "text" in asr_data
    assert asr_data["detected_language"] == "hi"

    # 4. Test Multi-Model End-to-End Voice Consultation Pipeline:
    # Voice In -> ASR -> Clinical Pregnancy Model -> TTS -> Voice Out
    consult_payload = {
        "text_query": "मुझे तेज सिरदर्द है और आंखों के आगे धुंधला दिख रहा है",
        "input_language": "hi",
        "output_audio": True
    }
    consult_res = client.post("/api/v1/voice/consult", json=consult_payload)
    assert consult_res.status_code == 200
    consult_data = consult_res.json()

    # Clinical Guardrail Checks:
    # 1. Clinical review must be recommended for preeclampsia danger signs
    assert consult_data["clinical_review_recommended"] is True
    assert "PREECLAMPSIA" in consult_data["potential_risk_flags"]
    # 2. Medical text must follow mandatory clinical guardrail
    assert "Potentially concerning pattern detected — clinical review recommended." in consult_data["medical_advice_text"]
    # 3. Patient-friendly text must be in Hindi
    assert len(consult_data["patient_friendly_text"]) > 20
    # 4. Must return synthesized speech audio in Base64
    assert consult_data["audio_response_base64"] is not None
    assert consult_data["audio_format"] == "audio/wav"
    # 5. Multi-model pipeline trace must show all models executed
    trace = consult_data["model_pipeline_trace"]
    assert "asr_model" in trace
    assert "medical_model" in trace
    assert "tts_engine" in trace
    assert trace["total_pipeline_ms"] > 0
