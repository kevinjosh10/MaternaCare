import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.medical_brain.catalog import MASTER_TESTS_CATALOG, get_test_by_id, LifeStage
from app.medical_brain.past_history_analyzer import PastObstetricHistoryProfile, past_history_analyzer
from app.medical_brain.brain_engine import PatientClinicalContext, TestResultInput, medical_brain
from app.medical_brain.microservice import PENDING_APPROVALS_DB, submit_doctor_approval, DoctorApprovalPayload

client = TestClient(app)


def test_master_catalog_122_parameters():
    """
    Validates that the complete master catalog of 122 medical tests is loaded
    and conforms to Indian clinical guidelines.
    """
    assert len(MASTER_TESTS_CATALOG) == 122

    # Check key representative tests across all life stages
    test_1 = get_test_by_id(1)
    assert test_1["name"] == "Urine Pregnancy Test (hCG)"
    assert test_1["stage"] == LifeStage.FIRST_TRIMESTER

    test_24 = get_test_by_id(24)
    assert "Uterine Artery Doppler" in test_24["name"]
    assert "FOGSI" in test_24["indian_clinical_protocol"]

    test_35 = get_test_by_id(35)
    assert "75g 2-Hour Oral Glucose Tolerance Test" in test_35["name"]
    assert "DIPSI" in test_35["indian_clinical_protocol"]

    test_44 = get_test_by_id(44)
    assert "Serial Antenatal Blood Pressure" in test_44["name"]

    test_69 = get_test_by_id(69)
    assert "Postpartum 75g 2-Hour Oral Glucose Tolerance Test" in test_69["name"]
    assert test_69["stage"] == LifeStage.POSTPARTUM_MOTHER

    test_80 = get_test_by_id(80)
    assert "Critical Congenital Heart Disease (CCHD)" in test_80["name"]
    assert test_80["stage"] == LifeStage.IMMEDIATE_NEWBORN

    test_90 = get_test_by_id(90)
    assert "Congenital Hypothyroidism" in test_90["name"]
    assert test_90["stage"] == LifeStage.GUTHRIE_IEM_PANEL

    test_122 = get_test_by_id(122)
    assert "Pediatric Oral Health Exam & Fluoride Varnish" in test_122["name"]
    assert test_122["stage"] == LifeStage.INFANCY_MONTHS_2_12


def test_past_obstetric_history_analyzer():
    """
    Tests evaluation of previous pregnancy issues (Prior preeclampsia, GDM, prior CS, PPH).
    """
    profile = PastObstetricHistoryProfile(
        gravida=3,
        para=1,
        living_children=1,
        abortions=1,
        previous_c_sections=1,
        inter_pregnancy_interval_months=14,
        prior_preeclampsia=True,
        prior_early_onset_preeclampsia=True,
        prior_gestational_diabetes=True,
        prior_postpartum_hemorrhage=False
    )
    report = past_history_analyzer.analyze_history(profile)

    assert report.is_high_risk_pregnancy is True
    assert report.risk_level == "HIGH"
    assert "G3 P1 L1 A1 S0" in report.gravida_para_status

    # Recurrence alerts
    alert_names = [a.complication_name for a in report.alerts]
    assert any("Preeclampsia" in name for name in alert_names)
    assert any("Gestational Diabetes" in name for name in alert_names)
    assert any("Uterine Scar" in name for name in alert_names)

    # Mandated preventive prescriptions
    presc_str = " ".join(report.preventive_prescriptions_indicated)
    assert "Aspirin 150 mg" in presc_str

    # Mandated surveillance tests
    all_mandated_test_ids = [tid for a in report.alerts for tid in a.mandated_tests]
    assert 24 in all_mandated_test_ids  # Uterine Artery Doppler
    assert 35 in all_mandated_test_ids  # 75g OGTT
    assert 44 in all_mandated_test_ids  # Serial BP monitoring


