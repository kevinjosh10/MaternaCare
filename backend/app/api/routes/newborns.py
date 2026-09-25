from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.newborn import Newborn, NewbornVisit
from app.schemas.newborn import (
    NewbornCreate, NewbornResponse,
    NewbornVisitCreate, NewbornVisitResponse
)

router = APIRouter(prefix="/newborns", tags=["Newborn & Follow-Up Care"])


@router.post("", response_model=NewbornResponse, status_code=status.HTTP_201_CREATED)
def register_newborn(
    newborn_in: NewbornCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE]))
):
    nb = Newborn(**newborn_in.model_dump())
    db.add(nb)
    db.commit()
    db.refresh(nb)
    return nb


@router.get("/{newborn_id}", response_model=NewbornResponse)
def get_newborn(
    newborn_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    nb = db.query(Newborn).filter(Newborn.newborn_id == newborn_id).first()
    if not nb:
        raise HTTPException(status_code=404, detail="Newborn record not found")
    return nb


@router.post("/{newborn_id}/visits", response_model=NewbornVisitResponse, status_code=status.HTTP_201_CREATED)
def record_newborn_visit(
    newborn_id: str,
    visit_in: NewbornVisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE, UserRole.HEALTH_WORKER]))
):
    nb = db.query(Newborn).filter(Newborn.newborn_id == newborn_id).first()
    if not nb:
        raise HTTPException(status_code=404, detail="Newborn record not found")

    visit = NewbornVisit(
        **visit_in.model_dump(exclude={"newborn_id"}),
        newborn_id=newborn_id
    )
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit


@router.get("/{newborn_id}/visits", response_model=List[NewbornVisitResponse])
def get_newborn_visits(
    newborn_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(NewbornVisit).filter(NewbornVisit.newborn_id == newborn_id).order_by(NewbornVisit.visit_date.asc()).all()
