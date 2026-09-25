from typing import Optional, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, Field


class UltrasoundBase(BaseModel):
    pregnancy_id: str
    patient_id: str
    scan_date: date
    gestational_age: Optional[float] = Field(None, example=20.0)  # weeks
    scan_type: str = Field(..., example="ANOMALY_SCAN")
    fetal_count: int = Field(1, example=1)
    fetal_position: Optional[str] = Field("Cephalic", example="Cephalic")
    fetal_heart_rate: Optional[float] = Field(None, example=142.0)
    estimated_fetal_weight: Optional[float] = Field(None, example=350.0)  # grams
    growth_assessment: Optional[str] = Field("Appropriate for Gestational Age (AGA)", example="AGA")
    placenta_information: Dict[str, Any] = {"location": "Fundal/Posterior", "maturity_grade": "Grade 1"}
    amniotic_fluid_information: Dict[str, Any] = {"afi_cm": 14.2, "status": "Adequate"}
    findings: Optional[str] = None
    impression: Optional[str] = None
    report_document: Optional[str] = None
    verification_status: str = Field("PENDING", example="PENDING")
    verified_by: Optional[str] = None


class UltrasoundCreate(UltrasoundBase):
    pass


class UltrasoundResponse(UltrasoundBase):
    scan_id: str
    created_at: datetime

    class Config:
        from_attributes = True
