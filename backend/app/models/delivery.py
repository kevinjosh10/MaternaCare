import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Date, Time, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Delivery(Base):
    __tablename__ = "deliveries"

    delivery_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    delivery_date = Column(Date, nullable=False, index=True)
    delivery_time = Column(Time, nullable=True)
    facility = Column(String(150), nullable=True)
    delivery_mode = Column(String(100), nullable=False)
    # SPONTANEOUS_VAGINAL, INSTRUMENTAL_VACUUM, INSTRUMENTAL_FORCEPS, ELECTIVE_C_SECTION, EMERGENCY_C_SECTION
    gestational_age_at_delivery = Column(Float, nullable=True)  # weeks
    indication_for_c_section = Column(Text, nullable=True)
    labour_complications = Column(JSON, default=list)  # e.g., ["Prolonged second stage", "Fetal distress"]
    maternal_complications = Column(JSON, default=list)  # e.g., ["Perineal tear 2nd degree", "Mild PPH"]
    blood_loss = Column(Float, nullable=True)  # in mL
    post_delivery_vitals = Column(JSON, default=dict)  # {"systolic_bp": 120, "diastolic_bp": 78, "pulse": 76}
    clinical_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    pregnancy = relationship("Pregnancy", back_populates="deliveries")
    patient = relationship("Patient", back_populates="deliveries")
    newborns = relationship("Newborn", back_populates="delivery")
    postpartum_visits = relationship("PostpartumVisit", back_populates="delivery")