def test_medical_brain_analysis_and_hitl_approval_gate():
    """
    Tests Model 4 Main Medical Brain inference, clinical evaluation,
    and Human-In-The-Loop (HITL) doctor approval trigger.
    """
    context = PatientClinicalContext(
        patient_name="Meenakshi",
        age=29,
        gestational_age_weeks=32.4,
        past_history=PastObstetricHistoryProfile(
            gravida=2,
            para=1,
            prior_preeclampsia=True,
            previous_c_sections=1
        ),
        recent_symptoms=["Frontal throbbing headache", "Severe leg swelling"],
        current_query_text="I have a terrible headache and blurriness in my eyes",
        test_results=[
            TestResultInput(test_id=44, value="156/102 mmHg", is_abnormal=True),
            TestResultInput(test_id=45, value="UPCR 0.62 mg/mg (3+ protein)", is_abnormal=True),
            TestResultInput(test_id=46, value="sFlt-1/PlGF ratio 135", is_abnormal=True),
            TestResultInput(test_id=43, value="CPR 0.88 (< 1.0)", is_abnormal=True)
        ]
    )

    analysis = medical_brain.analyze_patient(context)

    # Clinical findings
    assert analysis.is_high_risk is True
    assert analysis.risk_level in ["HIGH", "CRITICAL"]
    assert analysis.referral_recommended is True
    assert len(analysis.abnormal_tests_detected) >= 4

    # Standard clinical phrasing
    assert "Potentially concerning pattern detected — clinical review recommended." in analysis.medical_advice_english

    # Human-In-The-Loop Check:
    # Because medical recommendations were made (Aspirin/Labetalol), it must require approval!
    assert analysis.hitl_approval.is_approval_required is True
    assert analysis.hitl_approval.status == "PENDING_APPROVAL"


