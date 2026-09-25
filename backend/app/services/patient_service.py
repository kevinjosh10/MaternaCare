from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.models.history import ObstetricHistory, MedicalHistory
from app.schemas.patient import (
    PatientCreate, PatientUpdate,
    ObstetricHistoryCreate, MedicalHistoryCreate
)


class PatientService:

    @staticmethod
    def get_patient(db: Session, patient_id: str) -> Optional[Patient]:
        return db.query(Patient).filter(Patient.patient_id == patient_id).first()

    @staticmethod
    def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
        return db.query(Patient).offset(skip).limit(limit).all()

    @staticmethod
    def create_patient(db: Session, patient_in: PatientCreate) -> Patient:
        patient_data = patient_in.model_dump()
        emergency_contact = patient_data.pop("emergency_contact", None)
        patient = Patient(
            **patient_data,
            emergency_contact=emergency_contact.model_dump() if emergency_contact else None
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient

    @staticmethod
    def update_patient(db: Session, patient_id: str, patient_update: PatientUpdate) -> Optional[Patient]:
        patient = PatientService.get_patient(db, patient_id)
        if not patient:
            return None
        update_data = patient_update.model_dump(exclude_unset=True)
        if "emergency_contact" in update_data and update_data["emergency_contact"]:
            update_data["emergency_contact"] = update_data["emergency_contact"].model_dump()
        for key, val in update_data.items():
            setattr(patient, key, val)
        db.commit()
        db.refresh(patient)
        return patient

    @staticmethod
    def set_obstetric_history(db: Session, patient_id: str, history_in: ObstetricHistoryCreate) -> ObstetricHistory:
        history = db.query(ObstetricHistory).filter(ObstetricHistory.patient_id == patient_id).first()
        if history:
            for key, val in history_in.model_dump().items():
                setattr(history, key, val)
        else:
            history = ObstetricHistory(patient_id=patient_id, **history_in.model_dump())
            db.add(history)
        db.commit()
        db.refresh(history)
        return history

    @staticmethod
    def get_obstetric_history(db: Session, patient_id: str) -> Optional[ObstetricHistory]:
        return db.query(ObstetricHistory).filter(ObstetricHistory.patient_id == patient_id).first()

    @staticmethod
    def set_medical_history(db: Session, patient_id: str, history_in: MedicalHistoryCreate) -> MedicalHistory:
        history = db.query(MedicalHistory).filter(MedicalHistory.patient_id == patient_id).first()
        if history:
            for key, val in history_in.model_dump().items():
                setattr(history, key, val)
        else:
            history = MedicalHistory(patient_id=patient_id, **history_in.model_dump())
            db.add(history)
        db.commit()
        db.refresh(history)
        return history

    @staticmethod
    def get_medical_history(db: Session, patient_id: str) -> Optional[MedicalHistory]:
        return db.query(MedicalHistory).filter(MedicalHistory.patient_id == patient_id).first()


patient_service = PatientService()
