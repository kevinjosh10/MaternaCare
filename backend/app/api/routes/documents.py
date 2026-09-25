from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.audit import AuditLog
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentVerifyRequest
from app.services.document_service import document_service

router = APIRouter(prefix="/documents", tags=["Document Intelligence & Verification"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    doc_in: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = document_service.upload_document(db, doc_in)

    db.add(AuditLog(
        user_id=current_user.id,
        role=current_user.role,
        action="DOCUMENT_UPLOADED",
        patient_id=doc.patient_id,
        resource="DOCUMENT",
        new_value={"document_id": doc.document_id, "type": doc.document_type}
    ))
    db.commit()
    return doc


@router.get("/patient/{patient_id}", response_model=List[DocumentResponse])
def get_patient_documents(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return document_service.get_patient_documents(db, patient_id)


@router.post("/{document_id}/verify", response_model=DocumentResponse)
def verify_document_extraction(
    document_id: str,
    verify_req: DocumentVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.DOCTOR, UserRole.NURSE, UserRole.MIDWIFE]))
):
    """
    Human-in-the-loop verification step.
    Extracted document information must be verified by an authorized healthcare worker
    before becoming trusted clinical history.
    """
    doc = document_service.verify_document(db, document_id, verify_req)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    db.add(AuditLog(
        user_id=current_user.id,
        role=current_user.role,
        action="EXTRACTION_VERIFIED",
        patient_id=doc.patient_id,
        resource="DOCUMENT",
        new_value={"document_id": doc.document_id, "status": doc.verification_status, "verified_by": doc.verified_by}
    ))
    db.commit()
    return doc
