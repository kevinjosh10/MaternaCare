from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.communication import Communication
from app.schemas.communication import CommunicationCreate, CommunicationResponse
from app.services.communication_service import communication_service

router = APIRouter(prefix="/communications", tags=["Emergency Communication & Dispatch"])


@router.post("", response_model=CommunicationResponse, status_code=status.HTTP_201_CREATED)
def send_communication(
    comm_in: CommunicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.REFERRAL_COORDINATOR]))
):
    return communication_service.send_communication(db, comm_in)


@router.get("/referral/{referral_id}", response_model=List[CommunicationResponse])
def get_referral_communications(
    referral_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return communication_service.get_referral_communications(db, referral_id)
