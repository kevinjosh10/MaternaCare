import os
import sys
import json
import time

# Add the teammate's ML model folder to path so we can import their STT/TTS code!
sys.path.append(os.path.abspath("../MaternaCare/ml model"))

try:
    # Try importing teammate's modules
    from models_1_and_2 import LANGUAGES, record_audio_smart, robust_translate, play_audio_hidden, tempfile
    import speech_recognition as sr
    from gtts import gTTS
    MIC_ENABLED = True
except ImportError as e:
    print(f"Warning: Could not load teammate's microphone modules: {e}")
    MIC_ENABLED = False

# Import our Backend Core Models
from app.ai_models.orchestrator import voice_orchestrator
from app.medical_brain.brain_engine import medical_brain, PatientClinicalContext, TestResultInput
from app.medical_brain.microservice import submit_doctor_approval, DoctorApprovalPayload

def run_ocr_to_brain_flow():
    print("\n" + "="*70)
    print(" [MODEL 5] (OCR) TO [MODEL 4] (CORE BRAIN) PIPELINE")
    print("="*70)
    print("Simulating API call to Google Colab OCR Server (trycloudflare.com)...")
    time.sleep(2)
    
    # Simulating what colab_ocr_server.py returns
    mock_ocr_response = {
        "success": True,
        "filename": "Lab_Report_Week_34.pdf",
        "text": "Blood Pressure: 155/100 mmHg\nUrine Protein: 3+ Proteinuria\nHemoglobin: 9.2 g/dL"
    }
    
    print("\n[Model 5] Colab GPU OCR extracted the following raw text:")
    print(f"   {mock_ocr_response['text']}")
    
    print("\n[Model 4] Medical Brain Parsing text into official Catalog Test IDs...")
    time.sleep(1)
    
    test_inputs = [
        TestResultInput(test_id=44, value="155/100 mmHg"), # Blood Pressure
        TestResultInput(test_id=45, value="3+ Proteinuria"), # Urine Protein
        TestResultInput(test_id=4, value="9.2 g/dL") # Hb
    ]
    
    context = PatientClinicalContext(
        patient_id="PAT-DEMO-001",
        gestational_age_weeks=34,
        test_results=test_inputs,
        current_query_text="Doctor said my BP is high. Is this bad?"
    )
    
    print("\n[Model 4] Brain evaluating multi-parameter syndromes...")
    response = medical_brain.analyze_patient(context)
    
    print(f"\nRisk Level: {response.risk_level}")
    print(f"Syndromes Detected: {', '.join(response.detected_syndromes)}")
    print(f"\nAdvice Generated for Patient:")
    print(f"\"{response.patient_friendly_english}\"")
    
    print("\nAction Items for Doctor Panel:")
    for a in response.action_items_for_clinician:
        print(f"  - {a}")
        
    print("\n[Press Enter to return to main menu]")
    input()

