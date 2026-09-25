from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.audit import AuditLog
from app.schemas.patient import (
    PatientCreate, PatientUpdate, PatientResponse,
    ObstetricHistoryCreate, ObstetricHistoryResponse,
    MedicalHistoryCreate, MedicalHistoryResponse
)
from app.services.patient_service import patient_service

router = APIRouter(prefix="/patients", tags=["Patient Demographics & History"])


@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient_in: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE, UserRole.HEALTH_WORKER]))
):
    patient = patient_service.create_patient(db, patient_in)
    db.add(AuditLog(
        user_id=current_user.id,
        role=current_user.role,
        action="PATIENT_CREATED",
        patient_id=patient.patient_id,
        resource="PATIENT",
        new_value={"name": patient.name, "phone": patient.phone}
    ))
    db.commit()
    return patient


@router.get("", response_model=List[PatientResponse])
def list_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return patient_service.get_patients(db, skip, limit)


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = patient_service.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Audit patient access
    db.add(AuditLog(
        user_id=current_user.id,
        role=current_user.role,
        action="PATIENT_VIEWED",
        patient_id=patient.patient_id,
        resource="PATIENT"
    ))
    db.commit()
    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: str,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE, UserRole.HEALTH_WORKER]))
):
    patient = patient_service.update_patient(db, patient_id, patient_update)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.add(AuditLog(
        user_id=current_user.id,
        role=current_user.role,
        action="RECORD_UPDATED",
        patient_id=patient_id,
        resource="PATIENT",
        new_value=patient_update.model_dump(exclude_unset=True)
    ))
    db.commit()
    return patient


@router.post("/{patient_id}/history", response_model=ObstetricHistoryResponse)
def set_obstetric_history(
    patient_id: str,
    history_in: ObstetricHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE]))
):
    patient = patient_service.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_service.set_obstetric_history(db, patient_id, history_in)


@router.get("/{patient_id}/history", response_model=ObstetricHistoryResponse)
def get_obstetric_history(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history = patient_service.get_obstetric_history(db, patient_id)
    if not history:
        raise HTTPException(status_code=404, detail="Obstetric history not found for this patient")
    return history


@router.post("/{patient_id}/medical-history", response_model=MedicalHistoryResponse)
def set_medical_history(
    patient_id: str,
    history_in: MedicalHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE]))
):
    patient = patient_service.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_service.set_medical_history(db, patient_id, history_in)


@router.get("/{patient_id}/medical-history", response_model=MedicalHistoryResponse)
def get_medical_history(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history = patient_service.get_medical_history(db, patient_id)
    if not history:
        raise HTTPException(status_code=404, detail="Medical history not found for this patient")
    return history
