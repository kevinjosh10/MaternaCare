from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field


class PregnancyBase(BaseModel):
    patient_id: str
    pregnancy_number: int = Field(1, example=1)
    gravida: int = Field(1, example=1)
    para: int = Field(0, example=0)
    living_children: int = Field(0, example=0)
    abortion_count: int = Field(0, example=0)
    stillbirth_count: int = Field(0, example=0)
    last_menstrual_period: Optional[date] = None
    estimated_due_date: Optional[date] = None
    gestational_age: Optional[float] = Field(None, example=12.5)  # in weeks
    pregnancy_type: str = Field("Spontaneous", example="Spontaneous")
    singleton_or_multiple: str = Field("Singleton", example="Singleton")
    pregnancy_start_date: Optional[date] = None
    high_risk_flag: bool = Field(False, example=False)
    high_risk_reason: Optional[str] = None
    status: str = Field("ACTIVE", example="ACTIVE")


class PregnancyCreate(PregnancyBase):
    pass


class PregnancyUpdate(BaseModel):
    gravida: Optional[int] = None
    para: Optional[int] = None
    living_children: Optional[int] = None
    abortion_count: Optional[int] = None
    stillbirth_count: Optional[int] = None
    gestational_age: Optional[float] = None
    estimated_due_date: Optional[date] = None
    high_risk_flag: Optional[bool] = None
    high_risk_reason: Optional[str] = None
    status: Optional[str] = None


class PregnancyResponse(PregnancyBase):
    pregnancy_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
