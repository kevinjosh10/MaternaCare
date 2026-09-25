from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class DocumentBase(BaseModel):
    patient_id: str
    pregnancy_id: Optional[str] = None
    newborn_id: Optional[str] = None
    document_type: str = Field(..., example="ANC_RECORD")
    file_url: str
    file_hash: Optional[str] = None
    ocr_text_reference: Optional[str] = None
    extracted_data: Dict[str, Any] = {}
    extraction_confidence: float = Field(0.0, example=0.92)
    verification_status: str = Field("PENDING", example="PENDING")
    notes: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentVerifyRequest(BaseModel):
    verification_status: str = Field(..., example="VERIFIED")  # VERIFIED or REJECTED
    verified_by: str = Field(..., example="Dr. Priya Patel (Obstetrician)")
    corrected_data: Optional[Dict[str, Any]] = None  # Human reviewer's verified adjustments
    notes: Optional[str] = None


class DocumentResponse(DocumentBase):
    document_id: str
    upload_date: datetime
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None

    class Config:
        from_attributes = True
