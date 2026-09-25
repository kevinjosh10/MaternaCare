from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ObservationBase(BaseModel):
    patient_id: str
    pregnancy_id: Optional[str] = None
    newborn_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    observation_type: str = Field(..., example="systolic_bp")
    value: float = Field(..., example=120.0)
    unit: str = Field(..., example="mmHg")
    source: str = Field("CLINICAL_VISIT", example="CLINICAL_VISIT")
    verified: bool = Field(False, example=True)
    recorded_by: Optional[str] = None


class ObservationCreate(ObservationBase):
    pass


class ObservationResponse(ObservationBase):
    observation_id: str
    created_at: datetime

    class Config:
        from_attributes = True
