from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field


class LabResultBase(BaseModel):
    patient_id: str
    pregnancy_id: Optional[str] = None
    visit_id: Optional[str] = None
    test_date: date
    test_name: str = Field(..., example="Hemoglobin")
    test_category: str = Field(..., example="HEMATOLOGY")  # HEMATOLOGY, BIOCHEMISTRY, URINALYSIS, SEROLOGY
    result: str = Field(..., example="11.2")
    unit: Optional[str] = Field(None, example="g/dL")
    reference_range: Optional[str] = Field(None, example="11.0 - 15.0")
    abnormal_flag: bool = Field(False, example=False)
    lab_name: Optional[str] = Field(None, example="District Hospital Laboratory")
    report_document: Optional[str] = None
    verified_by: Optional[str] = None
    verification_status: str = Field("PENDING", example="PENDING")  # PENDING, VERIFIED, REJECTED


class LabResultCreate(LabResultBase):
    pass


class LabVerificationUpdate(BaseModel):
    verification_status: str = Field(..., example="VERIFIED")  # VERIFIED, REJECTED
    verified_by: str = Field(..., example="Dr. Sharma")


class LabResultResponse(LabResultBase):
    test_id: str
    created_at: datetime

    class Config:
        from_attributes = True
