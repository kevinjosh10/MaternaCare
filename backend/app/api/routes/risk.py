from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.audit import AuditLog
from app.models.risk import RiskAssessment, ExplanationFeature
from app.schemas.risk import (
    RiskAssessmentResponse, ExplanationFeatureResponse,
    ClinicianReviewUpdate
)
from app.services.risk_service import risk_service

router = APIRouter(prefix="/risk-assessments", tags=["Clinical Risk Intelligence & Explainability"])


@router.post("", response_model=RiskAssessmentResponse, status_code=status.HTTP_201_CREATED)
def trigger_risk_assessment(
    patient_id: str = Query(..., description="Target patient ID"),
    pregnancy_id: Optional[str] = Query(None, description="Optional pregnancy ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE, UserRole.HEALTH_WORKER]))
):
    """
    Evaluates concerning clinical patterns using configurable WHO/national protocols.
    Important: AI does NOT diagnose. Flags 'Potentially concerning pattern detected — clinical review recommended.'
    """
    assessment = risk_service.evaluate_maternal_risk(db, patient_id=patient_id, pregnancy_id=pregnancy_id)

    db.add(AuditLog(
        user_id=current_user.id,
        role=current_user.role,
        action="AI_ASSESSMENT_GENERATED",
        patient_id=patient_id,
        resource="RISK_ASSESSMENT",
        new_value={"assessment_id": assessment.assessment_id, "risk_level": assessment.risk_level, "score": assessment.risk_score}
    ))
    db.commit()
    return assessment


@router.get("/{assessment_id}", response_model=RiskAssessmentResponse)
def get_risk_assessment(
    assessment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assessment = risk_service.get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Risk assessment record not found")
    return assessment


@router.get("/{assessment_id}/explanation", response_model=List[ExplanationFeatureResponse])
def get_assessment_explanation(
    assessment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    SHAP-ready feature contribution and ranking endpoint for explainable clinical AI.
    """
    assessment = risk_service.get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Risk assessment record not found")
    return db.query(ExplanationFeature).filter(ExplanationFeature.assessment_id == assessment_id).order_by(ExplanationFeature.rank.asc()).all()


@router.patch("/{assessment_id}/review", response_model=RiskAssessmentResponse)
def clinician_review_assessment(
    assessment_id: str,
    review_in: ClinicianReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE]))
):
    """
    Human-in-the-loop clinical review and override endpoint.
    """
    assessment = risk_service.review_assessment(db, assessment_id, review_in)
    if not assessment:
        raise HTTPException(status_code=404, detail="Risk assessment record not found")

    db.add(AuditLog(
        user_id=current_user.id,
        role=current_user.role,
        action="AI_ASSESSMENT_REVIEWED",
        patient_id=assessment.patient_id,
        resource="RISK_ASSESSMENT",
        new_value={"status": review_in.clinician_review_status, "clinician": current_user.full_name}
    ))
    db.commit()
    return assessment
