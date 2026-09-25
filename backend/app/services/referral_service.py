from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.referral import Referral
from app.models.communication import Communication
from app.schemas.referral import ReferralCreate, ReferralStatusUpdate


class ReferralService:

    VALID_TRANSITIONS = {
        "CREATED": ["CLINICIAN_REVIEW", "FACILITY_SELECTED", "CANCELLED"],
        "CLINICIAN_REVIEW": ["FACILITY_SELECTED", "CANCELLED"],
        "FACILITY_SELECTED": ["REFERRAL_SENT", "CANCELLED"],
        "REFERRAL_SENT": ["ACKNOWLEDGED", "CANCELLED"],
        "ACKNOWLEDGED": ["TRANSFER_IN_PROGRESS", "CANCELLED"],
        "TRANSFER_IN_PROGRESS": ["ARRIVED", "CANCELLED"],
        "ARRIVED": ["COMPLETED", "CANCELLED"],
        "COMPLETED": [],
        "CANCELLED": []
    }

    @staticmethod
    def create_referral(db: Session, referral_in: ReferralCreate) -> Referral:
        referral = Referral(**referral_in.model_dump())
        db.add(referral)
        db.commit()
        db.refresh(referral)

        # Trigger automatic initial emergency alert communication
        auto_comm = Communication(
            referral_id=referral.referral_id,
            channel="SMS",
            recipient=referral.destination_facility or "Emergency Desk",
            language="en",
            message=(
                f"MaternaCare URGENT Referral Created: Patient ID {referral.patient_id}. "
                f"Risk Level: {referral.risk_level}. Reason: {referral.reason}."
            ),
            message_type="REFERRAL_ALERT",
            delivery_status="SENT",
            sent_at=datetime.now(timezone.utc)
        )
        db.add(auto_comm)
        db.commit()

        return referral

    @staticmethod
    def get_referral(db: Session, referral_id: str) -> Optional[Referral]:
        return db.query(Referral).filter(Referral.referral_id == referral_id).first()

    @staticmethod
    def get_patient_referrals(db: Session, patient_id: str) -> List[Referral]:
        return db.query(Referral).filter(Referral.patient_id == patient_id).order_by(Referral.created_at.desc()).all()

    @staticmethod
    def update_referral_status(db: Session, referral_id: str, update_in: ReferralStatusUpdate) -> Optional[Referral]:
        referral = ReferralService.get_referral(db, referral_id)
        if not referral:
            return None

        new_status = update_in.referral_status
        referral.referral_status = new_status
        now = datetime.now(timezone.utc)

        if new_status == "ACKNOWLEDGED" and not referral.acknowledged_at:
            referral.acknowledged_at = now
        elif new_status == "TRANSFER_IN_PROGRESS" and not referral.transfer_started_at:
            referral.transfer_started_at = now
        elif new_status == "ARRIVED" and not referral.arrival_at:
            referral.arrival_at = now
        elif new_status == "COMPLETED" and not referral.completed_at:
            referral.completed_at = now

        if update_in.transport_status:
            referral.transport_status = update_in.transport_status
        if update_in.destination_facility:
            referral.destination_facility = update_in.destination_facility
        if update_in.notes:
            referral.notes = f"{referral.notes or ''}\n[{now.isoformat()}] {update_in.notes}".strip()

        db.commit()
        db.refresh(referral)
        return referral


referral_service = ReferralService()
