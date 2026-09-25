import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class MedicationRecord(Base):
    __tablename__ = "medication_records"

    medication_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=True, index=True)
    medicine_name = Column(String(150), nullable=False)
    dose = Column(String(100), nullable=False)  # e.g., "500 mg", "100 mg"
    frequency = Column(String(100), nullable=False)  # e.g., "TDS", "Once daily after food"
    route = Column(String(50), default="Oral")  # Oral, IV, IM, Topical
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    reason = Column(String(255), nullable=True)  # e.g., "Gestational hypertension", "Bacterial infection"
    prescribed_by = Column(String(100), nullable=True)
    status = Column(String(50), default="ACTIVE")  # ACTIVE, COMPLETED, DISCONTINUED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    patient = relationship("Patient", back_populates="medications")
    pregnancy = relationship("Pregnancy", back_populates="medications")


class SupplementRecord(Base):
    __tablename__ = "supplement_records"

    supplement_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=True, index=True)
    name = Column(String(150), nullable=False)  # e.g., "Iron Folic Acid (IFA)", "Calcium & Vitamin D3"
    dose = Column(String(100), nullable=False)  # e.g., "60mg elemental iron + 500mcg folic acid"
    frequency = Column(String(100), nullable=False)  # e.g., "Once daily"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    prescribed_by = Column(String(100), nullable=True)
    status = Column(String(50), default="ACTIVE")  # ACTIVE, COMPLETED, PAUSED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    patient = relationship("Patient", back_populates="supplements")
    pregnancy = relationship("Pregnancy", back_populates="supplements")


class VaccinationRecord(Base):
    __tablename__ = "vaccination_records"

    vaccination_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=True, index=True)
    newborn_id = Column(String(36), ForeignKey("newborns.newborn_id", ondelete="CASCADE"), nullable=True, index=True)
    vaccine = Column(String(150), nullable=False)  # e.g., "Td-1", "Td-2", "Td-Booster", "BCG", "OPV-0", "Hepatitis B"
    dose = Column(String(50), nullable=False)  # e.g., "Dose 1", "0.5 ml"
    date = Column(Date, nullable=False, index=True)
    facility = Column(String(150), nullable=True)
    provider = Column(String(100), nullable=True)
    status = Column(String(50), default="ADMINISTERED")  # ADMINISTERED, SCHEDULED, MISSED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    patient = relationship("Patient", back_populates="vaccinations")
    pregnancy = relationship("Pregnancy", back_populates="vaccinations")
    newborn = relationship("Newborn", back_populates="vaccinations")
