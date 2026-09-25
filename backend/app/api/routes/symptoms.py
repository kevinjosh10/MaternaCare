from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.symptom import Symptom
from app.schemas.symptom import SymptomCreate, SymptomResponse

router = APIRouter(prefix="/symptoms", tags=["Symptom Tracking"])


@router.post("", response_model=SymptomResponse, status_code=status.HTTP_201_CREATED)
def record_symptom(
    sym_in: SymptomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sym = Symptom(
        **sym_in.model_dump(),
        reported_by=sym_in.reported_by or current_user.full_name
    )
    db.add(sym)
    db.commit()
    db.refresh(sym)
    return sym


@router.get("/patient/{patient_id}", response_model=List[SymptomResponse])
def get_patient_symptoms(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Symptom).filter(Symptom.patient_id == patient_id).order_by(Symptom.date_time.desc()).all()
