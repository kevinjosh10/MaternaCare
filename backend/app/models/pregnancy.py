import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Date, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Pregnancy(Base):
    __tablename__ = "pregnancies"

    pregnancy_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    pregnancy_number = Column(Integer, default=1)
    gravida = Column(Integer, default=1)
    para = Column(Integer, default=0)
    living_children = Column(Integer, default=0)
    abortion_count = Column(Integer, default=0)
    stillbirth_count = Column(Integer, default=0)
    last_menstrual_period = Column(Date, nullable=True)
    estimated_due_date = Column(Date, nullable=True)
    gestational_age = Column(Float, nullable=True)  # in weeks
    pregnancy_type = Column(String(50), default="Spontaneous")  # Spontaneous, IVF, etc.
    singleton_or_multiple = Column(String(50), default="Singleton")  # Singleton, Twin, Triplet
    pregnancy_start_date = Column(Date, nullable=True)
    high_risk_flag = Column(Boolean, default=False, index=True)
    high_risk_reason = Column(Text, nullable=True)
    status = Column(String(50), default="ACTIVE")  # ACTIVE, DELIVERED, TERMINATED, LOSS
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    patient = relationship("Patient", back_populates="pregnancies")
    antenatal_visits = relationship("AntenatalVisit", back_populates="pregnancy", cascade="all, delete-orphan")
    observations = relationship("Observation", back_populates="pregnancy", cascade="all, delete-orphan")
    symptoms = relationship("Symptom", back_populates="pregnancy", cascade="all, delete-orphan")
    labs = relationship("LabResult", back_populates="pregnancy", cascade="all, delete-orphan")
    ultrasounds = relationship("UltrasoundRecord", back_populates="pregnancy", cascade="all, delete-orphan")
    medications = relationship("MedicationRecord", back_populates="pregnancy", cascade="all, delete-orphan")
    supplements = relationship("SupplementRecord", back_populates="pregnancy", cascade="all, delete-orphan")
    vaccinations = relationship("VaccinationRecord", back_populates="pregnancy", cascade="all, delete-orphan")
    deliveries = relationship("Delivery", back_populates="pregnancy", cascade="all, delete-orphan")
    newborns = relationship("Newborn", back_populates="pregnancy", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessment", back_populates="pregnancy", cascade="all, delete-orphan")
    referrals = relationship("Referral", back_populates="pregnancy", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="pregnancy", cascade="all, delete-orphan")
