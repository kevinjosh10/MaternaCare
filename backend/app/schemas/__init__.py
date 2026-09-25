from app.schemas.auth import Token, TokenPayload, LoginRequest, UserCreate, UserResponse
from app.schemas.patient import (
    PatientCreate, PatientUpdate, PatientResponse,
    ObstetricHistoryCreate, ObstetricHistoryResponse,
    MedicalHistoryCreate, MedicalHistoryResponse,
    EmergencyContactSchema
)
from app.schemas.pregnancy import PregnancyCreate, PregnancyUpdate, PregnancyResponse
from app.schemas.visit import AntenatalVisitCreate, AntenatalVisitResponse
from app.schemas.observation import ObservationCreate, ObservationResponse
from app.schemas.symptom import SymptomCreate, SymptomResponse
from app.schemas.lab import LabResultCreate, LabResultResponse, LabVerificationUpdate
from app.schemas.ultrasound import UltrasoundCreate, UltrasoundResponse
from app.schemas.medication import (
    MedicationCreate, MedicationResponse,
    SupplementCreate, SupplementResponse,
    VaccinationCreate, VaccinationResponse
)
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentVerifyRequest
from app.schemas.delivery import DeliveryCreate, DeliveryResponse
from app.schemas.newborn import NewbornCreate, NewbornResponse, NewbornVisitCreate, NewbornVisitResponse
from app.schemas.postpartum import PostpartumVisitCreate, PostpartumVisitResponse
from app.schemas.risk import RiskAssessmentCreate, RiskAssessmentResponse, ExplanationFeatureResponse, ClinicianReviewUpdate
from app.schemas.facility import FacilityCreate, FacilityResponse
from app.schemas.referral import ReferralCreate, ReferralStatusUpdate, ReferralResponse
from app.schemas.communication import CommunicationCreate, CommunicationResponse
from app.schemas.timeline import TimelineEvent, PatientTimelineResponse, PatientSummaryResponse
from app.schemas.voice import (
    AudioTranscriptionRequest, AudioTranscriptionResponse,
    VoiceSynthesizeRequest, VoiceSynthesizeResponse,
    VoiceConsultationRequest, VoiceConsultationResponse
)
