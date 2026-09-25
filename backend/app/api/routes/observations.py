from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.observation import Observation
from app.schemas.observation import ObservationCreate, ObservationResponse

router = APIRouter(prefix="/observations", tags=["Time-Series Observations"])


@router.post("", response_model=ObservationResponse, status_code=status.HTTP_201_CREATED)
def create_observation(
    obs_in: ObservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE, UserRole.HEALTH_WORKER]))
):
    obs = Observation(
        **obs_in.model_dump(),
        recorded_by=obs_in.recorded_by or current_user.full_name
    )
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs


@router.get("/patient/{patient_id}", response_model=List[ObservationResponse])
def get_patient_observations(
    patient_id: str,
    observation_type: Optional[str] = Query(None, description="Filter by type, e.g. systolic_bp, weight, glucose"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    q = db.query(Observation).filter(Observation.patient_id == patient_id)
    if observation_type:
        q = q.filter(Observation.observation_type == observation_type)
    return q.order_by(Observation.timestamp.asc()).all()
