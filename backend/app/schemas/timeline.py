from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from app.schemas.patient import PatientResponse, ObstetricHistoryResponse, MedicalHistoryResponse
from app.schemas.pregnancy import PregnancyResponse
from app.schemas.risk import RiskAssessmentResponse
from app.schemas.referral import ReferralResponse
from app.schemas.delivery import DeliveryResponse
from app.schemas.newborn import NewbornResponse


class TimelineEvent(BaseModel):
    timestamp: datetime
    date: str
    event_type: str  # PREGNANCY_START, ANC_VISIT, OBSERVATION, SYMPTOM, LAB, ULTRASOUND, MEDICATION, DOCUMENT, RISK_ASSESSMENT, REFERRAL, DELIVERY, POSTPARTUM, NEWBORN_VISIT
    title: str
    summary: str
    details: Dict[str, Any] = {}
    severity_or_status: Optional[str] = None


class PatientTimelineResponse(BaseModel):
    patient_id: str
    patient_name: str
    total_events: int
    timeline: List[TimelineEvent]


class PatientSummaryResponse(BaseModel):
    patient_id: str
    demographics: PatientResponse
    obstetric_history: Optional[ObstetricHistoryResponse] = None
    medical_history: Optional[MedicalHistoryResponse] = None
    current_pregnancy: Optional[PregnancyResponse] = None
    gestational_age_weeks: Optional[float] = None
    latest_observations: Dict[str, Any] = {}
    recent_symptoms: List[Dict[str, Any]] = []
    recent_labs: List[Dict[str, Any]] = []
    latest_risk_assessment: Optional[RiskAssessmentResponse] = None
    active_referrals: List[ReferralResponse] = []
    verified_documents_count: int = 0
    delivery_status: Optional[str] = None
    delivery_record: Optional[DeliveryResponse] = None
    newborns: List[NewbornResponse] = []
    latest_postpartum_visit: Optional[Dict[str, Any]] = None
