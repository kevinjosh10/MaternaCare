from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.delivery import Delivery
from app.models.pregnancy import Pregnancy
from app.schemas.delivery import DeliveryCreate, DeliveryResponse

router = APIRouter(prefix="/deliveries", tags=["Delivery & Labour"])


@router.post("", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
def record_delivery(
    delivery_in: DeliveryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE]))
):
    delivery = Delivery(**delivery_in.model_dump())
    db.add(delivery)
    
    # Update pregnancy status to DELIVERED
    preg = db.query(Pregnancy).filter(Pregnancy.pregnancy_id == delivery.pregnancy_id).first()
    if preg:
        preg.status = "DELIVERED"

    db.commit()
    db.refresh(delivery)
    return delivery


@router.get("/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(
    delivery_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delivery = db.query(Delivery).filter(Delivery.delivery_id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery record not found")
    return delivery
