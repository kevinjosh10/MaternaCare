from typing import Optional, List, Dict, Any
from datetime import date, time, datetime
from pydantic import BaseModel, Field


class NewbornBase(BaseModel):
    mother_patient_id: str
    pregnancy_id: str
    delivery_id: Optional[str] = None
    name: str = Field("Baby of Mother", example="Baby Aarav")
    sex: str = Field(..., example="Male")
    date_of_birth: date
    time_of_birth: Optional[time] = None
    gestational_age: Optional[float] = Field(None, example=39.2)
    birth_weight: Optional[float] = Field(None, example=3100.0)  # grams
    birth_length: Optional[float] = Field(None, example=49.5)  # cm
    head_circumference: Optional[float] = Field(None, example=34.0)  # cm
    apgar_1_min: Optional[int] = Field(None, example=8)
    apgar_5_min: Optional[int] = Field(None, example=9)
    delivery_status: str = Field("LIVE_BIRTH", example="LIVE_BIRTH")
    resuscitation_required: bool = Field(False, example=False)
    feeding_started: bool = Field(True, example=True)
    breastfeeding_status: str = Field("EXCLUSIVE_BREASTFEEDING", example="EXCLUSIVE_BREASTFEEDING")
    newborn_screening: Dict[str, Any] = {"hearing": "Pass", "cchd": "Pass"}
    vaccinations: List[str] = ["BCG", "OPV-0", "Hepatitis-B (Birth Dose)"]
    clinical_notes: Optional[str] = None


class NewbornCreate(NewbornBase):
    pass


class NewbornResponse(NewbornBase):
    newborn_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class NewbornVisitBase(BaseModel):
    newborn_id: str
    visit_date: date
    age_days: int = Field(..., example=3)
    weight: Optional[float] = Field(None, example=3050.0)  # grams
    length: Optional[float] = Field(None, example=49.8)  # cm
    head_circumference: Optional[float] = Field(None, example=34.2)  # cm
    temperature: Optional[float] = Field(None, example=36.8)  # °C
    heart_rate: Optional[float] = Field(None, example=135.0)  # bpm
    respiratory_rate: Optional[float] = Field(None, example=42.0)  # bpm
    oxygen_saturation: Optional[float] = Field(None, example=98.0)  # %
    feeding: Optional[str] = Field("Exclusive Breastfeeding", example="Exclusive Breastfeeding")
    urination: Optional[str] = Field("Normal (>6 wet nappies/day)", example="Normal")
    stool: Optional[str] = Field("Soft yellow", example="Soft yellow")
    jaundice_observation: Optional[str] = Field("None", example="None")
    activity: Optional[str] = Field("Active and Alert", example="Active and Alert")
    sleep: Optional[str] = None
    clinical_findings: List[str] = []
    vaccinations: List[str] = []
    screenings: Dict[str, Any] = {}
    developmental_observations: List[str] = []
    clinician_notes: Optional[str] = None


class NewbornVisitCreate(NewbornVisitBase):
    pass


class NewbornVisitResponse(NewbornVisitBase):
    visit_id: str
    created_at: datetime

    class Config:
        from_attributes = True
