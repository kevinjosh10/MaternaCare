from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class SymptomBase(BaseModel):
    patient_id: str
    pregnancy_id: Optional[str] = None
    newborn_id: Optional[str] = None
    date_time: datetime = Field(default_factory=datetime.utcnow)
    symptom_type: str = Field(..., example="HEADACHE")
    severity: str = Field(..., example="MODERATE")  # MILD, MODERATE, SEVERE, CRITICAL
    duration: Optional[str] = Field(None, example="3 hours")
    onset: Optional[str] = Field("GRADUAL", example="GRADUAL")  # SUDDEN, GRADUAL
    frequency: Optional[str] = Field("INTERMITTENT", example="INTERMITTENT")
    associated_symptoms: List[str] = []
    reported_by: Optional[str] = Field("PATIENT", example="PATIENT")
    verified_by: Optional[str] = None


class SymptomCreate(SymptomBase):
    pass


class SymptomResponse(SymptomBase):
    symptom_id: str
    created_at: datetime

    class Config:
        from_attributes = True
