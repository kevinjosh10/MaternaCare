# MaternaCare: Distributed Multi-Model Architecture
**(With Human-In-The-Loop Doctor Approval)**

This document outlines the complete workflow connecting all 5 models in the system. This microservices architecture allows models to be hosted across different laptops or Google Colab instances, communicating seamlessly via APIs.

---

## 🏗️ System Architecture Diagram

```mermaid
graph TD
    %% Setup Phase
    PDF[("Medical Report (PDF)")] --> |Upload| M5["Model 5: OCR Model (Jina OCR v1)"]
    M5 --> |Extracts Patient Data| DB[("Patient Database / Memory (AWS RDS PostgreSQL)")]
    DB --- M4

    %% Emergency Bypass Pipeline
    Voice[(Patient Voice)] -.-> |Continuous Listening| M3["Model 3: Shout Recognizer"]
    M3 -.-> |Keywords: 'Help', 'Bachao'| Vercel["Hospital Dashboard (Vercel) & Alert System"]

    %% Conversational Pipeline
    Voice --> |Speaks| M2_STT["Model 2: Voice-to-Text (STT)"]
    M2_STT --> |Raw Native Text| M1_In["Model 1: Language Recognition"]
    M1_In --> |Detects language & Translates to English| M4["Model 4: Main Medical Brain (LLM)"]
    
    %% Core Processing & Doctor Approval
    M4 --> |Checks for Medical/Dietary Advice| Routing{Is it a Medical/Food Recommendation?}
    
    Routing -->|No (General Chat)| M1_Out["Model 1: Language Translation"]
    
    Routing -->|Yes (Medicine/Food)| ApprovalReq["Sends Pending Request to Vercel Dashboard"]
    ApprovalReq --> |Doctor Reviews| DoctorHitl(("👨‍⚕️ Doctor / Nurse Approval"))
    DoctorHitl --> |Approves or Edits| M1_Out
    
    %% Output Pipeline
    M1_Out --> |Translates back to Native Language| M2_TTS["Model 2: Text-to-Voice (TTS)"]
    M2_TTS --> |Speaks Approved Response| AudioOut[("Audio Speaker")]
```

---

## 🔄 Step-by-Step Data Flow

### Phase 1: Patient Onboarding (Model 5: OCR Model)
*This happens before the patient interacts with the system or whenever new lab reports/prescriptions are uploaded.*
1. The doctor or mother uploads the pregnant woman's past medical reports / ultrasound / lab slips (PDF / Scans).
2. **Model 5 (OCR Model - Jina OCR v1):** Scans the PDF/image, extracts vital medical data (blood pressure history, glucose levels, gestational metrics, allergies, prior complications).
3. **Data Transfer:** Structured text and extracted entities are saved into **Amazon RDS (PostgreSQL)** and linked to the patient ID so Model 4 has full access to the patient's continuous health memory.

---

### Phase 2: Ambient Emergency Guardian (Model 3: Shout Recognizer)
*This runs independently in the background to ensure immediate maternal and fetal safety.*
1. **Model 3 (Shout Recognizer):** Runs on a local edge device/laptop near the patient, continuously monitoring ambient audio.
2. If the woman shouts a distress keyword (e.g., *"help"*, *"bachao"*, *"dard ho raha hai"*), it immediately bypasses all standard conversational steps.
3. **Data Transfer:** Directly issues an urgent HTTP `POST` webhook to the Hospital & Ambulance Dispatch Hub on Vercel with real-time audio alert & GPS coordinates.

---

### Phase 3: Conversational Pipeline & Doctor Approval (Human-In-The-Loop)
*The core interaction loop when the mother asks questions or seeks guidance.*

1. **Hearing the Patient (Model 2: Voice-to-Text / STT):**
   - The woman speaks in her native language (e.g., Hindi, Tamil, Telugu, Marathi).
   - **Model 2 (STT)** converts raw speech audio into native text.
   - *Data Transfer:* Sends JSON payload `{"text": "mujhe dard ho raha hai", "patient_id": "P-1004"}` to Model 1.

2. **Language Processing (Model 1: Language Recognition & Translation):**
   - **Model 1** identifies the source language (e.g., Hindi `hi`) and translates the query into standardized medical English.
   - *Data Transfer:* Sends `{"translated_text": "I am experiencing pain", "source_lang": "hi", "patient_id": "P-1004"}` to Model 4.

3. **Medical Reasoning (Model 4: Main Medical Brain / LLM):**
   - Model 4 receives the English query and looks up the patient's verified history (from Model 5's S3/RDS memory) to incorporate context (e.g., 32 weeks gestational age, elevated BP, history of preeclampsia).
   - Generates an accurate, context-aware clinical response.

4. **⚠️ SAFETY CHECK — Human-In-The-Loop (HITL) Doctor Approval:**
   - Model 4 automatically screens its proposed response. If it contains **medical advice, prescriptions, dietary changes, remedies, or medication dosages** (*medicine, tablets, syrup, tea, diet, food, remedies*), it **pauses the pipeline**.
   - *Data Transfer:* Issues a pending request to the Clinician/Hospital Vercel Dashboard:
     ```json
     {
       "status": "PENDING_APPROVAL",
       "patient_id": "P-1004",
       "proposed_advice": "Ginger infusion for mild nausea; maintain SBP monitoring under 140 mmHg.",
       "urgency": "MEDIUM"
     }
     ```
   - A real-time notification alerts the on-duty clinician/nurse on the dashboard.
   - The clinician clicks **Approve**, **Reject**, or **Edit**.
   - The dashboard returns the approved, validated medical response to the pipeline.

5. **Translation Back (Model 1):**
   - **Model 1** translates the doctor-approved English response back into the mother's native language.
   - *Data Transfer:* Sends `{"text": "Adrak ki chai pee sakti hain...", "target_lang": "hi"}` to Model 2.

6. **Speaking (Model 2: Text-to-Voice / TTS):**
   - **Model 2 (TTS)** synthesizes native speech audio and plays it loudly and clearly to the patient through local speakers.

---

## 📡 API Contract Specification for Microservices

| Model | Role | Input Payload | Output Payload | Endpoint |
|---|---|---|---|---|
| **Model 5** | OCR Extraction | Multipart Form (`file`, `patientId`) | `{"s3Uri", "ocrMarkdown", "extractedEntities"}` | `POST /api/documents/upload` |
| **Model 3** | Shout / Distress Detector | Audio Stream (`PCM/WAV`) | `{"distressDetected": true, "keyword": "help"}` | `POST /api/emergency/shout-trigger` |
| **Model 2** | STT / TTS | Audio Blob / Text String | Transcribed Text / Synthesized Audio URL | `POST /api/audio/stt`, `POST /api/audio/tts` |
| **Model 1** | Language Translation | `{"text", "source_lang", "target_lang"}` | `{"translated_text", "detected_lang"}` | `POST /api/language/translate` |
| **Model 4** | Medical Brain & HITL Check | `{"query", "patientContext"}` | `{"response", "requiresApproval": true/false}` | `POST /api/medical/query` |
| **Vercel** | Doctor HITL Review Hub | `{"approvalId", "decision", "editedText"}` | `{"status": "APPROVED", "finalText"}` | `POST /api/doctor/approval` |
