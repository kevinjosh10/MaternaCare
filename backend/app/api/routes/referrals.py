from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.audit import AuditLog
from app.schemas.referral import ReferralCreate, ReferralStatusUpdate, ReferralResponse
from app.services.referral_service import referral_service

router = APIRouter(prefix="/referrals", tags=["Emergency Referrals & Transfer"])


@router.post("", response_model=ReferralResponse, status_code=status.HTTP_201_CREATED)
def create_referral(
    referral_in: ReferralCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE, UserRole.REFERRAL_COORDINATOR]))
):
    referral = referral_service.create_referral(db, referral_in)

    db.add(AuditLog(
        user_id=current_user.id,
        role=current_user.role,
        action="REFERRAL_CREATED",
        patient_id=referral.patient_id,
        resource="REFERRAL",
        new_value={"referral_id": referral.referral_id, "risk": referral.risk_level, "source": referral.source_facility}
    ))
    db.commit()
    return referral


@router.get("/{referral_id}", response_model=ReferralResponse)
def get_referral(
    referral_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    referral = referral_service.get_referral(db, referral_id)
    if not referral:
        raise HTTPException(status_code=404, detail="Referral record not found")
    return referral


@router.get("/patient/{patient_id}", response_model=List[ReferralResponse])
def get_patient_referrals(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return referral_service.get_patient_referrals(db, patient_id)


@router.patch("/{referral_id}/status", response_model=ReferralResponse)
def update_referral_status(
    referral_id: str,
    status_update: ReferralStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.REFERRAL_COORDINATOR, UserRole.FACILITY_USER]))
):
    referral = referral_service.update_referral_status(db, referral_id, status_update)
    if not referral:
        raise HTTPException(status_code=404, detail="Referral not found")

    db.add(AuditLog(
        user_id=current_user.id,
        role=current_user.role,
        action="REFERRAL_UPDATED",
        patient_id=referral.patient_id,
        resource="REFERRAL",
        new_value={"status": referral.referral_status, "transport": referral.transport_status}
    ))
    db.commit()
    return referral
