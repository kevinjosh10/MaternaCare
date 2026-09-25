import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    document_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=True, index=True)
    newborn_id = Column(String(36), ForeignKey("newborns.newborn_id", ondelete="CASCADE"), nullable=True, index=True)
    document_type = Column(String(100), nullable=False)
    # Types: "PREVIOUS_RECORD", "ANC_RECORD", "LAB_REPORT", "ULTRASOUND_REPORT",
    # "PRESCRIPTION", "DISCHARGE_SUMMARY", "DELIVERY_RECORD", "NEWBORN_RECORD",
    # "VACCINATION_RECORD", "REFERRAL_LETTER", "POSTNATAL_RECORD"
    upload_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_hash = Column(String(128), nullable=True)  # SHA-256 integrity checksum
    ocr_text_reference = Column(Text, nullable=True)  # Raw OCR extracted text
    extracted_data = Column(JSON, default=dict)  # Structured candidate data
    extraction_confidence = Column(Float, default=0.0)  # 0.0 to 1.0 confidence score
    verification_status = Column(String(50), default="PENDING", index=True)  # PENDING, VERIFIED, REJECTED
    verified_by = Column(String(100), nullable=True)  # Authorized healthcare worker ID/name
    verified_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="documents")
    pregnancy = relationship("Pregnancy", back_populates="documents")
    newborn = relationship("Newborn", back_populates="documents")
