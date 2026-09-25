from app.services.patient_service import patient_service, PatientService
from app.services.document_service import document_service, DocumentService
from app.services.risk_service import risk_service, RiskAssessmentService
from app.services.referral_service import referral_service, ReferralService
from app.services.communication_service import communication_service, CommunicationService
from app.services.timeline_service import timeline_service, TimelineService
from app.services.voice_service import voice_service, VoiceConsultationService

__all__ = [
    "patient_service",
    "PatientService",
    "document_service",
    "DocumentService",
    "risk_service",
    "RiskAssessmentService",
    "referral_service",
    "ReferralService",
    "communication_service",
    "CommunicationService",
    "timeline_service",
    "TimelineService",
    "voice_service",
    "VoiceConsultationService"
]
