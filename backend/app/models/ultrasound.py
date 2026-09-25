import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, Date, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class UltrasoundRecord(Base):
    __tablename__ = "ultrasound_records"

    scan_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    scan_date = Column(Date, nullable=False, index=True)
    gestational_age = Column(Float, nullable=True)  # weeks
    scan_type = Column(String(100), nullable=False)  # DATING, NT_SCAN, ANOMALY_SCAN, GROWTH_DOPPLER, BIOPHYSICAL_PROFILE
    fetal_count = Column(Integer, default=1)
    fetal_position = Column(String(100), nullable=True)  # Cephalic, Breech, Transverse
    fetal_heart_rate = Column(Float, nullable=True)  # bpm
    estimated_fetal_weight = Column(Float, nullable=True)  # grams
    growth_assessment = Column(String(100), nullable=True)  # Appropriate for Gestational Age (AGA), SGA, LGA, IUGR
    placenta_information = Column(JSON, default=dict)  # {"location": "Anterior", "grade": 2, "previa": false}
    amniotic_fluid_information = Column(JSON, default=dict)  # {"afi_cm": 14.5, "status": "Normal"}
    findings = Column(Text, nullable=True)
    impression = Column(Text, nullable=True)
    report_document = Column(String(255), nullable=True)
    verification_status = Column(String(50), default="PENDING", index=True)  # PENDING, VERIFIED, REJECTED
    verified_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    pregnancy = relationship("Pregnancy", back_populates="ultrasounds")
    patient = relationship("Patient")
