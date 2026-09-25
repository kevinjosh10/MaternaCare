import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Communication(Base):
    __tablename__ = "communications"

    communication_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    referral_id = Column(String(36), ForeignKey("referrals.referral_id", ondelete="CASCADE"), nullable=True, index=True)
    channel = Column(String(50), nullable=False)  # SMS, VOICE, TTS, PHONE, IN_APP
    recipient = Column(String(100), nullable=False)  # Phone number, email, or device identifier
    language = Column(String(20), default="en")
    message = Column(Text, nullable=False)
    message_type = Column(String(50), default="REFERRAL_ALERT")  # REFERRAL_ALERT, EMERGENCY_CALL, REMINDER, VISIT_NOTICE
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    sent_at = Column(DateTime, nullable=True)
    delivery_status = Column(String(50), default="QUEUED")  # QUEUED, SENT, DELIVERED, FAILED
    acknowledgement_status = Column(String(50), default="PENDING")  # PENDING, ACKNOWLEDGED
    provider_reference = Column(String(150), nullable=True)  # External gateway message SID

    referral = relationship("Referral", back_populates="communications")
