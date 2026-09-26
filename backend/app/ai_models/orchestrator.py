import time
import logging
from typing import Dict, Any, Optional
from app.ai_models.asr_model import asr_engine
from app.ai_models.medical_pregnancy_model import pregnancy_knowledge_model
from app.ai_models.tts_model import tts_engine

logger = logging.getLogger(__name__)


class VoiceToVoiceMedicalOrchestrator:
    """
    Multi-Model Communication Pipeline Orchestrator.
    Seamlessly manages communication between:
    1. Multilingual Speech Recognition (ASR) Model
    2. Medical Pregnancy Knowledge Intelligence Model
    3. Multilingual Text-to-Speech (TTS) Voice Synthesis Model
    """

    def __init__(self):
        self.asr = asr_engine
        self.medical_kg = pregnancy_knowledge_model
        self.tts = tts_engine
        logger.info("Initialized Voice-to-Voice Multi-Model Medical Orchestrator")

    def process_consultation(
        self,
        audio_base64: Optional[str] = None,
        text_query: Optional[str] = None,
        language_hint: Optional[str] = None,
        patient_context: Optional[Dict[str, Any]] = None,
        generate_audio: bool = True
    ) -> Dict[str, Any]:
        """
        End-to-End Orchestrated Pipeline:
        [Voice In] -> ASR Model -> Medical Knowledge Engine -> TTS Model -> [Voice Out]
        """
        pipeline_start = time.time()
        trace = {
            "asr_model": self.asr.model_name,
            "medical_model": "MaternaCare-Clinical-Brain-v2", # Updated to actual Medical Brain
            "tts_engine": self.tts.engine_name,
            "steps": []
        }

        # Step 1: Speech Recognition (Voice In -> Text)
        step1_start = time.time()
        if audio_base64:
            transcription_res = self.asr.transcribe(
                audio_base64=audio_base64,
                target_language=language_hint
            )
            query_text = transcription_res["text"]
            detected_lang = transcription_res["detected_language"]
            trace["steps"].append({
                "step": "ASR_TRANSCRIPTION",
                "elapsed_ms": round((time.time() - step1_start) * 1000, 2),
                "detected_language": detected_lang,
                "confidence": transcription_res["language_confidence"]
            })
        elif text_query:
            query_text = text_query
            detected_lang = language_hint or "en"
            trace["steps"].append({
                "step": "DIRECT_TEXT_INPUT",
                "elapsed_ms": 0.1,
                "language": detected_lang
            })
        else:
            raise ValueError("Either audio_base64 or text_query must be provided.")

        # --- NEW: Model 3 (Ambient Emergency Guardian) ---
        from app.ai_models.emergency_guardian import emergency_guardian
        emergency_check = emergency_guardian.check_for_emergency(query_text)
        if emergency_check["emergency_detected"]:
            trace["steps"].append({"step": "EMERGENCY_GUARDIAN_INTERCEPT"})
            return {
                "transcribed_query": query_text,
                "detected_language": detected_lang,
                "status": "EMERGENCY_DISPATCHED",
                "dispatch_payload": emergency_check["dispatch_payload"],
                "message": emergency_check["message"],
                "model_pipeline_trace": trace
            }

        # Step 2: Clinical Medical Reasoning (Main Medical Brain - Model 4)
        step2_start = time.time()
        from app.medical_brain.brain_engine import medical_brain, PatientClinicalContext
        
        # Build context from request (fallback to defaults if not provided)
        context = PatientClinicalContext(
            patient_id=patient_context.get("patient_id", "P-UNKNOWN") if patient_context else "P-UNKNOWN",
            age=patient_context.get("age", 25) if patient_context else 25,
            gestational_weeks=patient_context.get("gestational_weeks", 20.0) if patient_context else 20.0,
            symptoms=[query_text], # Pass the user's query as a symptom/input
            current_query_text=query_text, # Explicitly pass it for NLP evaluation
            test_results=patient_context.get("test_results", []) if patient_context else [],
            past_history=patient_context.get("past_history", None) if patient_context else None
        )
        
        clinical_analysis = medical_brain.analyze_patient(context)
        
        trace["steps"].append({
            "step": "MEDICAL_BRAIN_EVALUATION",
            "elapsed_ms": round((time.time() - step2_start) * 1000, 2),
            "hitl_status": clinical_analysis.hitl_approval.status,
            "syndromes_detected": clinical_analysis.detected_syndromes
        })

        # Step 3: HITL Gate Check
        if clinical_analysis.hitl_approval.status == "PENDING_APPROVAL":
            trace["steps"].append({
                "step": "HITL_HALT",
                "reason": clinical_analysis.hitl_approval.trigger_reasons
            })
            
            from app.medical_brain.microservice import PENDING_APPROVALS_DB
            PENDING_APPROVALS_DB[clinical_analysis.analysis_id] = clinical_analysis
            
            return {
                "transcribed_query": query_text,
                "detected_language": detected_lang,
                "status": "PENDING_DOCTOR_APPROVAL",
                "analysis_id": clinical_analysis.analysis_id,
                "triggers": clinical_analysis.hitl_approval.trigger_reasons,
                "message": "Consultation requires doctor approval before responding to patient.",
                "model_pipeline_trace": trace
            }

        # Step 4: Multi-Lingual Translation Layer (Model 1) FIRST!
        final_patient_text = clinical_analysis.patient_friendly_english
        target_lang = language_hint or detected_lang or "en"
        
        if target_lang and target_lang.lower() not in ["en", "en-us", "en-in", "english"]:
            try:
                import os, dotenv
                dotenv.load_dotenv()
                api_key = os.environ.get("GEMINI_API_KEY", "")
                if api_key:
                    import google.generativeai as genai
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-3.8-flash')
                    prompt = f"Translate the following medical advice for a pregnant woman directly and naturally into the language with code '{target_lang}'. Do not add explanations, provide ONLY the natural translation in the target language's native script:\n\n{final_patient_text}"
                    res = model.generate_content(prompt)
                    if res.text:
                        final_patient_text = res.text.replace('*', '').strip()
                        trace["steps"].append({"step": "GEMINI_LANGUAGE_TRANSLATION", "target_lang": target_lang})
            except Exception as e:
                logger.error(f"Translation to {target_lang} failed: {e}")

        # Step 5: High-Fidelity TTS Voice Synthesis (Model 2) in the Target Language!
        step5_start = time.time()
        audio_response_b64 = None
        if generate_audio:
            tts_res = self.tts.synthesize(
                text=final_patient_text,
                language=target_lang,
                voice_gender="female"
            )
            audio_response_b64 = tts_res["audio_base64"]
            trace["steps"].append({
                "step": "TTS_VOICE_SYNTHESIS",
                "elapsed_ms": round((time.time() - step5_start) * 1000, 2),
                "audio_duration_seconds": tts_res["duration_seconds"],
                "sample_rate": tts_res["sample_rate"],
                "language": target_lang
            })

        trace["total_pipeline_ms"] = round((time.time() - pipeline_start) * 1000, 2)

        return {
            "transcribed_query": query_text,
            "detected_language": target_lang,
            "status": "COMPLETED",
            "medical_advice_text": clinical_analysis.medical_advice_english,
            "patient_friendly_text": final_patient_text,
            "detected_syndromes": clinical_analysis.detected_syndromes,
            "audio_response_base64": audio_response_b64,
            "audio_format": "audio/mp3" if audio_response_b64 else None,
            "model_pipeline_trace": trace
        }

    def process_doctor_approved_response(self, approved_text: str, language: str = "en") -> Dict[str, Any]:
        """
        To be called when the Doctor approves/edits the advice on the dashboard.
        This sends the approved text directly to the Translation (Model 1) and TTS (Model 2) pipeline.
        """
        step_start = time.time()
        
        # Step 1: Synthesize Voice for the Patient
        tts_res = self.tts.synthesize(
            text=approved_text,
            language=language,
            voice_gender="female"
        )
        
        return {
            "status": "AUDIO_GENERATED_POST_APPROVAL",
            "spoken_text": approved_text,
            "language": language,
            "audio_response_base64": tts_res["audio_base64"],
            "audio_format": "audio/wav",
            "elapsed_ms": round((time.time() - step_start) * 1000, 2)
        }


# Singleton pipeline orchestrator
voice_orchestrator = VoiceToVoiceMedicalOrchestrator()
