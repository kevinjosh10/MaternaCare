from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ReferralBase(BaseModel):
    patient_id: str
    pregnancy_id: Optional[str] = None
    newborn_id: Optional[str] = None
    created_by: str = Field(..., example="Dr. Priya (CHC Medical Officer)")
    reason: str = Field(..., example="Severe Preeclampsia requiring tertiary maternal & neonatal ICU backup")
    risk_level: str = Field(..., example="CRITICAL")  # LOW, MODERATE, HIGH, CRITICAL
    clinical_summary: str = Field(
        ...,
        example="G2P1 with gestational age 34 weeks presenting with BP 160/110 mmHg, 3+ proteinuria, severe headache."
    )
    source_facility: str = Field(..., example="Community Health Centre Arajiline")
    destination_facility: Optional[str] = Field(None, example="District Women's Hospital Varanasi")
    transport_status: str = Field("NONE", example="NONE")
    referral_status: str = Field("CREATED", example="CREATED")
    notes: Optional[str] = None


class ReferralCreate(ReferralBase):
    pass


class ReferralStatusUpdate(BaseModel):
    referral_status: str = Field(..., example="ACKNOWLEDGED")
    # CREATED, CLINICIAN_REVIEW, FACILITY_SELECTED, REFERRAL_SENT, ACKNOWLEDGED,
    # TRANSFER_IN_PROGRESS, ARRIVED, COMPLETED, CANCELLED
    transport_status: Optional[str] = None
    destination_facility: Optional[str] = None
    notes: Optional[str] = None


class ReferralResponse(ReferralBase):
    referral_id: str
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    transfer_started_at: Optional[datetime] = None
    arrival_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