def run_voice_consultation():
    print("\n" + "="*70)
    print(" CONTINUOUS MULTILINGUAL VOICE CONSULTATION (MODELS 1, 2, & 4)")
    print("="*70)
    
    if not MIC_ENABLED:
        print("Microphone modules not found. Using text fallback.")
        try:
            while True:
                query = input("\nEnter your medical question (or press Ctrl+C to exit): ")
                res = voice_orchestrator.process_consultation(text_query=query, language_hint='en')
                print(f"\nResponse: {res.get('patient_friendly_text')}")
        except KeyboardInterrupt:
            print("\n[Exiting voice consultation...]")
            return

    # Use Teammate's Language Selector
    print("\n--- SELECT YOUR LANGUAGE ---")
    for key, lang in LANGUAGES.items():
        if int(key) <= 25:
            col2_key = str(int(key) + 25)
            col2_lang = LANGUAGES.get(col2_key, {'name': ''})
            print(f"[{key:>2}] {lang['name']:<25} | [{col2_key:>2}] {col2_lang['name']}")
            
    print("\nEnter the number of the language you will speak (e.g., 3 for Tamil): ")
    choice = input("Choice [1]: ").strip() or "1"
    selected_lang = LANGUAGES.get(choice, LANGUAGES['1'])
    lang_code = selected_lang['code']
    
    temp_dir = tempfile.gettempdir()
    audio_file = os.path.join(temp_dir, "hackathon_demo.wav")
    
    print("\n[Starting Continuous Voice Mode - Press Ctrl+C at any time to exit]")
    
    try:
        while True:
            print(f"\n[Model 1] Preparing microphone for {selected_lang['name']}...")
            success = record_audio_smart(audio_file, max_duration=15)
            
            if not success:
                print("Could not record audio. Retrying...")
                continue
                
            print("\n[Model 2] Running Speech-to-Text (STT)...")
            try:
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    audio_data = recognizer.record(source)
                raw_text = recognizer.recognize_google(audio_data, language=lang_code)
            except Exception as e:
                print(f"STT Error: Could not understand audio.")
                continue
                
            print(f"Transcribed: {raw_text}")
            
            print("\n[Model 1] Translating native language to English for the Medical Brain...")
            english_query = robust_translate(raw_text, lang_code, 'en')
            print(f"English Query: {english_query}")
            
            print("\n[Model 4] Medical Brain evaluating query locally...")
            # NOTE: We pass the english_query into the core brain!
            res = voice_orchestrator.process_consultation(text_query=english_query, language_hint='en')
            
            status = res.get('status')
            if status == 'EMERGENCY_DISPATCHED':
                print("\n[Model 3] EMERGENCY GUARDIAN OVERRIDE!")
                print(f"Triggers: {res['dispatch_payload']['detected_triggers']}")
                print(f"--> PINGING AMBULANCE DRIVER PANEL WITH LIVE LOCATION <--")
                
                # Speak to the user so they aren't met with silence
                alert_msg = robust_translate("Emergency detected! An ambulance has been dispatched to your location.", 'en', lang_code)
                try:
                    tts = gTTS(text=alert_msg, lang=lang_code, slow=False)
                    tts.save(mp3_file)
                    play_audio_hidden(mp3_file)
                except:
                    pass
                continue
                
            elif status == 'PENDING_DOCTOR_APPROVAL':
                print("\n[HITL GATE] Proposed advice contains Medicine/Prescriptions.")
                print(f"--> FORWARDING TO DOCTOR DASHBOARD PANEL FOR APPROVAL <--")
                print(f"Triggers: {res.get('triggers', ['medicine keywords'])}")
                
                # Speak to the user so they aren't met with silence
                hitl_msg = robust_translate("Your request involves medication. It has been sent to your doctor for review. They will reply shortly.", 'en', lang_code)
                try:
                    tts = gTTS(text=hitl_msg, lang=lang_code, slow=False)
                    tts.save(mp3_file)
                    play_audio_hidden(mp3_file)
                except:
                    pass
                continue
                
            final_english = res.get('patient_friendly_text')
            print(f"\n[Model 1] Translating AI advice back to {selected_lang['name']}...")
            native_response = robust_translate(final_english, 'en', lang_code)
            
            print(f"\n[Model 2] Generating Text-to-Speech (TTS)...")
            print(f"Output: {native_response}")
            mp3_file = os.path.join(temp_dir, "hackathon_response.mp3")
            try:
                tts = gTTS(text=native_response, lang=lang_code, slow=False)
                tts.save(mp3_file)
                play_audio_hidden(mp3_file)
            except Exception as e:
                print(f"TTS Engine Error: {e}")
                
            print("\n--- Cycle Complete. Ready for next query. ---")
            
    except KeyboardInterrupt:
        print("\n\n[Ctrl+C Detected: Exiting Continuous Voice Consultation...]")
        return

def main():
    while True:
        print("\n\n" + "="*70)
        print(" MATERNACARE HACKATHON MASTER PIPELINE ")
        print(" Integrates: Teammate ML Models + Backend + Colab OCR + Doctor/Driver Panels")
        print("="*70)
        print(" 1. Run Live Multilingual Voice Demo (Mic -> STT -> Brain -> TTS)")
        print(" 2. Run PDF OCR Integration Demo (Colab GPU OCR -> Core Brain)")
        print(" 3. Simulate Doctor Panel (Approve Pending Medicine)")
        print(" 4. Exit")
        print("="*70)
        
        choice = input("Enter choice [1-4]: ").strip()
        
        if choice == '1':
            run_voice_consultation()
        elif choice == '2':
            run_ocr_to_brain_flow()
        elif choice == '3':
            print("\n[Doctor Panel] Viewing pending authorizations...")
            print("Action: Approved Paracetamol prescription for PAT-DEMO-001")
            time.sleep(1)
            print("Webhook fired: TTS Engine synthesizing audio and sending back to patient app.")
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
