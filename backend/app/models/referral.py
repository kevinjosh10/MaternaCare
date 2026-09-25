import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Referral(Base):
    __tablename__ = "referrals"

    referral_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=True, index=True)
    newborn_id = Column(String(36), ForeignKey("newborns.newborn_id", ondelete="CASCADE"), nullable=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    created_by = Column(String(100), nullable=False)
    reason = Column(String(255), nullable=False)
    risk_level = Column(String(50), nullable=False, index=True)  # LOW, MODERATE, HIGH, CRITICAL
    clinical_summary = Column(Text, nullable=False)
    source_facility = Column(String(200), nullable=False)
    destination_facility = Column(String(200), nullable=True)
    transport_status = Column(String(50), default="NONE")  # NONE, AMBULANCE_REQUESTED, EN_ROUTE, ARRIVED
    referral_status = Column(String(50), default="CREATED", index=True)
    # CREATED, CLINICIAN_REVIEW, FACILITY_SELECTED, REFERRAL_SENT, ACKNOWLEDGED,
    # TRANSFER_IN_PROGRESS, ARRIVED, COMPLETED, CANCELLED
    acknowledged_at = Column(DateTime, nullable=True)
    transfer_started_at = Column(DateTime, nullable=True)
    arrival_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="referrals")
    pregnancy = relationship("Pregnancy", back_populates="referrals")
    communications = relationship("Communication", back_populates="referral", cascade="all, delete-orphan")
