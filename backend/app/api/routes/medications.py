from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.medication import MedicationRecord, SupplementRecord, VaccinationRecord
from app.schemas.medication import (
    MedicationCreate, MedicationResponse,
    SupplementCreate, SupplementResponse,
    VaccinationCreate, VaccinationResponse
)

router = APIRouter(tags=["Medications, Supplements & Vaccinations"])


# Medications
@router.post("/medications", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
def prescribe_medication(
    med_in: MedicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE]))
):
    med = MedicationRecord(
        **med_in.model_dump(),
        prescribed_by=med_in.prescribed_by or current_user.full_name
    )
    db.add(med)
    db.commit()
    db.refresh(med)
    return med


@router.get("/patients/{patient_id}/medications", response_model=List[MedicationResponse])
def get_patient_medications(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(MedicationRecord).filter(MedicationRecord.patient_id == patient_id).order_by(MedicationRecord.start_date.desc()).all()


# Supplements
@router.post("/supplements", response_model=SupplementResponse, status_code=status.HTTP_201_CREATED)
def prescribe_supplement(
    sup_in: SupplementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE, UserRole.HEALTH_WORKER]))
):
    sup = SupplementRecord(
        **sup_in.model_dump(),
        prescribed_by=sup_in.prescribed_by or current_user.full_name
    )
    db.add(sup)
    db.commit()
    db.refresh(sup)
    return sup


@router.get("/patients/{patient_id}/supplements", response_model=List[SupplementResponse])
def get_patient_supplements(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(SupplementRecord).filter(SupplementRecord.patient_id == patient_id).order_by(SupplementRecord.start_date.desc()).all()


# Vaccinations
@router.post("/vaccinations", response_model=VaccinationResponse, status_code=status.HTTP_201_CREATED)
def record_vaccination(
    vac_in: VaccinationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE, UserRole.HEALTH_WORKER]))
):
    vac = VaccinationRecord(
        **vac_in.model_dump(),
        provider=vac_in.provider or current_user.full_name
    )
    db.add(vac)
    db.commit()
    db.refresh(vac)
    return vac


@router.get("/patients/{patient_id}/vaccinations", response_model=List[VaccinationResponse])
def get_patient_vaccinations(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(VaccinationRecord).filter(VaccinationRecord.patient_id == patient_id).order_by(VaccinationRecord.date.asc()).all()