def test_microservice_api_and_doctor_approval_workflow():
    """
    Tests REST API endpoints for Model 4:
    /api/v1/medical-brain/analyze -> PENDING_APPROVAL -> /api/v1/medical-brain/review-approval -> DOCTOR_APPROVED
    """
    payload = {
        "patient_name": "Ritu Sharma",
        "age": 28,
        "gestational_age_weeks": 34.0,
        "past_history": {
            "gravida": 2,
            "para": 1,
            "prior_preeclampsia": True
        },
        "recent_symptoms": ["headache"],
        "test_results": [
            {"test_id": 44, "value": "150/96 mmHg", "is_abnormal": True}
        ]
    }

    # 1. Trigger Model 4 Analysis
    res = client.post("/api/v1/medical-brain/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    analysis_id = data["analysis_id"]
    assert data["hitl_approval"]["status"] == "PENDING_APPROVAL"

    # 2. Check Pending Approvals Queue (for Vercel Hospital Dashboard)
    pending_res = client.get("/api/v1/medical-brain/pending-approvals")
    assert pending_res.status_code == 200
    pending_list = pending_res.json()
    assert any(p["analysis_id"] == analysis_id for p in pending_list)

    # 3. Doctor reviews & approves advice
    approval_payload = {
        "analysis_id": analysis_id,
        "decision": "APPROVED",
        "doctor_name": "Dr. Priya Patel (Senior Obstetrician)",
        "doctor_notes": "Reviewed labs and BP. Agreed with Labetalol initiation and weekly monitoring."
    }
    review_res = client.post("/api/v1/medical-brain/review-approval", json=approval_payload)
    assert review_res.status_code == 200
    approved_data = review_res.json()
    assert approved_data["hitl_approval"]["status"] == "DOCTOR_APPROVED"
    assert approved_data["hitl_approval"]["approved_by"] == "Dr. Priya Patel (Senior Obstetrician)"


def test_syndrome_recognition_preeclampsia_and_hellp():
    """
    Validates clinical recognition of Preeclampsia crisis and HELLP syndrome.
    """
    # 1. Preeclampsia crisis
    ctx_pe = PatientClinicalContext(
        patient_name="Anjali",
        age=26,
        gestational_age_weeks=35.0,
        recent_symptoms=["Blurred vision", "Severe headache"],
        test_results=[
            TestResultInput(test_id=44, value="165/110 mmHg"),
            TestResultInput(test_id=45, value="Protein 3+")
        ]
    )
    res_pe = medical_brain.analyze_patient(ctx_pe)
    assert res_pe.risk_level == "CRITICAL"
    assert any("Preeclampsia" in s for s in res_pe.detected_syndromes)
    assert res_pe.recommended_referral_facility == "TERTIARY_CARE_CENTRE"

    # 2. HELLP Syndrome
    ctx_hellp = PatientClinicalContext(
        patient_name="Sunita",
        age=30,
        gestational_age_weeks=33.0,
        recent_symptoms=["Epigastric pain"],
        test_results=[
            TestResultInput(test_id=44, value="150/98 mmHg"),
            TestResultInput(test_id=47, value="AST 180 U/L, ALT 210 U/L"),
            TestResultInput(test_id=4, value="Platelets 55000 /uL")
        ]
    )
    res_hellp = medical_brain.analyze_patient(ctx_hellp)
    assert res_hellp.risk_level == "CRITICAL"
    assert any("HELLP" in s for s in res_hellp.detected_syndromes)


def test_syndrome_recognition_gdm_and_rh_isoimmunization():
    """
    Validates Gestational Diabetes (DIPSI) and Rh Isoimmunization detection.
    """
    # 1. GDM DIPSI
    ctx_gdm = PatientClinicalContext(
        patient_name="Pooja",
        age=31,
        gestational_age_weeks=25.0,
        test_results=[
            TestResultInput(test_id=35, value="75g OGTT 2h: 165 mg/dL")
        ]
    )
    res_gdm = medical_brain.analyze_patient(ctx_gdm)
    assert any("Gestational Diabetes" in s for s in res_gdm.detected_syndromes)
    assert res_gdm.risk_level == "MODERATE"

    # 2. Rh Isoimmunization
    ctx_rh = PatientClinicalContext(
        patient_name="Deepika",
        age=27,
        gestational_age_weeks=31.0,
        test_results=[
            TestResultInput(test_id=5, value="A Rh Negative"),
            TestResultInput(test_id=6, value="ICT Positive Titer 1:32"),
            TestResultInput(test_id=41, value="MCA-PSV 1.6 MoM")
        ]
    )
    res_rh = medical_brain.analyze_patient(ctx_rh)
    assert any("Rh Isoimmunization" in s for s in res_rh.detected_syndromes)
    assert res_rh.risk_level == "CRITICAL"
    assert res_rh.referral_recommended is True


def test_neonatal_screenings_and_hitl_rejection():
    """
    Validates Neonatal CCHD, Guthrie TSH, and Doctor Rejection in HITL workflow.
    """
    # 1. Neonatal CCHD Failure
    ctx_cchd = PatientClinicalContext(
        patient_name="Baby Boy",
        age=0,
        life_stage=LifeStage.IMMEDIATE_NEWBORN,
        test_results=[
            TestResultInput(test_id=80, value="CCHD Fail: Pre 94%, Post 87%")
        ]
    )
    res_cchd = medical_brain.analyze_patient(ctx_cchd)
    assert any("CCHD" in s for s in res_cchd.detected_syndromes)
    assert res_cchd.risk_level == "CRITICAL"
    assert res_cchd.recommended_referral_facility == "TERTIARY_CARE_CENTRE"

    # 2. Doctor Rejection Workflow
    ctx_med = PatientClinicalContext(
        patient_name="Kavita",
        age=28,
        past_history=PastObstetricHistoryProfile(prior_preeclampsia=True),
        test_results=[TestResultInput(test_id=44, value="150/95 mmHg")]
    )
    res_med = medical_brain.analyze_patient(ctx_med)
    assert res_med.hitl_approval.status == "PENDING_APPROVAL"
    PENDING_APPROVALS_DB[res_med.analysis_id] = res_med

    # Doctor rejects and mandates immediate ER visit
    rej_payload = DoctorApprovalPayload(
        analysis_id=res_med.analysis_id,
        decision="REJECTED",
        doctor_name="Dr. Arvind Joshi",
        doctor_notes="Patient requires immediate in-person triage, do not give remote medication."
    )
    rej_res = submit_doctor_approval(rej_payload)
    assert rej_res.hitl_approval.status == "DOCTOR_REJECTED"
    assert "rejected" in rej_res.medical_advice_english.lower()

