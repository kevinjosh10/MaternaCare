import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_patient_and_pregnancy_lifecycle():
    # 1. Create Patient
    patient_payload = {
        "name": "Ananya Sharma",
        "date_of_birth": "1998-05-12",
        "age": 28,
        "sex": "Female",
        "phone": "+91 9123456780",
        "address": "Gomti Nagar, Sector 4",
        "district": "Lucknow",
        "state": "Uttar Pradesh",
        "preferred_language": "hi",
        "emergency_contact": {"name": "Vikram Sharma", "relation": "Husband", "phone": "+91 9123456789"},
        "blood_group": "O+",
        "marital_status": "Married"
    }
    pat_res = client.post("/api/v1/patients", json=patient_payload)
    assert pat_res.status_code == 201
    pat_data = pat_res.json()
    patient_id = pat_data["patient_id"]
    assert pat_data["name"] == "Ananya Sharma"

    # 2. Retrieve Patient
    get_res = client.get(f"/api/v1/patients/{patient_id}")
    assert get_res.status_code == 200
    assert get_res.json()["district"] == "Lucknow"

    # 3. Add Obstetric History
    obs_payload = {
        "previous_pregnancies": 1,
        "previous_live_births": 1,
        "previous_abortions": 0,
        "previous_c_sections": 0,
        "previous_vaginal_deliveries": 1,
        "previous_preeclampsia": False
    }
    obs_res = client.post(f"/api/v1/patients/{patient_id}/history", json=obs_payload)
    assert obs_res.status_code == 200

    # 4. Register Pregnancy
    preg_payload = {
        "patient_id": patient_id,
        "pregnancy_number": 2,
        "gravida": 2,
        "para": 1,
        "living_children": 1,
        "gestational_age": 14.2,
        "high_risk_flag": False
    }
    preg_res = client.post("/api/v1/pregnancies", json=preg_payload)
    assert preg_res.status_code == 201
    preg_data = preg_res.json()
    assert preg_data["gravida"] == 2
