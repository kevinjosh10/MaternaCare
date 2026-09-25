import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_risk_assessment_and_referral_state_machine():
    # Setup patient
    pat = client.post("/api/v1/patients", json={
        "name": "Kavita Yadav",
        "age": 27,
        "sex": "Female",
        "phone": "+91 9776655443",
        "district": "Varanasi",
        "state": "Uttar Pradesh"
    }).json()
    patient_id = pat["patient_id"]

    preg = client.post("/api/v1/pregnancies", json={
        "patient_id": patient_id,
        "pregnancy_number": 1,
        "gestational_age": 34.0,
        "high_risk_flag": True,
        "high_risk_reason": "Severe headache and elevated BP"
    }).json()
    pregnancy_id = preg["pregnancy_id"]

    # Log high BP observation
    client.post("/api/v1/observations", json={
        "patient_id": patient_id,
        "pregnancy_id": pregnancy_id,
        "observation_type": "systolic_bp",
        "value": 165.0,
        "unit": "mmHg"
    })
    client.post("/api/v1/observations", json={
        "patient_id": patient_id,
        "pregnancy_id": pregnancy_id,
        "observation_type": "diastolic_bp",
        "value": 112.0,
        "unit": "mmHg"
    })

    # Log warning symptom
    client.post("/api/v1/symptoms", json={
        "patient_id": patient_id,
        "pregnancy_id": pregnancy_id,
        "symptom_type": "HEADACHE",
        "severity": "CRITICAL"
    })

    # 1. Trigger AI Risk Assessment
    risk_res = client.post(f"/api/v1/risk-assessments?patient_id={patient_id}&pregnancy_id={pregnancy_id}")
    assert risk_res.status_code == 201
    risk_data = risk_res.json()
    assessment_id = risk_data["assessment_id"]
    assert risk_data["risk_level"] == "CRITICAL"
    # Verify standard medical phrasing requirement
    assert "Potentially concerning pattern detected — clinical review recommended." in risk_data["explanation"]

    # 2. Get SHAP-ready Explainability features
    exp_res = client.get(f"/api/v1/risk-assessments/{assessment_id}/explanation")
    assert exp_res.status_code == 200
    exps = exp_res.json()
    assert len(exps) >= 1
    assert "contribution" in exps[0]
    assert "direction" in exps[0]

    # 3. Clinician Review of Risk Assessment
    review_res = client.patch(f"/api/v1/risk-assessments/{assessment_id}/review", json={
        "clinician_review_status": "REVIEWED_AGREED",
        "clinician_notes": "Urgent magnesium sulfate loading and tertiary referral indicated."
    })
    assert review_res.status_code == 200
    assert review_res.json()["clinician_review_status"] == "REVIEWED_AGREED"

    # 4. Create Emergency Referral
    ref_payload = {
        "patient_id": patient_id,
        "pregnancy_id": pregnancy_id,
        "created_by": "Dr. Sharma",
        "reason": "Severe Preeclampsia at 34 weeks",
        "risk_level": "CRITICAL",
        "clinical_summary": "BP 165/112 mmHg with persistent severe frontal headache.",
        "source_facility": "Community Health Centre Arajiline",
        "destination_facility": "District Women's Hospital Varanasi",
        "transport_status": "AMBULANCE_REQUESTED"
    }
    ref_res = client.post("/api/v1/referrals", json=ref_payload)
    assert ref_res.status_code == 201
    referral_id = ref_res.json()["referral_id"]
    assert ref_res.json()["referral_status"] == "CREATED"

    # 5. State Machine Progressions: ACKNOWLEDGED -> TRANSFER_IN_PROGRESS -> ARRIVED -> COMPLETED
    ack_res = client.patch(f"/api/v1/referrals/{referral_id}/status", json={
        "referral_status": "ACKNOWLEDGED",
        "transport_status": "AMBULANCE_DISPATCHED"
    })
    assert ack_res.status_code == 200
    assert ack_res.json()["referral_status"] == "ACKNOWLEDGED"

    done_res = client.patch(f"/api/v1/referrals/{referral_id}/status", json={
        "referral_status": "COMPLETED",
        "transport_status": "ARRIVED",
        "notes": "Patient admitted safely to tertiary obstetric ICU."
    })
    assert done_res.status_code == 200
    assert done_res.json()["referral_status"] == "COMPLETED"
