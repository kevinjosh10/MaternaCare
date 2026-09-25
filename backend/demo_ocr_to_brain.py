import json
from app.medical_brain.brain_engine import medical_brain, PatientClinicalContext, TestResultInput

def simulate_pdf_upload_and_brain_evaluation():
    print("=====================================================================")
    print(" PIPELINE DEMO: OCR PDF UPLOAD -> CORE BRAIN MEMORY")
    print("=====================================================================")
    
    # STEP 1: OCR Extraction (Simulated)
    print("\n[1] User uploads '3rd_Trimester_Lab_Report.pdf'")
    print("[2] Model 1 (OCR Vision Engine) processes the document...")
    
    # This represents the JSON output from the OCR model
    ocr_extracted_data = {
        "patient_id": "PAT-9999",
        "gestational_age": 34,
        "extracted_tests": [
            {"test_id": 44, "name": "Blood Pressure", "value": "150/95 mmHg"},
            {"test_id": 45, "name": "Urine Protein", "value": "3+ Proteinuria"},
            {"test_id": 4, "name": "Hemoglobin (CBC)", "value": "10.2 g/dL"}
        ]
    }
    
    print(f"    -> Extracted Data: {json.dumps(ocr_extracted_data, indent=2)}")
    
    # STEP 2: Database / Memory Storage
    print("\n[3] Saving extracted clinical data to Patient Medical Record (Memory)...")
    test_inputs = []
    for test in ocr_extracted_data["extracted_tests"]:
        test_inputs.append(TestResultInput(test_id=test["test_id"], value=test["value"]))
        
    context = PatientClinicalContext(
        patient_id=ocr_extracted_data["patient_id"],
        gestational_age_weeks=ocr_extracted_data["gestational_age"],
        test_results=test_inputs,
        current_query_text="Hi, I just uploaded my lab reports. Is my baby okay?"
    )
    
    # STEP 3: Core Brain (Model 4) Evaluation
    print("\n[4] Core Brain (Model 4) actively reading patient memory and current query...")
    response = medical_brain.analyze_patient(context)
    
    print("\n[5] BRAIN CLINICAL SYNTHESIS:")
    print(f"    Risk Level: {response.risk_level}")
    print(f"    High Risk Detected: {response.is_high_risk}")
    
    if response.detected_syndromes:
        print(f"    Detected Syndromes: {', '.join(response.detected_syndromes)}")
        
    print("\n[6] FINAL VOICE OUTPUT TO PATIENT:")
    print(f"    \"{response.patient_friendly_english}\"")
    
    print("\n[7] INTERNAL DOCTOR ACTION ITEMS:")
    for action in response.action_items_for_clinician:
        print(f"    - {action}")
        
    print("=====================================================================")

if __name__ == "__main__":
    simulate_pdf_upload_and_brain_evaluation()
