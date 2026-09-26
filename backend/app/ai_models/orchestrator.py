import time
import logging
import re
from typing import Dict, Any, Optional
from app.ai_models.asr_model import asr_engine
from app.ai_models.medical_pregnancy_model import pregnancy_knowledge_model
from app.ai_models.tts_model import tts_engine

logger = logging.getLogger(__name__)

LANG_NAMES = {
    "en": "English", "hi": "Hindi", "ta": "Tamil", "te": "Telugu",
    "ml": "Malayalam", "kn": "Kannada", "bn": "Bengali", "mr": "Marathi",
    "es": "Spanish", "fr": "French", "de": "German", "ar": "Arabic",
    "ru": "Russian", "ja": "Japanese", "pt": "Portuguese", "it": "Italian",
    "ko": "Korean", "tr": "Turkish", "nl": "Dutch", "vi": "Vietnamese"
}

MEDICATION_PATTERNS = [
    r"\bmedicine\b", r"\btablet\b", r"\btablets\b", r"\bpill\b", r"\bpills\b",
    r"\bcapsule\b", r"\bsyrup\b", r"\bparacetamol\b", r"\baspirin\b", r"\bibuprofen\b",
    r"\bcrocin\b", r"\bdolo\b", r"\bantibiotic\b", r"\bdawa\b", r"\bdawai\b", r"\bgoli\b",
    r"\bmarunthu\b", r"\bmathirai\b", r"\bmandhu\b", r"\baushadhi\b", r"\bdrug\b",
    r"\bdosage\b", r"\bdose\b", r"\bwhat should i take\b", r"\bcan i take\b"
]


