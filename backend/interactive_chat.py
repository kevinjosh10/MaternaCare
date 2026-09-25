"""
MaternaCare Model 4: Live Interactive Clinical Brain Console
Allows healthcare workers, developers, and testers to interactively test Model 4 in real-time.
"""

import sys
from typing import List, Optional

from app.medical_brain.catalog import MASTER_TESTS_CATALOG, get_test_by_id, LifeStage
from app.medical_brain.past_history_analyzer import PastObstetricHistoryProfile, past_history_analyzer
from app.medical_brain.brain_engine import (
    MainMedicalBrainEngine, PatientClinicalContext, TestResultInput, medical_brain
)
from app.medical_brain.microservice import PENDING_APPROVALS_DB, submit_doctor_approval, DoctorApprovalPayload


def print_divider(char="=", length=75):
    print(char * length)


def test_preset_case(choice: str):
    presets = {
        "1": {
            "title": "Severe Preeclampsia & Neurological Symptoms",
            "name": "Meenakshi (Madurai)",
            "age": 28,
            "ga": 34.0,
            "query": "Severe throbbing headache, blurred vision, and swollen legs",
            "history": PastObstetricHistoryProfile(gravida=2, para=1, prior_preeclampsia=True),
            "tests": [
                TestResultInput(test_id=44, value="165/110 mmHg"),
                TestResultInput(test_id=45, value="Proteinuria 3+ (UPCR 2.4)")
            ]
        },
        "2": {
            "title": "Gestational Diabetes Mellitus (DIPSI Protocol)",
            "name": "Pooja (Jaipur)",
            "age": 31,
            "ga": 26.0,
            "query": "Extreme thirst, fatigue, and frequent urination",
            "history": PastObstetricHistoryProfile(gravida=2, para=1, prior_gestational_diabetes=True),
            "tests": [
                TestResultInput(test_id=15, value="Fasting Blood Sugar 104 mg/dL"),
                TestResultInput(test_id=35, value="75g OGTT 2h: 168 mg/dL")
            ]
        },
        "3": {
            "title": "Antepartum Hemorrhage / Emergency Bleeding",
            "name": "Lakshmi (Cuttack)",
            "age": 25,
            "ga": 32.0,
            "query": "Sudden bright red vaginal bleeding soaking my clothes!",
            "history": PastObstetricHistoryProfile(gravida=2, para=1, previous_c_sections=1),
            "tests": [
                TestResultInput(test_id=44, value="105/65 mmHg")
            ]
        },
        "4": {
            "title": "Neonatal Critical Heart Defect (CCHD Screen Failure)",
            "name": "Newborn Baby Boy",
            "age": 0,
            "ga": 39.5,
            "query": "Baby has blue tint around lips and rapid breathing",
            "history": None,
            "tests": [
                TestResultInput(test_id=80, value="CCHD Fail: Right Hand 93%, Foot 84% (Gradient 9%)")
            ]
        },
        "5": {
            "title": "Routine Healthy Pregnancy Follow-up",
            "name": "Ananya (Bengaluru)",
            "age": 24,
            "ga": 20.0,
            "query": "Feeling good, feeling baby kicks, here for regular checkup",
            "history": PastObstetricHistoryProfile(gravida=1, para=0),
            "tests": [
                TestResultInput(test_id=4, value="Hb 12.1 g/dL"),
                TestResultInput(test_id=44, value="114/72 mmHg")
            ]
        }
    }

    if choice not in presets:
        print("[!] Invalid preset choice.")
        return

    data = presets[choice]
    print(f"\n[LOADING PRESET] {data['title']}")
    run_clinical_case(
        patient_name=data["name"],
        age=data["age"],
        ga=data["ga"],
        query=data["query"],
        history=data["history"],
        tests=data["tests"]
    )


