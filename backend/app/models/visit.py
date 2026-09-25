import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Date, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class AntenatalVisit(Base):
    __tablename__ = "antenatal_visits"

    visit_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    visit_date = Column(Date, nullable=False, index=True)
    gestational_age = Column(Float, nullable=True)  # weeks
    weight = Column(Float, nullable=True)  # kg
    height = Column(Float, nullable=True)  # cm
    bmi = Column(Float, nullable=True)
    systolic_bp = Column(Float, nullable=True)  # mmHg
    diastolic_bp = Column(Float, nullable=True)  # mmHg
    pulse = Column(Float, nullable=True)  # bpm
    temperature = Column(Float, nullable=True)  # °C
    respiratory_rate = Column(Float, nullable=True)  # breaths/min
    oxygen_saturation = Column(Float, nullable=True)  # SpO2 %
    symptoms = Column(JSON, default=list)  # Reported symptoms
    warning_signs = Column(JSON, default=list)  # Red flags: severe headache, blurred vision, epigastric pain
    fetal_heart_rate = Column(Float, nullable=True)  # bpm
    fetal_movement = Column(String(50), nullable=True)  # Normal, Reduced, Absent
    fundal_height = Column(Float, nullable=True)  # cm
    edema = Column(String(50), nullable=True)  # None, Mild (+), Moderate (++), Severe (+++)
    urine_findings = Column(JSON, default=dict)  # {"protein": "trace", "glucose": "nil"}
    clinical_notes = Column(Text, nullable=True)
    healthcare_worker = Column(String(100), nullable=True)
    facility = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    pregnancy = relationship("Pregnancy", back_populates="antenatal_visits")
    patient = relationship("Patient")
