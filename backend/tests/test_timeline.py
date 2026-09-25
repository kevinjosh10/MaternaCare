import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_timeline_and_summary_continuity():
    # 1. Setup Patient
    pat = client.post("/api/v1/patients", json={
        "name": "Pooja Verma",
        "age": 23,
        "sex": "Female",
        "district": "Varanasi",
        "state": "Uttar Pradesh"
    }).json()
    patient_id = pat["patient_id"]

    preg = client.post("/api/v1/pregnancies", json={
        "patient_id": patient_id,
        "pregnancy_number": 1,
        "gestational_age": 39.0
    }).json()
    pregnancy_id = preg["pregnancy_id"]

    # 2. Add Delivery
    deliv = client.post("/api/v1/deliveries", json={
        "pregnancy_id": pregnancy_id,
        "patient_id": patient_id,
        "delivery_date": "2025-08-10",
        "delivery_mode": "SPONTANEOUS_VAGINAL",
        "gestational_age_at_delivery": 39.2,
        "blood_loss": 200.0
    }).json()
    delivery_id = deliv["delivery_id"]

    # 3. Add Newborn
    nb = client.post("/api/v1/newborns", json={
        "mother_patient_id": patient_id,
        "pregnancy_id": pregnancy_id,
        "delivery_id": delivery_id,
        "name": "Baby of Pooja",
        "sex": "Female",
        "date_of_birth": "2025-08-10",
        "birth_weight": 3050.0,
        "apgar_1_min": 8,
        "apgar_5_min": 9
    }).json()
    newborn_id = nb["newborn_id"]

    # 4. Add Newborn Visit
    client.post(f"/api/v1/newborns/{newborn_id}/visits", json={
        "newborn_id": newborn_id,
        "visit_date": "2025-08-13",
        "age_days": 3,
        "weight": 2980.0,
        "heart_rate": 138.0,
        "feeding": "Exclusive Breastfeeding"
    })

    # 5. Add Postpartum Visit
    client.post("/api/v1/postpartum-visits", json={
        "patient_id": patient_id,
        "delivery_id": delivery_id,
        "visit_date": "2025-08-13",
        "postpartum_day": 3,
        "systolic_bp": 118.0,
        "diastolic_bp": 76.0,
        "uterine_status": "Well contracted",
        "vaginal_bleeding": "Lochia Rubra normal"
    })

    # 6. Verify Longitudinal Timeline
    timeline_res = client.get(f"/api/v1/patients/{patient_id}/timeline")
    assert timeline_res.status_code == 200
    timeline_data = timeline_res.json()
    assert timeline_data["total_events"] >= 3
    event_types = [e["event_type"] for e in timeline_data["timeline"]]
    assert "DELIVERY" in event_types
    assert "NEWBORN_BIRTH" in event_types
    assert "POSTPARTUM_VISIT" in event_types

    # 7. Verify Unified Patient Summary
    summary_res = client.get(f"/api/v1/patients/{patient_id}/summary")
    assert summary_res.status_code == 200
    summary_data = summary_res.json()
    assert summary_data["delivery_status"] == "DELIVERED"
    assert len(summary_data["newborns"]) >= 1
    assert summary_data["newborns"][0]["name"] == "Baby of Pooja"
    assert summary_data["latest_postpartum_visit"]["postpartum_day"] == 3
