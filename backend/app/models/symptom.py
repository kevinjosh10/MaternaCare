import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Symptom(Base):
    __tablename__ = "symptoms"

    symptom_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=True, index=True)
    newborn_id = Column(String(36), ForeignKey("newborns.newborn_id", ondelete="CASCADE"), nullable=True, index=True)
    date_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    symptom_type = Column(String(100), nullable=False, index=True)
    # e.g., "HEADACHE", "BLURRED_VISION", "EPIGASTRIC_PAIN", "VAGINAL_BLEEDING", "REDUCED_FETAL_MOVEMENT",
    # "FEVER", "DYSPNEA", "CHEST_PAIN", "VOMITING", "NEONATAL_LETHARGY", "NEONATAL_POOR_FEEDING"
    severity = Column(String(50), nullable=False)  # MILD, MODERATE, SEVERE, CRITICAL
    duration = Column(String(100), nullable=True)  # e.g., "2 hours", "3 days"
    onset = Column(String(50), nullable=True)  # SUDDEN, GRADUAL
    frequency = Column(String(50), nullable=True)  # CONSTANT, INTERMITTENT, EPISODIC
    associated_symptoms = Column(JSON, default=list)  # e.g., ["nausea", "photophobia"]
    reported_by = Column(String(100), nullable=True)  # PATIENT, ASHA_WORKER, NURSE, DOCTOR
    verified_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    patient = relationship("Patient", back_populates="symptoms")
    pregnancy = relationship("Pregnancy", back_populates="symptoms")
    newborn = relationship("Newborn", back_populates="symptoms")
