import sys
import logging
from app.ai_models.orchestrator import voice_orchestrator
from app.medical_brain.microservice import submit_doctor_approval, DoctorApprovalPayload

# Suppress loud logs for cleaner CLI experience
logging.getLogger("app.ai_models.emergency_guardian").setLevel(logging.ERROR)
logging.getLogger("model4_microservice").setLevel(logging.ERROR)
logging.getLogger("maternacare_trainer").setLevel(logging.ERROR)

def interactive_cli():
    print("=" * 80)
    print(" MATERNACARE END-TO-END PIPELINE - INTERACTIVE CLI")
    print(" Type 'quit' or 'exit' to stop.")
    print("=" * 80)

    while True:
        try:
            user_input = input("\nPatient Query: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue
                
            # Process through orchestrator
            response = voice_orchestrator.process_consultation(
                text_query=user_input,
                language_hint="en"
            )
            
            status = response.get("status")
            
            if status == "EMERGENCY_DISPATCHED":
                print("\n[MODEL 3 - EMERGENCY GUARDIAN INTERCEPTED]")
                print("   Action: Ambulance Dispatched Automatically!")
                print(f"   Triggers Detected: {response['dispatch_payload']['detected_triggers']}")
                
            elif status == "PENDING_DOCTOR_APPROVAL":
                print("\n[MODEL 4 - HITL GATE ACTIVATED]")
                print("   Status: PENDING_DOCTOR_APPROVAL")
                print(f"   Reason: {response['triggers'][0]}")
                print(f"   Analysis ID: {response['analysis_id']}")
                
                # Simulate the doctor dashboard intervention interactively
                doc_action = input("\n[Doctor Panel] Do you want to Approve (a), Edit (e), or Reject (r)? [a/e/r]: ").strip().lower()
                
                if doc_action == 'e':
                    edited_text = input("   Enter your edited advice: ")
                    payload = DoctorApprovalPayload(
                        analysis_id=response['analysis_id'],
                        decision="EDITED",
                        doctor_name="Dr. Tester",
                        edited_advice=edited_text
                    )
                elif doc_action == 'r':
                    payload = DoctorApprovalPayload(
                        analysis_id=response['analysis_id'],
                        decision="REJECTED",
                        doctor_name="Dr. Tester"
                    )
                else: # Default to approve
                    payload = DoctorApprovalPayload(
                        analysis_id=response['analysis_id'],
                        decision="APPROVED",
                        doctor_name="Dr. Tester"
                    )
                
                approved_record = submit_doctor_approval(payload)
                print(f"\n[MODEL 2 - TTS SYNTHESIS TRIGGERED]")
                print(f"   Spoken Output: \"{approved_record.patient_friendly_english}\"")
                
            else:
                # Normal Completion
                print("\n[MODEL 4 - GENERAL CONSULTATION]")
                print(f"   Status: {status}")
                print(f"   AI Advice: {response.get('medical_advice_text')}")
                print("\n[MODEL 2 - TTS SYNTHESIS TRIGGERED]")
                print(f"   Spoken Output: \"{response.get('patient_friendly_text')}\"")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    interactive_cli()
