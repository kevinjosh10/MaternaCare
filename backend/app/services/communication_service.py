import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.communication import Communication
from app.schemas.communication import CommunicationCreate


class CommunicationService:

    @staticmethod
    def send_communication(db: Session, comm_in: CommunicationCreate) -> Communication:
        comm = Communication(
            **comm_in.model_dump(),
            delivery_status="SENT",
            sent_at=datetime.now(timezone.utc),
            provider_reference=f"MSG-{uuid.uuid4().hex[:12].upper()}"
        )
        db.add(comm)
        db.commit()
        db.refresh(comm)
        return comm

    @staticmethod
    def get_referral_communications(db: Session, referral_id: str) -> List[Communication]:
        return db.query(Communication).filter(Communication.referral_id == referral_id).order_by(Communication.created_at.desc()).all()


communication_service = CommunicationService()
