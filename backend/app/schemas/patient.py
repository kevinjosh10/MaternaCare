from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, Field


class EmergencyContactSchema(BaseModel):
    name: Optional[str] = None
    relation: Optional[str] = None
    phone: Optional[str] = None


class ObstetricHistoryBase(BaseModel):
    previous_pregnancies: int = 0
    previous_live_births: int = 0
    previous_abortions: int = 0
    previous_stillbirths: int = 0
    previous_c_sections: int = 0
    previous_vaginal_deliveries: int = 0
    previous_preeclampsia: bool = False
    previous_gestational_diabetes: bool = False
    previous_postpartum_haemorrhage: bool = False
    previous_preterm_birth: bool = False
    previous_low_birth_weight: bool = False
    previous_neonatal_complications_or_death: bool = False
    complications_details: Optional[List[Dict[str, Any]]] = []


class ObstetricHistoryCreate(ObstetricHistoryBase):
    pass


class ObstetricHistoryResponse(ObstetricHistoryBase):
    id: str
    patient_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class MedicalHistoryBase(BaseModel):
    chronic_conditions: List[str] = []
    previous_surgeries: List[Dict[str, Any]] = []
    allergies: List[str] = []
    medications: List[Dict[str, Any]] = []
    family_history: List[str] = []


class MedicalHistoryCreate(MedicalHistoryBase):
    pass


class MedicalHistoryResponse(MedicalHistoryBase):
    id: str
    patient_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class PatientBase(BaseModel):
    name: str = Field(..., example="Sunita Devi")
    date_of_birth: Optional[date] = None
    age: Optional[int] = Field(None, example=24)
    sex: str = Field("Female", example="Female")
    phone: Optional[str] = Field(None, example="+91 9876543210")
    address: Optional[str] = Field(None, example="Village Rampur, Post Kalan")
    district: Optional[str] = Field(None, example="Varanasi")
    state: Optional[str] = Field(None, example="Uttar Pradesh")
    preferred_language: str = Field("hi", example="hi")
    emergency_contact: Optional[EmergencyContactSchema] = None
    blood_group: Optional[str] = Field(None, example="B+")
    occupation: Optional[str] = Field(None, example="Homemaker")
    education: Optional[str] = Field(None, example="Secondary School")
    marital_status: Optional[str] = Field(None, example="Married")


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    preferred_language: Optional[str] = None
    emergency_contact: Optional[EmergencyContactSchema] = None
    blood_group: Optional[str] = None
    occupation: Optional[str] = None
    education: Optional[str] = None
    marital_status: Optional[str] = None


class PatientResponse(PatientBase):
    patient_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
