from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.lab import LabResult
from app.schemas.lab import LabResultCreate, LabResultResponse, LabVerificationUpdate

router = APIRouter(prefix="/labs", tags=["Laboratory Results"])


@router.post("", response_model=LabResultResponse, status_code=status.HTTP_201_CREATED)
def record_lab_result(
    lab_in: LabResultCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE, UserRole.HEALTH_WORKER]))
):
    lab = LabResult(**lab_in.model_dump())
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return lab


@router.get("/patient/{patient_id}", response_model=List[LabResultResponse])
def get_patient_labs(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(LabResult).filter(LabResult.patient_id == patient_id).order_by(LabResult.test_date.desc()).all()


@router.patch("/{test_id}/verify", response_model=LabResultResponse)
def verify_lab_result(
    test_id: str,
    verify_in: LabVerificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE]))
):
    lab = db.query(LabResult).filter(LabResult.test_id == test_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab test not found")

    lab.verification_status = verify_in.verification_status
    lab.verified_by = verify_in.verified_by or current_user.full_name
    db.commit()
    db.refresh(lab)
    return lab
