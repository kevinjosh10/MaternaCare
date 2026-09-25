from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.ai_models.orchestrator import voice_orchestrator
from app.models.patient import Patient
from app.models.pregnancy import Pregnancy
from app.models.history import ObstetricHistory
from app.models.symptom import Symptom
from app.models.audit import AuditLog
from app.schemas.voice import VoiceConsultationRequest, VoiceConsultationResponse


class VoiceConsultationService:

    @staticmethod
    def process_consultation(
        db: Session,
        request: VoiceConsultationRequest,
        user_id: str = "SYSTEM_VOICE_GATEWAY",
        role: str = "PATIENT_OR_WORKER"
    ) -> VoiceConsultationResponse:
        patient_context = {}
        patient = None

        if request.patient_id:
            patient = db.query(Patient).filter(Patient.patient_id == request.patient_id).first()
            if patient:
                patient_context["patient_name"] = patient.name
                patient_context["preferred_language"] = patient.preferred_language
                # Load obstetric history
                obs_hist = db.query(ObstetricHistory).filter(ObstetricHistory.patient_id == patient.patient_id).first()
                if obs_hist:
                    patient_context["previous_preeclampsia"] = obs_hist.previous_preeclampsia
                    patient_context["previous_c_sections"] = obs_hist.previous_c_sections

                # Load pregnancy
                preg = None
                if request.pregnancy_id:
                    preg = db.query(Pregnancy).filter(Pregnancy.pregnancy_id == request.pregnancy_id).first()
                else:
                    preg = db.query(Pregnancy).filter(
                        Pregnancy.patient_id == patient.patient_id,
                        Pregnancy.status == "ACTIVE"
                    ).order_by(Pregnancy.created_at.desc()).first()

                if preg:
                    patient_context["gestational_age"] = preg.gestational_age
                    patient_context["high_risk_flag"] = preg.high_risk_flag
                    patient_context["high_risk_reason"] = preg.high_risk_reason

        # Run multi-model communication pipeline
        result = voice_orchestrator.process_consultation(
            audio_base64=request.audio_base64,
            text_query=request.text_query,
            language_hint=request.input_language or (patient.preferred_language if patient else None),
            patient_context=patient_context,
            generate_audio=request.output_audio
        )

        # Log audit entry
        audit = AuditLog(
            user_id=user_id,
            role=role,
            action="VOICE_CONSULTATION_PROCESSED",
            patient_id=request.patient_id,
            resource="VOICE_AI_PIPELINE",
            old_value=None,
            new_value={
                "transcribed_query": result["transcribed_query"],
                "detected_language": result["detected_language"],
                "concern_level": result["potential_risk_flags"],
                "clinical_review_recommended": result["clinical_review_recommended"]
            }
        )
        db.add(audit)

        # If a potentially concerning symptom was detected and patient_id is present, log as an unverified Symptom for clinical review
        if request.patient_id and result["clinical_review_recommended"] and result["clinical_findings"]:
            for item in result["clinical_findings"]:
                sym = Symptom(
                    patient_id=request.patient_id,
                    pregnancy_id=request.pregnancy_id,
                    symptom_type=item["symptom_or_sign"].upper(),
                    severity="SEVERE" if item["concern_level"] == "URGENT_EMERGENCY" else "MODERATE",
                    duration="Reported via Voice Agent",
                    onset="SUDDEN" if item["concern_level"] == "URGENT_EMERGENCY" else "GRADUAL",
                    reported_by="PATIENT_VOICE_AGENT",
                    verified_by=None
                )
                db.add(sym)

        db.commit()

        return VoiceConsultationResponse(
            transcribed_query=result["transcribed_query"],
            detected_language=result["detected_language"],
            medical_advice_text=result["medical_advice_text"],
            patient_friendly_text=result["patient_friendly_text"],
            clinical_review_recommended=result["clinical_review_recommended"],
            potential_risk_flags=result["potential_risk_flags"],
            clinical_findings=result["clinical_findings"],
            suggested_actions=result["suggested_actions"],
            audio_response_base64=result["audio_response_base64"],
            audio_format=result["audio_format"],
            model_pipeline_trace=result["model_pipeline_trace"]
        )


voice_service = VoiceConsultationService()
