from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class FacilityBase(BaseModel):
    name: str = Field(..., example="District Women's & Children's Hospital")
    type: str = Field(..., example="DISTRICT_HOSPITAL")
    address: Optional[str] = Field(None, example="Civil Lines, Hospital Road")
    district: str = Field(..., example="Varanasi")
    state: str = Field(..., example="Uttar Pradesh")
    latitude: Optional[float] = Field(None, example=25.3176)
    longitude: Optional[float] = Field(None, example=82.9739)
    phone: Optional[str] = Field(None, example="+91 542 2223344")
    emergency_phone: Optional[str] = Field(None, example="108 / 102")
    services: List[str] = ["24x7 Emergency Obstetric Care", "Cesarean Section", "Blood Bank", "SNCU", "ICU"]
    specialties: List[str] = ["OBGYN", "NEONATOLOGY", "ANESTHESIOLOGY"]
    operating_status: str = Field("ACTIVE", example="ACTIVE")


class FacilityCreate(FacilityBase):
    pass


class FacilityResponse(FacilityBase):
    facility_id: str
    created_at: datetime

    class Config:
        from_attributes = True
