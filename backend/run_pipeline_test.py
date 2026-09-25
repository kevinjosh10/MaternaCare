import time
import json
import logging
from app.ai_models.orchestrator import voice_orchestrator
from app.medical_brain.microservice import submit_doctor_approval, DoctorApprovalPayload, PENDING_APPROVALS_DB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PipelineTester")

def test_full_pipeline():
    print("=" * 80)
    print(" MATERNACARE END-TO-END PIPELINE TEST (WITH MOCK ASR/TTS)")
    print("=" * 80)

    # Test 1: Emergency Guardian Intercept
    print("\n--- TEST 1: EMERGENCY KEYWORD SHOUT ---")
    res1 = voice_orchestrator.process_consultation(
        text_query="Help, I am bleeding heavily!",
        language_hint="en"
    )
    print(f"Status: {res1['status']}")
    print(f"Message: {res1.get('message')}")
    if "dispatch_payload" in res1:
        print(f"Dispatch Data: {json.dumps(res1['dispatch_payload'], indent=2)}")

    # Test 2: Standard Safe Consultation (No HITL)
    print("\n--- TEST 2: SAFE CONSULTATION ---")
    res2 = voice_orchestrator.process_consultation(
        text_query="I am 16 weeks pregnant, everything is fine, just feeling a bit tired.",
        language_hint="en",
        patient_context={"gestational_weeks": 16.0}
    )
    print(f"Status: {res2['status']}")
    if res2['status'] == 'PENDING_DOCTOR_APPROVAL':
        print(f"Triggers: {res2.get('triggers')}")
    else:
        print(f"AI Advice: {res2.get('medical_advice_text')}")
    print(f"Audio Generated? {'Yes' if res2.get('audio_response_base64') else 'No'}")

    # Test 3: HITL Intercept (Medicines recommended)
    print("\n--- TEST 3: HITL GATE (PRESCRIBING MEDICINE) ---")
    res3 = voice_orchestrator.process_consultation(
        text_query="I have severe anemia and my hemoglobin is 7. Can I take iron tablets?",
        language_hint="en",
        patient_context={"gestational_weeks": 28.0}
    )
    print(f"Status: {res3['status']}")
    print(f"Triggers: {res3.get('triggers')}")
    
    if res3['status'] == "PENDING_DOCTOR_APPROVAL":
        analysis_id = res3['analysis_id']
        print(f"\n[DASHBOARD SIMULATION] Doctor reviews Analysis ID: {analysis_id}")
        
        # Doctor approves with an edit
        approval_payload = DoctorApprovalPayload(
            analysis_id=analysis_id,
            decision="EDITED",
            doctor_name="Dr. Aditi Sharma",
            edited_advice="Yes, take 2 iron tablets daily after meals and recheck Hb in 2 weeks."
        )
        approved_record = submit_doctor_approval(approval_payload)
        
        print(f"Doctor Status: {approved_record.hitl_approval.status}")
        print(f"Final Patient Advice (Sent to TTS): {approved_record.patient_friendly_english}")

    print("\n" + "=" * 80)
    print(" PIPELINE TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_full_pipeline()
