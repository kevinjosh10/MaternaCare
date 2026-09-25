"""
MaternaCare Model 4: Dedicated Standalone Microservice.
Exposes REST API endpoints for the Main Medical Brain.
Communicates with Model 1 (Translation), Model 2 (STT/TTS), Model 5 (OCR), and the Vercel Hospital Dashboard.
"""

from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status, Query, APIRouter
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import logging

from app.medical_brain.catalog import MASTER_TESTS_CATALOG, get_test_by_id, get_tests_by_stage, LifeStage
from app.medical_brain.past_history_analyzer import (
    PastObstetricHistoryProfile, past_history_analyzer, HistoryAnalysisReport
)
from app.medical_brain.brain_engine import (
    PatientClinicalContext, MedicalBrainAnalysisResponse,
    HITLApprovalStatus, medical_brain
)
from app.medical_brain.train_brain import train_medical_brain

logger = logging.getLogger("model4_microservice")

# In-memory store for pending doctor approvals (can sync with database or Vercel dashboard webhook)
PENDING_APPROVALS_DB: Dict[str, MedicalBrainAnalysisResponse] = {}

router = APIRouter(prefix="/medical-brain", tags=["Model 4: Main Medical Brain"])


class DoctorApprovalPayload(BaseModel):
    analysis_id: str
    decision: str = Field(..., example="APPROVED")  # "APPROVED", "EDITED", "REJECTED"
    doctor_name: str = Field(..., example="Dr. Priya Patel (Senior Obstetrician)")
    edited_advice: Optional[str] = None
    doctor_notes: Optional[str] = None


@router.get("/health")
def model4_health_check():
    return {
        "model_name": "Model 4: Main Medical Brain (Clinical Reasoning Core)",
        "status": "OPERATIONAL",
        "supported_test_parameters": len(MASTER_TESTS_CATALOG),
        "guidelines": "FOGSI, DIPSI, MoHFW, WHO, ACOG",
        "human_in_the_loop_active": True
    }


@router.get("/catalog", response_model=Dict[int, Dict[str, Any]])
def get_master_diagnostic_catalog(stage: Optional[LifeStage] = None):
    """
    Returns the complete master list of 122 medical tests for mother and child,
    including reference ranges, specimen types, and Indian clinical protocols.
    """
    if stage:
        return {k: v for k, v in MASTER_TESTS_CATALOG.items() if v["stage"] == stage}
    return MASTER_TESTS_CATALOG


@router.get("/catalog/{test_id}", response_model=Dict[str, Any])
def get_test_details(test_id: int):
    test = get_test_by_id(test_id)
    if not test:
        raise HTTPException(status_code=404, detail=f"Test ID {test_id} not found in 122 Master Catalog.")
    return test


@router.post("/analyze-history", response_model=HistoryAnalysisReport)
def analyze_previous_pregnancy_issues(profile: PastObstetricHistoryProfile):
    """
    Evaluates what kind of problems the pregnant woman had in previous pregnancies
    (prior preeclampsia, GDM, prior CS, PPH, preterm, stillbirth, Rh isoimmunization).
    Calculates recurrence risk and mandates specific tests from the 122 catalog.
    """
    return past_history_analyzer.analyze_history(profile)


@router.post("/analyze", response_model=MedicalBrainAnalysisResponse)
def analyze_patient_and_tests(context: PatientClinicalContext):
    """
    Core Model 4 Inference:
    Ingests patient history, test results (1 to 122), and current symptoms.
    Evaluates clinical patterns, recommends actions, and flags for Doctor HITL Approval
    if medicine, food, or remedies are recommended.
    """
    analysis = medical_brain.analyze_patient(context)

    # If pending doctor approval, store in pending queue for Vercel Hospital Dashboard
    if analysis.hitl_approval.status == "PENDING_APPROVAL":
        PENDING_APPROVALS_DB[analysis.analysis_id] = analysis
        logger.info(f"Analysis {analysis.analysis_id} sent to Doctor Approval Queue (Triggers: {analysis.hitl_approval.trigger_reasons})")

    return analysis


@router.get("/pending-approvals", response_model=List[MedicalBrainAnalysisResponse])
def get_pending_doctor_approvals():
    """
    Endpoint for Vercel Hospital Dashboard to fetch all pending advice requests awaiting doctor sign-off.
    """
    return list(PENDING_APPROVALS_DB.values())


@router.post("/review-approval", response_model=MedicalBrainAnalysisResponse)
def submit_doctor_approval(payload: DoctorApprovalPayload):
    """
    Human-In-The-Loop Callback:
    The doctor on the Vercel Dashboard approves, edits, or rejects proposed advice.
    """
    if payload.analysis_id not in PENDING_APPROVALS_DB:
        raise HTTPException(status_code=404, detail=f"Pending analysis ID {payload.analysis_id} not found.")

    record = PENDING_APPROVALS_DB[payload.analysis_id]
    now = datetime.now(timezone.utc)

    if payload.decision == "APPROVED":
        record.hitl_approval.status = "DOCTOR_APPROVED"
        approved_text_to_speak = record.patient_friendly_english
    elif payload.decision == "EDITED":
        record.hitl_approval.status = "DOCTOR_EDITED"
        if payload.edited_advice:
            record.medical_advice_english = payload.edited_advice
            record.patient_friendly_english = payload.edited_advice
            approved_text_to_speak = payload.edited_advice
    elif payload.decision == "REJECTED":
        record.hitl_approval.status = "DOCTOR_REJECTED"
        rejection_msg = "Please visit your doctor directly at the clinic for an in-person check-up."
        record.medical_advice_english = "Proposed advice rejected by clinician. Patient scheduled for direct in-person evaluation."
        record.patient_friendly_english = rejection_msg
        approved_text_to_speak = rejection_msg

    record.hitl_approval.doctor_notes = payload.doctor_notes
    record.hitl_approval.approved_by = payload.doctor_name
    record.hitl_approval.approved_at = now

    # Remove from pending queue
    del PENDING_APPROVALS_DB[payload.analysis_id]

    # --- NEW: Trigger Orchestrator to generate Voice Output based on Doctor's final word ---
    from app.ai_models.orchestrator import voice_orchestrator
    try:
        # Assuming English for now, but in reality, would map to patient's preferred language
        audio_result = voice_orchestrator.process_doctor_approved_response(approved_text_to_speak, language="en")
        # In a real app, this audio would be pushed to the patient's device via WebSocket or push notification.
        # Here we just attach it to the returned response.
        logger.info(f"Generated TTS for Doctor Approved text. Elapsed: {audio_result['elapsed_ms']}ms")
        
        # We can append it to the response model as a dynamic field or just return it in a wrapper.
        # Since MedicalBrainAnalysisResponse is strict, we'll log it. 
        # For full implementation, we'd add an audio_base64 field to the response model.
    except Exception as e:
        logger.error(f"Failed to generate post-approval TTS: {str(e)}")

    return record


@router.post("/train")
def trigger_training(epochs: int = Query(20, description="Training epochs")):
    """
    Triggers neural training loop on augmented Indian maternal-neonatal diagnostic dataset.
    """
    try:
        train_medical_brain(epochs=epochs, output_dir="./checkpoints")
        return {"status": "SUCCESS", "message": f"Trained Model 4 for {epochs} epochs on 122 diagnostic test parameters."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")
