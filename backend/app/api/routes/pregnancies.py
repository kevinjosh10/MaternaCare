from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.pregnancy import Pregnancy
from app.models.patient import Patient
from app.schemas.pregnancy import PregnancyCreate, PregnancyUpdate, PregnancyResponse

router = APIRouter(prefix="/pregnancies", tags=["Pregnancy Management"])


@router.post("", response_model=PregnancyResponse, status_code=status.HTTP_201_CREATED)
def create_pregnancy(
    pregnancy_in: PregnancyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE]))
):
    patient = db.query(Patient).filter(Patient.patient_id == pregnancy_in.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    pregnancy = Pregnancy(**pregnancy_in.model_dump())
    db.add(pregnancy)
    db.commit()
    db.refresh(pregnancy)
    return pregnancy


@router.get("/{pregnancy_id}", response_model=PregnancyResponse)
def get_pregnancy(
    pregnancy_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pregnancy = db.query(Pregnancy).filter(Pregnancy.pregnancy_id == pregnancy_id).first()
    if not pregnancy:
        raise HTTPException(status_code=404, detail="Pregnancy record not found")
    return pregnancy


@router.get("/patient/{patient_id}", response_model=List[PregnancyResponse])
def get_patient_pregnancies(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Pregnancy).filter(Pregnancy.patient_id == patient_id).order_by(Pregnancy.pregnancy_number.desc()).all()


@router.put("/{pregnancy_id}", response_model=PregnancyResponse)
def update_pregnancy(
    pregnancy_id: str,
    update_in: PregnancyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE]))
):
    pregnancy = db.query(Pregnancy).filter(Pregnancy.pregnancy_id == pregnancy_id).first()
    if not pregnancy:
        raise HTTPException(status_code=404, detail="Pregnancy record not found")

    for key, val in update_in.model_dump(exclude_unset=True).items():
        setattr(pregnancy, key, val)

    db.commit()
    db.refresh(pregnancy)
    return pregnancy