def run_clinical_case(
    patient_name: str,
    age: int,
    ga: float,
    query: str,
    history: Optional[PastObstetricHistoryProfile] = None,
    tests: Optional[List[TestResultInput]] = None
):
    print_divider("-")
    print(f"PATIENT CONTEXT:")
    print(f"  Name: {patient_name} | Age: {age} | Gestational Age: {ga}w")
    print(f"  Query / Complaint: \"{query}\"")
    if history:
        print(f"  Obstetric History: G{history.gravida} P{history.para} (Prior PreE: {history.prior_preeclampsia}, Prior GDM: {history.prior_gestational_diabetes})")
    if tests:
        print(f"  Tests Submitted ({len(tests)}):")
        for t in tests:
            cat = get_test_by_id(t.test_id)
            print(f"    - Test #{t.test_id} ({cat['name'] if cat else 'Custom'}): {t.value}")
    print_divider("-")

    ctx = PatientClinicalContext(
        patient_name=patient_name,
        age=age,
        gestational_age_weeks=ga,
        past_history=history,
        current_query_text=query,
        test_results=tests or []
    )

    print("\n[AI BRAIN INFERENCE IN PROGRESS...]")
    res = medical_brain.analyze_patient(ctx)

    # Color/visual markers
    risk_badge = f"*** {res.risk_level} RISK ***"
    print(f"\nRESULTS:")
    print(f"  Risk Classification : {risk_badge}")
    print(f"  Emergency Referral  : {res.referral_recommended} (Destination: {res.recommended_referral_facility or 'None'})")
    print(f"  Detected Syndromes  : {res.detected_syndromes or ['None']}")
    
    if res.abnormal_tests_detected:
        print(f"  Abnormal Tests ({len(res.abnormal_tests_detected)}):")
        for ab in res.abnormal_tests_detected:
            print(f"    * Test #{ab['test_id']} ({ab['test_name']}): {ab['observed_value']} -> {ab['clinical_interpretation']}")

    print(f"\nDOCTOR CLINICAL SUMMARY (English):")
    print(f"  \"{res.medical_advice_english}\"")

    print(f"\nPATIENT-FRIENDLY RESPONSE (Plain language for Voice/Translation):")
    print(f"  \"{res.patient_friendly_english}\"")

    print(f"\nHUMAN-IN-THE-LOOP (HITL) SAFETY GATE:")
    print(f"  Gate Status : {res.hitl_approval.status}")
    if res.hitl_approval.trigger_reasons:
        print(f"  Triggered By: {res.hitl_approval.trigger_reasons}")

    if res.hitl_approval.status == "PENDING_APPROVAL":
        print(f"\n[SAFETY PAUSE] This response contains medications, diets, or clinical recommendations.")
        print(f"The advice is held until an authorized doctor approves it on the Hospital Dashboard.")
        PENDING_APPROVALS_DB[res.analysis_id] = res

        print_divider("~")
        print("SIMULATE DOCTOR ACTION FROM HOSPITAL DASHBOARD:")
        print("  [A] Approve advice as is")
        print("  [E] Edit advice with clinical adjustments")
        print("  [R] Reject advice and demand in-person hospital consult")
        print("  [Enter] Skip simulation")
        doc_choice = input("Select action (A/E/R/Enter): ").strip().upper()

        if doc_choice == "A":
            approval = DoctorApprovalPayload(
                analysis_id=res.analysis_id,
                decision="APPROVED",
                doctor_name="Dr. Priya Patel (Senior Obstetrician)",
                doctor_notes="Labs and clinical findings reviewed. Protocol approved for release."
            )
            updated = submit_doctor_approval(approval)
            print(f"[SUCCESS] Response DOCTOR_APPROVED by {updated.hitl_approval.approved_by}!")
            print("Response released downstream to Model 1 (Translation) and Model 2 (Voice synthesis).")
        elif doc_choice == "E":
            edited_text = input("Enter customized doctor advice: ").strip() or "Modified dose per clinical judgment."
            approval = DoctorApprovalPayload(
                analysis_id=res.analysis_id,
                decision="EDITED",
                doctor_name="Dr. Priya Patel (Senior Obstetrician)",
                edited_advice=edited_text,
                doctor_notes="Custom dosage modified based on patient profile."
            )
            updated = submit_doctor_approval(approval)
            print(f"[SUCCESS] Response DOCTOR_EDITED. Updated text released to patient!")
        elif doc_choice == "R":
            approval = DoctorApprovalPayload(
                analysis_id=res.analysis_id,
                decision="REJECTED",
                doctor_name="Dr. Priya Patel (Senior Obstetrician)",
                doctor_notes="High imminent danger. Mandate immediate ER attendance."
            )
            updated = submit_doctor_approval(approval)
            print(f"[SUCCESS] Response DOCTOR_REJECTED. Patient directed to emergency room.")
    else:
        print(f"[DIRECT RELEASE] No medications or diet prescribed. Response released directly.")

    print_divider("=")


def start_interactive_console():
    print_divider("=")
    print(" MATERNACARE MODEL 4: CLINICAL BRAIN LIVE INTERACTIVE CONSOLE")
    print(" Guidelines: FOGSI, DIPSI, MoHFW, WHO, ACOG | Catalog: 122 Diagnostic Tests")
    print_divider("=")

    try:
        while True:
            print("\nChoose an option:")
            print("  [1-5] Run Pre-Built Clinical Scenarios:")
            print("        1: Preeclampsia Crisis (BP 165/110 + Protein 3+ + Headache)")
            print("        2: Gestational Diabetes Mellitus (OGTT 168 mg/dL + FBS 104)")
            print("        3: Antepartum Hemorrhage (Active Vaginal Bleeding)")
            print("        4: Neonatal Heart Defect (CCHD Pulse Ox Fail)")
            print("        5: Routine Normal Pregnancy Checkup (Hb 12.1, BP 114/72)")
            print("  [C]   Enter a Custom Patient Case (Free text symptoms + Test values)")
            print("  [Q]   Quit")

            choice = input("\nEnter choice (1-5, C, or Q): ").strip().upper()

            if choice in ["1", "2", "3", "4", "5"]:
                test_preset_case(choice)
            elif choice == "C":
                print("\n--- ENTER CUSTOM CASE ---")
                name = input("Patient Name (or press Enter for 'Rani Devi'): ").strip() or "Rani Devi"
                ga_str = input("Gestational Age in weeks (e.g. 32): ").strip()
                ga = float(ga_str) if ga_str else 32.0
                query = input("Patient Symptoms / Query (e.g. 'high blood pressure and headache'): ").strip()
                
                print("\nDo you want to add a test result from the 122 catalog? (y/n): ")
                add_test = input().strip().lower()
                tests = []
                if add_test == "y":
                    print("Popular Test IDs: 4=CBC/Hb, 15=FBS, 35=OGTT 75g, 44=BP, 45=Urine Protein, 49=Bile Acids, 80=CCHD, 90=Guthrie TSH")
                    tid_str = input("Test ID (1-122): ").strip()
                    tval = input("Observed Value (e.g. '160/105 mmHg' or '175 mg/dL' or 'Hb 6.2'): ").strip()
                    if tid_str and tval:
                        tests.append(TestResultInput(test_id=int(tid_str), value=tval))

                run_clinical_case(patient_name=name, age=26, ga=ga, query=query, tests=tests)
            elif choice == "Q":
                print("\nExiting MaternaCare Medical Brain Console. Stay safe!")
                break
            else:
                print("[!] Unrecognized input. Please choose 1-5, C, or Q.")
    except (EOFError, KeyboardInterrupt):
        print("\n\nSession finished. Exiting MaternaCare Medical Brain Console.")


if __name__ == "__main__":
    start_interactive_console()
