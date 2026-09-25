import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_clinical_data_recording_and_verification():
    # Setup patient & pregnancy
    pat = client.post("/api/v1/patients", json={
        "name": "Meera Patel",
        "age": 25,
        "sex": "Female",
        "phone": "+91 9988776655",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "preferred_language": "hi"
    }).json()
    patient_id = pat["patient_id"]

    preg = client.post("/api/v1/pregnancies", json={
        "patient_id": patient_id,
        "pregnancy_number": 1,
        "gravida": 1,
        "para": 0,
        "gestational_age": 28.0
    }).json()
    pregnancy_id = preg["pregnancy_id"]

    # 1. Antenatal Care Visit
    visit_res = client.post(f"/api/v1/pregnancies/{pregnancy_id}/visits", json={
        "pregnancy_id": pregnancy_id,
        "patient_id": patient_id,
        "visit_date": "2025-06-15",
        "gestational_age": 28.0,
        "systolic_bp": 122.0,
        "diastolic_bp": 78.0,
        "pulse": 82.0,
        "weight": 58.5,
        "fetal_heart_rate": 142.0,
        "fundal_height": 28.0,
        "fetal_movement": "Normal",
        "symptoms": ["Mild backache"]
    })
    assert visit_res.status_code == 201

    # 2. Time-series observation check
    obs_res = client.get(f"/api/v1/observations/patient/{patient_id}?observation_type=systolic_bp")
    assert obs_res.status_code == 200
    assert len(obs_res.json()) >= 1
    assert obs_res.json()[0]["value"] == 122.0

    # 3. Lab Result Recording & Verification
    lab_res = client.post("/api/v1/labs", json={
        "patient_id": patient_id,
        "pregnancy_id": pregnancy_id,
        "test_date": "2025-06-15",
        "test_name": "Hemoglobin",
        "test_category": "HEMATOLOGY",
        "result": "11.2",
        "unit": "g/dL",
        "reference_range": "11.0-15.0"
    })
    assert lab_res.status_code == 201
    lab_id = lab_res.json()["test_id"]

    # Verify Lab Result
    verify_res = client.patch(f"/api/v1/labs/{lab_id}/verify", json={
        "verification_status": "VERIFIED",
        "verified_by": "Dr. Sunita Sharma"
    })
    assert verify_res.status_code == 200
    assert verify_res.json()["verification_status"] == "VERIFIED"

    # 4. Document Human-in-the-Loop Verification
    doc_res = client.post("/api/v1/documents", json={
        "patient_id": patient_id,
        "pregnancy_id": pregnancy_id,
        "document_type": "LAB_REPORT",
        "file_url": "https://storage.maternacare.org/docs/lab_scan_101.pdf",
        "extracted_data": {"labs": [{"test_name": "Blood Sugar Fasting", "result": "88", "unit": "mg/dL"}]},
        "extraction_confidence": 0.94
    })
    assert doc_res.status_code == 201
    doc_id = doc_res.json()["document_id"]
    assert doc_res.json()["verification_status"] == "PENDING"  # Must NOT be automatically verified

    # Doctor verifies the document
    doc_ver = client.post(f"/api/v1/documents/{doc_id}/verify", json={
        "verification_status": "VERIFIED",
        "verified_by": "Dr. Sunita Sharma (Obstetrician)",
        "notes": "Verified against laboratory original printout"
    })
    assert doc_ver.status_code == 200
    assert doc_ver.json()["verification_status"] == "VERIFIED"
