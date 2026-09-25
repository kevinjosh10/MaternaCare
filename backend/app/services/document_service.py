import hashlib
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.lab import LabResult
from app.schemas.document import DocumentCreate, DocumentVerifyRequest


class DocumentService:

    @staticmethod
    def calculate_file_hash(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    @staticmethod
    def upload_document(db: Session, doc_in: DocumentCreate) -> Document:
        # Crucial medical safety requirement:
        # Never automatically mark extracted medical information as verified.
        doc_data = doc_in.model_dump()
        doc_data["verification_status"] = "PENDING"
        doc_data["verified_by"] = None
        doc_data["verified_at"] = None

        doc = Document(**doc_data)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc

    @staticmethod
    def get_document(db: Session, document_id: str) -> Optional[Document]:
        return db.query(Document).filter(Document.document_id == document_id).first()

    @staticmethod
    def get_patient_documents(db: Session, patient_id: str) -> List[Document]:
        return db.query(Document).filter(Document.patient_id == patient_id).order_by(Document.upload_date.desc()).all()

    @staticmethod
    def verify_document(db: Session, document_id: str, verify_req: DocumentVerifyRequest) -> Optional[Document]:
        """
        HUMAN-IN-THE-LOOP VERIFICATION STEP:
        Only an authorized clinician or health worker can mark extracted data as verified.
        Once verified, candidate data is committed as trusted clinical history.
        """
        doc = db.query(Document).filter(Document.document_id == document_id).first()
        if not doc:
            return None

        doc.verification_status = verify_req.verification_status
        doc.verified_by = verify_req.verified_by
        doc.verified_at = datetime.now(timezone.utc)
        if verify_req.notes:
            doc.notes = verify_req.notes
        if verify_req.corrected_data:
            doc.extracted_data = verify_req.corrected_data

        # If document is a verified Lab Report, sync structured data into trusted LabResult table
        if verify_req.verification_status == "VERIFIED" and doc.document_type == "LAB_REPORT":
            labs_data = doc.extracted_data.get("labs", [])
            for lab_item in labs_data:
                lab = LabResult(
                    patient_id=doc.patient_id,
                    pregnancy_id=doc.pregnancy_id,
                    test_date=datetime.now(timezone.utc).date(),
                    test_name=lab_item.get("test_name", "Extracted Lab"),
                    test_category=lab_item.get("test_category", "BIOCHEMISTRY"),
                    result=str(lab_item.get("result", "")),
                    unit=lab_item.get("unit"),
                    reference_range=lab_item.get("reference_range"),
                    abnormal_flag=bool(lab_item.get("abnormal_flag", False)),
                    lab_name=lab_item.get("lab_name", "Verified from Document"),
                    report_document=doc.file_url,
                    verified_by=verify_req.verified_by,
                    verification_status="VERIFIED"
                )
                db.add(lab)

        db.commit()
        db.refresh(doc)
        return doc


document_service = DocumentService()
