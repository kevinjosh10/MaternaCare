import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Date, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    sex = Column(String(20), default="Female", nullable=False)
    phone = Column(String(30), nullable=True, index=True)
    address = Column(String(500), nullable=True)
    district = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=True)
    preferred_language = Column(String(50), default="en", nullable=False)
    emergency_contact = Column(JSON, nullable=True)  # {name, relation, phone}
    blood_group = Column(String(10), nullable=True)
    occupation = Column(String(100), nullable=True)
    education = Column(String(100), nullable=True)
    marital_status = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    pregnancies = relationship("Pregnancy", back_populates="patient", cascade="all, delete-orphan")
    obstetric_history = relationship("ObstetricHistory", back_populates="patient", uselist=False, cascade="all, delete-orphan")
    medical_history = relationship("MedicalHistory", back_populates="patient", uselist=False, cascade="all, delete-orphan")
    observations = relationship("Observation", back_populates="patient", cascade="all, delete-orphan")
    symptoms = relationship("Symptom", back_populates="patient", cascade="all, delete-orphan")
    labs = relationship("LabResult", back_populates="patient", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("MedicationRecord", back_populates="patient", cascade="all, delete-orphan")
    supplements = relationship("SupplementRecord", back_populates="patient", cascade="all, delete-orphan")
    vaccinations = relationship("VaccinationRecord", back_populates="patient", cascade="all, delete-orphan")
    deliveries = relationship("Delivery", back_populates="patient", cascade="all, delete-orphan")
    postpartum_visits = relationship("PostpartumVisit", back_populates="patient", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessment", back_populates="patient", cascade="all, delete-orphan")
    referrals = relationship("Referral", back_populates="patient", cascade="all, delete-orphan")
