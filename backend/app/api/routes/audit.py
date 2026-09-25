from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import require_roles
from app.models.user import UserRole
from app.models.audit import AuditLog
from pydantic import BaseModel
from datetime import datetime


class AuditLogResponse(BaseModel):
    audit_id: str
    user_id: str
    role: str
    action: str
    patient_id: Optional[str] = None
    timestamp: datetime
    resource: str
    old_value: Optional[dict] = None
    new_value: Optional[dict] = None
    device_metadata: Optional[dict] = None

    class Config:
        from_attributes = True


router = APIRouter(prefix="/audit-logs", tags=["Audit Log & Governance"])


@router.get("", response_model=List[AuditLogResponse])
def get_audit_logs(
    patient_id: Optional[str] = Query(None, description="Filter logs for specific patient"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([UserRole.ADMIN, UserRole.DOCTOR, UserRole.REFERRAL_COORDINATOR]))
):
    q = db.query(AuditLog)
    if patient_id:
        q = q.filter(AuditLog.patient_id == patient_id)
    return q.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
