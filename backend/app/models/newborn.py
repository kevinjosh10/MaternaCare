import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, Date, Time, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Newborn(Base):
    __tablename__ = "newborns"

    newborn_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mother_patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=False, index=True)
    delivery_id = Column(String(36), ForeignKey("deliveries.delivery_id", ondelete="CASCADE"), nullable=True, index=True)
    name = Column(String(150), default="Baby of Mother", nullable=False)
    sex = Column(String(20), nullable=False)  # Male, Female, Ambiguous
    date_of_birth = Column(Date, nullable=False, index=True)
    time_of_birth = Column(Time, nullable=True)
    gestational_age = Column(Float, nullable=True)  # weeks at birth
    birth_weight = Column(Float, nullable=True)  # in grams (e.g., 2950)
    birth_length = Column(Float, nullable=True)  # in cm
    head_circumference = Column(Float, nullable=True)  # in cm
    apgar_1_min = Column(Integer, nullable=True)  # 0-10
    apgar_5_min = Column(Integer, nullable=True)  # 0-10
    delivery_status = Column(String(50), default="LIVE_BIRTH")  # LIVE_BIRTH, STILLBIRTH
    resuscitation_required = Column(Boolean, default=False)
    feeding_started = Column(Boolean, default=True)
    breastfeeding_status = Column(String(50), default="EXCLUSIVE_BREASTFEEDING")  # EXCLUSIVE_BREASTFEEDING, MIXED, FORMULA
    newborn_screening = Column(JSON, default=dict)  # {"hearing": "Pass", "cchd": "Pass", "metabolic": "Normal"}
    vaccinations = Column(JSON, default=list)  # ["BCG", "OPV-0", "Hepatitis-B birth dose"]
    clinical_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    pregnancy = relationship("Pregnancy", back_populates="newborns")
    delivery = relationship("Delivery", back_populates="newborns")
    visits = relationship("NewbornVisit", back_populates="newborn", cascade="all, delete-orphan")
    observations = relationship("Observation", back_populates="newborn", cascade="all, delete-orphan")
    symptoms = relationship("Symptom", back_populates="newborn", cascade="all, delete-orphan")
    vaccination_records = relationship("VaccinationRecord", back_populates="newborn", cascade="all, delete-orphan")


class NewbornVisit(Base):
    __tablename__ = "newborn_visits"

    visit_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    newborn_id = Column(String(36), ForeignKey("newborns.newborn_id", ondelete="CASCADE"), nullable=False, index=True)
    visit_date = Column(Date, nullable=False, index=True)
    age_days = Column(Integer, nullable=False)  # Age in days
    weight = Column(Float, nullable=True)  # in grams
    length = Column(Float, nullable=True)  # in cm
    head_circumference = Column(Float, nullable=True)  # in cm
    temperature = Column(Float, nullable=True)  # °C
    heart_rate = Column(Float, nullable=True)  # bpm
    respiratory_rate = Column(Float, nullable=True)  # breaths/min
    oxygen_saturation = Column(Float, nullable=True)  # SpO2 %
    feeding = Column(String(50), nullable=True)  # Exclusive Breastfeeding, Formula, Mixed, Complementary
    urination = Column(String(50), nullable=True)  # Normal (>=6 wet diapers), Decreased
    stool = Column(String(50), nullable=True)  # Normal meconium/transitional/yellow, Diarrhea, Constipated
    jaundice_observation = Column(String(100), nullable=True)  # None, Zone 1 (Face), Zone 2 (Trunk), Zone 3 (Limbs), Severe
    activity = Column(String(50), nullable=True)  # Active & Alert, Lethargic, Irritable, Hypotonic
    sleep = Column(String(100), nullable=True)
    clinical_findings = Column(JSON, default=list)  # Umbilical cord stump status, skin rashes, thrush
    vaccinations = Column(JSON, default=list)  # Administered this visit
    screenings = Column(JSON, default=dict)
    developmental_observations = Column(JSON, default=list)  # e.g., ["Social smile at 6w", "Head holding at 3m"]
    clinician_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    newborn = relationship("Newborn", back_populates="visits")
