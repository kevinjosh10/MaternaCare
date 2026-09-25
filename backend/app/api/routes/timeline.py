from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.timeline import PatientTimelineResponse, PatientSummaryResponse
from app.services.timeline_service import timeline_service

router = APIRouter(prefix="/patients", tags=["Patient Health Memory: Timeline & Summary"])


@router.get("/{patient_id}/timeline", response_model=PatientTimelineResponse)
def get_patient_timeline(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Longitudinal Health Memory Interface:
    Combines chronological events from:
    - Previous Obstetric History
    - Pregnancy Registrations
    - ANC Visits
    - Time-series Vitals & Observations
    - Symptoms
    - Labs
    - Ultrasounds
    - Medications & Prescriptions
    - Documents
    - AI Risk Assessments
    - Emergency Referrals
    - Delivery Events
    - Newborn Births & Follow-up Visits
    - Postpartum Maternal Visits
    """
    res = timeline_service.get_patient_timeline(db, patient_id)
    if not res:
        raise HTTPException(status_code=404, detail="Patient not found")
    return res


@router.get("/{patient_id}/summary", response_model=PatientSummaryResponse)
def get_patient_summary(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Unified Patient Clinical Summary:
    Returns demographics, current pregnancy status, latest vital observations,
    recent symptoms, recent labs, latest AI risk assessment, active referrals,
    delivery status, newborn info, and latest postpartum status.
    """
    res = timeline_service.get_patient_summary(db, patient_id)
    if not res:
        raise HTTPException(status_code=404, detail="Patient not found")
    return res
