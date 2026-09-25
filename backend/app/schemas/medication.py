from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field


# Medication
class MedicationBase(BaseModel):
    patient_id: str
    pregnancy_id: Optional[str] = None
    medicine_name: str = Field(..., example="Labetalol")
    dose: str = Field(..., example="100 mg")
    frequency: str = Field(..., example="Twice daily")
    route: str = Field("Oral", example="Oral")
    start_date: date
    end_date: Optional[date] = None
    reason: Optional[str] = Field(None, example="Gestational hypertension management")
    prescribed_by: Optional[str] = None
    status: str = Field("ACTIVE", example="ACTIVE")


class MedicationCreate(MedicationBase):
    pass


class MedicationResponse(MedicationBase):
    medication_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# Supplement
class SupplementBase(BaseModel):
    patient_id: str
    pregnancy_id: Optional[str] = None
    name: str = Field(..., example="Iron and Folic Acid (IFA)")
    dose: str = Field(..., example="60 mg Iron + 500 mcg Folic Acid")
    frequency: str = Field(..., example="Once daily after dinner")
    start_date: date
    end_date: Optional[date] = None
    prescribed_by: Optional[str] = None
    status: str = Field("ACTIVE", example="ACTIVE")


class SupplementCreate(SupplementBase):
    pass


class SupplementResponse(SupplementBase):
    supplement_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# Vaccination
class VaccinationBase(BaseModel):
    patient_id: str
    pregnancy_id: Optional[str] = None
    newborn_id: Optional[str] = None
    vaccine: str = Field(..., example="Td-1")
    dose: str = Field(..., example="0.5 mL")
    date: date
    facility: Optional[str] = None
    provider: Optional[str] = None
    status: str = Field("ADMINISTERED", example="ADMINISTERED")


class VaccinationCreate(VaccinationBase):
    pass


class VaccinationResponse(VaccinationBase):
    vaccination_id: str
    created_at: datetime

    class Config:
        from_attributes = True
