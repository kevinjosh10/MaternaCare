import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Date, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base


class LabResult(Base):
    __tablename__ = "lab_results"

    test_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=True, index=True)
    visit_id = Column(String(36), nullable=True)
    test_date = Column(Date, nullable=False, index=True)
    test_name = Column(String(150), nullable=False, index=True)  # e.g., Hemoglobin, Fasting Blood Glucose, Urine Protein
    test_category = Column(String(100), nullable=False)  # HEMATOLOGY, BIOCHEMISTRY, URINALYSIS, SEROLOGY, etc.
    result = Column(String(255), nullable=False)
    unit = Column(String(50), nullable=True)  # g/dL, mg/dL, +, etc.
    reference_range = Column(String(100), nullable=True)
    abnormal_flag = Column(Boolean, default=False, index=True)
    lab_name = Column(String(150), nullable=True)
    report_document = Column(String(255), nullable=True)  # Document reference or file path
    verified_by = Column(String(100), nullable=True)
    verification_status = Column(String(50), default="PENDING", index=True)  # PENDING, VERIFIED, REJECTED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_lab_test_patient_date", "patient_id", "test_name", "test_date"),
    )

    # Relationships
    patient = relationship("Patient", back_populates="labs")
    pregnancy = relationship("Pregnancy", back_populates="labs")
