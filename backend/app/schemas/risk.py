from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ExplanationFeatureResponse(BaseModel):
    id: str
    feature: str
    feature_value: str
    contribution: float  # SHAP value
    direction: str  # INCREASE_RISK or DECREASE_RISK
    rank: int

    class Config:
        from_attributes = True


class RiskAssessmentBase(BaseModel):
    patient_id: str
    pregnancy_id: Optional[str] = None
    newborn_id: Optional[str] = None
    model_version: str = "maternacare-risk-engine-v1.0"
    risk_category: str = Field(..., example="PREECLAMPSIA")
    risk_score: float = Field(..., ge=0.0, le=1.0, example=0.78)
    risk_level: str = Field(..., example="HIGH")  # LOW, MODERATE, HIGH, CRITICAL
    input_snapshot: Dict[str, Any] = {}
    contributing_factors: List[str] = []
    trend_features: Dict[str, Any] = {}
    explanation: str = Field(
        "Potentially concerning pattern detected — clinical review recommended.",
        example="Potentially concerning pattern detected — clinical review recommended."
    )
    clinician_review_status: str = Field("PENDING_REVIEW", example="PENDING_REVIEW")
    clinician_notes: Optional[str] = None


class RiskAssessmentCreate(RiskAssessmentBase):
    explanations: Optional[List[Dict[str, Any]]] = []


class ClinicianReviewUpdate(BaseModel):
    clinician_review_status: str = Field(..., example="REVIEWED_AGREED")  # REVIEWED_AGREED, REVIEWED_DISAGREED, OVERRIDDEN
    clinician_notes: str = Field(..., example="Patient scheduled for urgent Doppler ultrasound and lab panel.")


class RiskAssessmentResponse(RiskAssessmentBase):
    assessment_id: str
    timestamp: datetime
    created_at: datetime
    explanations: List[ExplanationFeatureResponse] = []

    class Config:
        from_attributes = True
