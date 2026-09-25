from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.ultrasound import UltrasoundRecord
from app.models.pregnancy import Pregnancy
from app.schemas.ultrasound import UltrasoundCreate, UltrasoundResponse

router = APIRouter(prefix="/ultrasounds", tags=["Ultrasound Imaging"])


@router.post("", response_model=UltrasoundResponse, status_code=status.HTTP_201_CREATED)
def record_ultrasound(
    us_in: UltrasoundCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE]))
):
    pregnancy = db.query(Pregnancy).filter(Pregnancy.pregnancy_id == us_in.pregnancy_id).first()
    if not pregnancy:
        raise HTTPException(status_code=404, detail="Pregnancy not found")

    us = UltrasoundRecord(**us_in.model_dump())
    db.add(us)
    db.commit()
    db.refresh(us)
    return us


@router.get("/pregnancy/{pregnancy_id}", response_model=List[UltrasoundResponse])
def get_pregnancy_ultrasounds(
    pregnancy_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(UltrasoundRecord).filter(UltrasoundRecord.pregnancy_id == pregnancy_id).order_by(UltrasoundRecord.scan_date.asc()).all()
