from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.facility import Facility
from app.schemas.facility import FacilityCreate, FacilityResponse

router = APIRouter(prefix="/facilities", tags=["Healthcare Facilities & GPS Directory"])


@router.post("", response_model=FacilityResponse, status_code=status.HTTP_201_CREATED)
def create_facility(
    facility_in: FacilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.REFERRAL_COORDINATOR]))
):
    facility = Facility(**facility_in.model_dump())
    db.add(facility)
    db.commit()
    db.refresh(facility)
    return facility


@router.get("", response_model=List[FacilityResponse])
def list_facilities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Facility).all()


@router.get("/{facility_id}", response_model=FacilityResponse)
def get_facility(
    facility_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    facility = db.query(Facility).filter(Facility.facility_id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    return facility
