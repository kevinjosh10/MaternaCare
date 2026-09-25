import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, JSON
from app.core.database import Base


class Facility(Base):
    __tablename__ = "facilities"

    facility_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False, index=True)
    type = Column(String(100), nullable=False)
    # PRIMARY_HEALTH_CENTRE, COMMUNITY_HEALTH_CENTRE, DISTRICT_HOSPITAL, TERTIARY_CARE_HOSPITAL, PRIVATE_HOSPITAL
    address = Column(String(500), nullable=True)
    district = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    phone = Column(String(50), nullable=True)
    emergency_phone = Column(String(50), nullable=True)
    services = Column(JSON, default=list)  # e.g., ["24x7 Delivery", "Cesarean Section", "Blood Storage", "SNCU"]
    specialties = Column(JSON, default=list)  # e.g., ["OBGYN", "PEDIATRICS", "ANESTHESIA", "NEONATOLOGY"]
    operating_status = Column(String(50), default="ACTIVE")  # ACTIVE, TEMPORARILY_CLOSED, FULL_CAPACITY
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
