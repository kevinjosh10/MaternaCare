import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, Date, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class PostpartumVisit(Base):
    __tablename__ = "postpartum_visits"

    visit_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    delivery_id = Column(String(36), ForeignKey("deliveries.delivery_id", ondelete="CASCADE"), nullable=True, index=True)
    visit_date = Column(Date, nullable=False, index=True)
    postpartum_day = Column(Integer, nullable=False)  # e.g., Day 1, Day 3, Day 7, Day 14, Day 42 (6w), Day 90 (3m), Day 365 (1y)
    systolic_bp = Column(Float, nullable=True)  # mmHg
    diastolic_bp = Column(Float, nullable=True)  # mmHg
    pulse = Column(Float, nullable=True)  # bpm
    temperature = Column(Float, nullable=True)  # °C
    weight = Column(Float, nullable=True)  # kg
    vaginal_bleeding = Column(String(100), nullable=True)  # Lochia Rubra, Lochia Serosa, Lochia Alba, Excessive/PPH concern
    uterine_status = Column(String(100), nullable=True)  # Well contracted, at umbilicus, not palpable, tender/boggy
    wound_status = Column(String(100), nullable=True)  # Perineum/Incision clean & dry, healing well, erythema, discharge
    pain = Column(String(100), nullable=True)  # None, Mild, Moderate, Severe (or VAS 0-10)
    headache = Column(String(100), nullable=True)  # None, Mild, Severe/persistent (Red flag for postpartum preeclampsia)
    urinary_status = Column(String(100), nullable=True)  # Normal, dysuria, incontinence
    bowel_status = Column(String(100), nullable=True)  # Normal, constipated
    breastfeeding = Column(String(100), nullable=True)  # Established, struggling with latch, formula feeding
    breast_symptoms = Column(String(100), nullable=True)  # Soft, engorged, mastitis signs, cracked nipples
    medications = Column(JSON, default=list)  # Paracetamol, IFA, Calcium, Antibiotics
    nutrition = Column(String(255), nullable=True)
    sleep = Column(String(100), nullable=True)
    emotional_wellbeing = Column(JSON, default=dict)  # {"epds_score": 4, "mood": "Stable", "bonding": "Good"}
    clinical_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    patient = relationship("Patient", back_populates="postpartum_visits")
    delivery = relationship("Delivery", back_populates="postpartum_visits")
