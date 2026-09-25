import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class ObstetricHistory(Base):
    __tablename__ = "obstetric_histories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    previous_pregnancies = Column(Integer, default=0)
    previous_live_births = Column(Integer, default=0)
    previous_abortions = Column(Integer, default=0)
    previous_stillbirths = Column(Integer, default=0)
    previous_c_sections = Column(Integer, default=0)
    previous_vaginal_deliveries = Column(Integer, default=0)
    previous_preeclampsia = Column(Boolean, default=False)
    previous_gestational_diabetes = Column(Boolean, default=False)
    previous_postpartum_haemorrhage = Column(Boolean, default=False)
    previous_preterm_birth = Column(Boolean, default=False)
    previous_low_birth_weight = Column(Boolean, default=False)
    previous_neonatal_complications_or_death = Column(Boolean, default=False)
    complications_details = Column(JSON, nullable=True)  # List of previous pregnancy details or events
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    patient = relationship("Patient", back_populates="obstetric_history")


class MedicalHistory(Base):
    __tablename__ = "medical_histories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    chronic_conditions = Column(JSON, default=list)  # e.g., ["Hypertension", "Type 2 Diabetes", "Asthma"]
    previous_surgeries = Column(JSON, default=list)  # e.g., [{"surgery": "Appendectomy", "year": 2018}]
    allergies = Column(JSON, default=list)  # e.g., ["Penicillin", "Sulfa drugs"]
    medications = Column(JSON, default=list)  # Ongoing non-obstetric medications
    family_history = Column(JSON, default=list)  # e.g., ["Maternal Hypertension", "Twins in family"]
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    patient = relationship("Patient", back_populates="medical_history")
