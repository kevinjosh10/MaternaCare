from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.postpartum import PostpartumVisit
from app.schemas.postpartum import PostpartumVisitCreate, PostpartumVisitResponse

router = APIRouter(prefix="/postpartum-visits", tags=["Postpartum Mother Care"])


@router.post("", response_model=PostpartumVisitResponse, status_code=status.HTTP_201_CREATED)
def record_postpartum_visit(
    visit_in: PostpartumVisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE, UserRole.HEALTH_WORKER]))
):
    pv = PostpartumVisit(**visit_in.model_dump())
    db.add(pv)
    db.commit()
    db.refresh(pv)
    return pv


@router.get("/patient/{patient_id}", response_model=List[PostpartumVisitResponse])
def get_patient_postpartum_visits(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(PostpartumVisit).filter(PostpartumVisit.patient_id == patient_id).order_by(PostpartumVisit.visit_date.asc()).all()
