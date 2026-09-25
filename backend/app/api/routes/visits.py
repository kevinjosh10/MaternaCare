from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.visit import AntenatalVisit
from app.models.pregnancy import Pregnancy
from app.models.observation import Observation
from app.schemas.visit import AntenatalVisitCreate, AntenatalVisitResponse

router = APIRouter(prefix="/pregnancies", tags=["Antenatal Care Visits"])


@router.post("/{pregnancy_id}/visits", response_model=AntenatalVisitResponse, status_code=status.HTTP_201_CREATED)
def create_antenatal_visit(
    pregnancy_id: str,
    visit_in: AntenatalVisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE, UserRole.HEALTH_WORKER]))
):
    pregnancy = db.query(Pregnancy).filter(Pregnancy.pregnancy_id == pregnancy_id).first()
    if not pregnancy:
        raise HTTPException(status_code=404, detail="Pregnancy not found")

    visit = AntenatalVisit(
        **visit_in.model_dump(exclude={"pregnancy_id"}),
        pregnancy_id=pregnancy_id,
        healthcare_worker=visit_in.healthcare_worker or current_user.full_name
    )
    db.add(visit)
    db.flush()

    # Time-series normalization: automatically log vitals to Observation table
    visit_time = datetime.combine(visit.visit_date, datetime.min.time())
    vital_mappings = [
        ("systolic_bp", visit.systolic_bp, "mmHg"),
        ("diastolic_bp", visit.diastolic_bp, "mmHg"),
        ("pulse", visit.pulse, "bpm"),
        ("temperature", visit.temperature, "°C"),
        ("oxygen_saturation", visit.oxygen_saturation, "%"),
        ("fetal_heart_rate", visit.fetal_heart_rate, "bpm"),
        ("fundal_height", visit.fundal_height, "cm"),
        ("weight", visit.weight, "kg"),
    ]

    for obs_type, val, unit in vital_mappings:
        if val is not None:
            db.add(Observation(
                patient_id=pregnancy.patient_id,
                pregnancy_id=pregnancy_id,
                timestamp=visit_time,
                observation_type=obs_type,
                value=float(val),
                unit=unit,
                source="ANC_VISIT",
                verified=True,
                recorded_by=current_user.full_name
            ))

    # Update pregnancy gestational age
    if visit.gestational_age:
        pregnancy.gestational_age = visit.gestational_age

    db.commit()
    db.refresh(visit)
    return visit


@router.get("/{pregnancy_id}/visits", response_model=List[AntenatalVisitResponse])
def get_antenatal_visits(
    pregnancy_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(AntenatalVisit).filter(AntenatalVisit.pregnancy_id == pregnancy_id).order_by(AntenatalVisit.visit_date.asc()).all()
