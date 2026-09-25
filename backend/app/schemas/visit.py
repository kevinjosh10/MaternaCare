from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, Field


class AntenatalVisitBase(BaseModel):
    pregnancy_id: str
    patient_id: str
    visit_date: date
    gestational_age: Optional[float] = Field(None, example=24.0)
    weight: Optional[float] = Field(None, example=62.5)  # kg
    height: Optional[float] = Field(None, example=158.0)  # cm
    bmi: Optional[float] = Field(None, example=25.0)
    systolic_bp: Optional[float] = Field(None, example=118.0)  # mmHg
    diastolic_bp: Optional[float] = Field(None, example=76.0)  # mmHg
    pulse: Optional[float] = Field(None, example=82.0)  # bpm
    temperature: Optional[float] = Field(None, example=36.8)  # °C
    respiratory_rate: Optional[float] = Field(None, example=18.0)  # bpm
    oxygen_saturation: Optional[float] = Field(None, example=98.0)  # %
    symptoms: List[str] = []
    warning_signs: List[str] = []
    fetal_heart_rate: Optional[float] = Field(None, example=144.0)  # bpm
    fetal_movement: Optional[str] = Field("Normal", example="Normal")
    fundal_height: Optional[float] = Field(None, example=24.0)  # cm
    edema: Optional[str] = Field("None", example="None")
    urine_findings: Dict[str, Any] = {}
    clinical_notes: Optional[str] = None
    healthcare_worker: Optional[str] = None
    facility: Optional[str] = None


class AntenatalVisitCreate(AntenatalVisitBase):
    pass


class AntenatalVisitResponse(AntenatalVisitBase):
    visit_id: str
    created_at: datetime

    class Config:
        from_attributes = True
