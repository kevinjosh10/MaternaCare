import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base


class Observation(Base):
    __tablename__ = "observations"

    observation_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=True, index=True)
    newborn_id = Column(String(36), ForeignKey("newborns.newborn_id", ondelete="CASCADE"), nullable=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    observation_type = Column(String(100), nullable=False, index=True)
    # e.g., systolic_bp, diastolic_bp, pulse, temperature, spo2, fetal_heart_rate,
    # fundal_height, weight, hemoglobin, random_blood_sugar, fasting_blood_sugar
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)  # mmHg, bpm, °C, %, cm, kg, g/dL, mg/dL
    source = Column(String(50), default="CLINICAL_VISIT")  # CLINICAL_VISIT, LAB, WEARABLE, PATIENT_REPORTED
    verified = Column(Boolean, default=False, index=True)
    recorded_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_obs_patient_time", "patient_id", "timestamp"),
        Index("ix_obs_type_time", "observation_type", "timestamp"),
    )

    # Relationships
    patient = relationship("Patient", back_populates="observations")
    pregnancy = relationship("Pregnancy", back_populates="observations")
    newborn = relationship("Newborn", back_populates="observations")
