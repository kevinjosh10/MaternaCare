import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON
from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    audit_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(100), nullable=False, index=True)
    role = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False, index=True)
    # Actions: PATIENT_VIEWED, PATIENT_CREATED, RECORD_UPDATED, DOCUMENT_UPLOADED,
    # EXTRACTION_VERIFIED, AI_ASSESSMENT_GENERATED, AI_ASSESSMENT_REVIEWED,
    # REFERRAL_CREATED, REFERRAL_UPDATED, FACILITY_CHANGED, VOICE_QUERY_PROCESSED
    patient_id = Column(String(36), nullable=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    resource = Column(String(100), nullable=False)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    device_metadata = Column(JSON, default=dict)  # IP address, User-Agent, Session ID