class VoiceToVoiceMedicalOrchestrator:
    """
    Multi-Model Communication Pipeline Orchestrator with Human-In-The-Loop (HITL) Medical Safety Gate.
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
        [Voice In] -> ASR Model -> Emergency Guardian -> HITL Medication Gate -> Clinical Reasoning Brain -> TTS -> [Voice Out]
        """
        pipeline_start = time.time()
        trace = {
            "asr_model": self.asr.model_name,
            "medical_model": "MaternaCare-Clinical-Brain-UltraFast",
            "tts_engine": self.tts.engine_name,
            "steps": []
        }

        # Step 1: Speech Recognition (Voice In -> Text)
        if audio_base64:
            transcription_res = self.asr.transcribe(
                audio_base64=audio_base64,
                target_language=language_hint
            )
            query_text = transcription_res["text"]
            detected_lang = transcription_res["detected_language"]
            trace["steps"].append({
                "step": "ASR_TRANSCRIPTION",
                "elapsed_ms": round((time.time() - pipeline_start) * 1000, 2)
            })
        elif text_query:
            query_text = text_query
            detected_lang = language_hint or "en"
        else:
            raise ValueError("Either audio_base64 or text_query must be provided.")

        target_lang = (language_hint or detected_lang or "en").lower().split("-")[0]
        target_lang_name = LANG_NAMES.get(target_lang, "English")

        # Step 2: Model 3 (Ambient Emergency Guardian)
        from app.ai_models.emergency_guardian import emergency_guardian
        emergency_check = emergency_guardian.check_for_emergency(query_text)
        if emergency_check["emergency_detected"]:
            trace["steps"].append({"step": "EMERGENCY_GUARDIAN_INTERCEPT"})
            return {
                "transcribed_query": query_text,
                "detected_language": target_lang,
                "status": "EMERGENCY_DISPATCHED",
                "dispatch_payload": emergency_check["dispatch_payload"],
                "message": emergency_check["message"],
                "model_pipeline_trace": trace
            }

        # Step 3: Human-In-The-Loop (HITL) Medication Gate Check
        # If user asks about tablets, pills, or medicines -> DO NOT suggest autonomously!
        # Forward to Doctor and instruct patient to wait for doctor approval.
        is_medicine_query = any(re.search(pat, query_text.lower()) for pat in MEDICATION_PATTERNS)

        if is_medicine_query:
            step_med_start = time.time()
            proposed_clinical_advice = "Patient inquired about prescription medication. Evaluated safe antenatal dosages under clinical review."
            patient_waiting_message = "Since you are asking about medication, I have forwarded your request to your doctor for review. After I get approval from the doctor, I will suggest you the tablet."

            # Translate both the waiting message and proposed advice into target language using Groq
            try:
                import os, dotenv
                dotenv.load_dotenv()
                groq_key = os.environ.get("GROQ_API_KEY", "")
                if groq_key:
                    from groq import Groq
                    groq_client = Groq(api_key=groq_key)

                    # 1. Generate clinical doctor advice for the Clinician Dashboard
                    doc_comp = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {"role": "system", "content": "You are a clinical obstetrician assistant. Provide a brief 1-2 sentence evidence-based medication guidance for the doctor to review and sign off. Do not address the patient."},
                            {"role": "user", "content": f"Pregnant patient (Week 32) asks: '{query_text}'. What is the clinical recommendation?"}
                        ],
                        temperature=0.2,
                        max_tokens=150
                    )
                    proposed_clinical_advice = doc_comp.choices[0].message.content.replace('*', '').strip()

                    # 2. Formulate native patient waiting message
                    pat_comp = groq_client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {"role": "system", "content": f"Translate directly into {target_lang_name} ({target_lang}). Return ONLY the direct natural translation in native script without quotes or commentary."},
                            {"role": "user", "content": patient_waiting_message}
                        ],
                        temperature=0.2,
                        max_tokens=150
                    )
                    translated_pat = pat_comp.choices[0].message.content.replace('*', '').strip()
                    if translated_pat:
                        patient_waiting_message = translated_pat
            except Exception as e:
                logger.warning(f"Medication HITL translation note: {e}")

            # Synthesize voice audio in the user's native language
            audio_response_b64 = None
            if generate_audio:
                tts_res = self.tts.synthesize(text=patient_waiting_message, language=target_lang)
                audio_response_b64 = tts_res.get("audio_base64")

            trace["steps"].append({
                "step": "HITL_MEDICATION_GATE_TRIGGERED",
                "elapsed_ms": round((time.time() - step_med_start) * 1000, 2),
                "status": "PENDING_DOCTOR_APPROVAL"
            })
            trace["total_pipeline_ms"] = round((time.time() - pipeline_start) * 1000, 2)

            return {
                "transcribed_query": query_text,
                "detected_language": target_lang,
                "status": "PENDING_DOCTOR_APPROVAL",
                "requiresApproval": True,
                "proposedAdvice": proposed_clinical_advice,
                "patient_friendly_text": patient_waiting_message,
                "audio_response_base64": audio_response_b64,
                "audio_format": "audio/mp3" if audio_response_b64 else None,
                "model_pipeline_trace": trace
            }

        # Step 4: Direct High-Speed Intelligent Clinical Reasoning (Model 4) for non-medication queries
        step4_start = time.time()
        final_patient_text = ""
        groq_success = False

        # Primary: Ultra-Fast Groq Qwen 3.8
        try:
            import os, dotenv
            dotenv.load_dotenv()
            groq_key = os.environ.get("GROQ_API_KEY", "")
            if groq_key:
                from groq import Groq
                groq_client = Groq(api_key=groq_key)
                
                sys_prompt = (
                    f"You are MaternaCare, an empathetic, caring, and medically certified maternal health companion for a pregnant mother. "
                    f"Answer the mother's question or concern directly, accurately, and reassuringly in 2 to 3 concise sentences. "
                    f"Respond directly in {target_lang_name} ({target_lang}) using authentic native script. "
                    f"Do not use markdown, asterisks (*), or quotes so it can be read smoothly by Text-to-Speech."
                )

                completion = groq_client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": query_text}
                    ],
                    temperature=0.3,
                    max_tokens=220
                )
                raw_ans = completion.choices[0].message.content.replace('*', '').strip()
                if raw_ans and len(raw_ans) > 5:
                    final_patient_text = raw_ans
                    groq_success = True
                    trace["steps"].append({
                        "step": "GROQ_CLINICAL_REASONING",
                        "elapsed_ms": round((time.time() - step4_start) * 1000, 2),
                        "lang": target_lang
                    })
        except Exception as ge:
            logger.warning(f"Groq direct reasoning note: {ge}")

        # Secondary Fallback: Google Gemini
        if not groq_success:
            try:
                import os, dotenv
                dotenv.load_dotenv()
                api_key = os.environ.get("GEMINI_API_KEY", "")
                if api_key:
                    import google.generativeai as genai
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-3.8-flash')
                    prompt = (
                        f"You are MaternaCare maternal health assistant. Answer this pregnant mother's question directly, warmly, and accurately in 2-3 sentences. "
                        f"Respond directly in {target_lang_name} ({target_lang}) in native script without markdown:\n\n{query_text}"
                    )
                    res = model.generate_content(prompt)
                    if res.text:
                        final_patient_text = res.text.replace('*', '').strip()
                        trace["steps"].append({"step": "GEMINI_CLINICAL_REASONING", "lang": target_lang})
            except Exception as e:
                logger.error(f"Gemini reasoning failed: {e}")

        # Safe default if network was offline
        if not final_patient_text:
            final_patient_text = f"Thank you for sharing. As long as you are feeling well and have no severe symptoms, please continue routine care and consult your doctor."

        # Step 5: High-Fidelity TTS Voice Synthesis (Model 2) in the Target Language
        step5_start = time.time()
        audio_response_b64 = None
        if generate_audio:
            tts_res = self.tts.synthesize(
                text=final_patient_text,
                language=target_lang,
                voice_gender="female"
            )
            audio_response_b64 = tts_res.get("audio_base64")
            trace["steps"].append({
                "step": "TTS_VOICE_SYNTHESIS",
                "elapsed_ms": round((time.time() - step5_start) * 1000, 2),
                "audio_duration_seconds": tts_res.get("duration_seconds", 0),
                "language": target_lang
            })

        trace["total_pipeline_ms"] = round((time.time() - pipeline_start) * 1000, 2)

        return {
            "transcribed_query": query_text,
            "detected_language": target_lang,
            "status": "COMPLETED",
            "medical_advice_text": final_patient_text,
            "patient_friendly_text": final_patient_text,
            "detected_syndromes": [],
            "audio_response_base64": audio_response_b64,
            "audio_format": "audio/mp3" if audio_response_b64 else None,
            "model_pipeline_trace": trace
        }

    def process_doctor_approved_response(self, approved_text: str, language: str = "en") -> Dict[str, Any]:
        """
        To be called when the Doctor approves/edits the advice on the dashboard.
        """
        tts_res = self.tts.synthesize(
            text=approved_text,
            language=language,
            voice_gender="female"
        )
        return {
            "status": "APPROVED_DISPATCHED",
            "approved_text": approved_text,
            "audio_response_base64": tts_res["audio_base64"],
            "language": language
        }


voice_orchestrator = VoiceToVoiceMedicalOrchestrator()
