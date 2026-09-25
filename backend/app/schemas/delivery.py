from typing import Optional, List, Dict, Any
from datetime import date, time, datetime
from pydantic import BaseModel, Field


class DeliveryBase(BaseModel):
    pregnancy_id: str
    patient_id: str
    delivery_date: date
    delivery_time: Optional[time] = None
    facility: Optional[str] = Field(None, example="District Hospital Obstetrics Wing")
    delivery_mode: str = Field(..., example="SPONTANEOUS_VAGINAL")
    gestational_age_at_delivery: Optional[float] = Field(None, example=39.2)
    indication_for_c_section: Optional[str] = None
    labour_complications: List[str] = []
    maternal_complications: List[str] = []
    blood_loss: Optional[float] = Field(None, example=250.0)  # in mL
    post_delivery_vitals: Dict[str, Any] = {"systolic_bp": 118, "diastolic_bp": 76, "pulse": 78}
    clinical_notes: Optional[str] = None


class DeliveryCreate(DeliveryBase):
    pass


class DeliveryResponse(DeliveryBase):
    delivery_id: str
    created_at: datetime

    class Config:
        from_attributes = True
