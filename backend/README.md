# MaternaCare — AI-Powered Maternal & Neonatal Continuity, Risk & Emergency Referral Intelligence

MaternaCare is an enterprise-grade backend and AI intelligence foundation for an end-to-end longitudinal maternal and neonatal healthcare system with an integrated **Multilingual Voice-to-Voice Pregnancy Intelligence Pipeline**.

---

## ⚕️ Important Clinical Governance & Safety Notice

1. **Decision Support, Not Autonomous Diagnosis**:
   - The AI **does NOT** diagnose patients.
   - The system standardizes phrasing: `Potentially concerning pattern detected — clinical review recommended.`
2. **Human-in-the-Loop Workflow**:
   - Extracted document information and AI risk flags **must be verified by an authorized clinician or health worker** before becoming trusted clinical history.
3. **Protocol-Aligned & Configurable**:
   - Clinical rules are aligned with World Health Organization (WHO) and National Antenatal & Postnatal Care guidelines (preeclampsia, gestational diabetes, hemorrhage, and neonatal danger signs).
4. **Data Integrity**:
   - Demo and test data are explicitly labeled as synthetic.
   - All patient data access is protected by Role-Based Access Control (RBAC) and immutable Audit Logs.

---

## 🎙️ Multi-Model Voice-to-Voice Architecture

MaternaCare integrates three specialized AI models that communicate seamlessly with each other:

```
[Maternal Voice In (Any Language)]
               │
               ▼
┌────────────────────────────────────────┐
│ 1. Multilingual Speech Recognition ASR │
│ (Transcribes Hindi, Tamil, Telugu,     │
│  Kannada, Bengali, English, etc.)      │
└──────────────────┬─────────────────────┘
                   │ Transcribed Query & Detected Language
                   ▼
┌────────────────────────────────────────┐
│ Context Integrator: Longitudinal Memory│
│ (Gestational Age, Past BP, Symptoms)   │
└──────────────────┬─────────────────────┘
                   │ Rich Clinical Context
                   ▼
┌────────────────────────────────────────┐
│ 2. Medical Pregnancy Knowledge Model   │
│ - Trimester & Postpartum Protocols     │
│ - Red flag detection (Preeclampsia,    │
│   bleeding, reduced fetal movement)    │
│ - Strict clinical guardrails           │
│ - Dual Output: Doctor & Patient Views  │
└──────────────────┬─────────────────────┘
                   │ Plain-Language Empathetic Response
                   ▼
┌────────────────────────────────────────┐
│ 3. Multilingual Speech Synthesis (TTS) │
│ - Converts clinical advice into gentle │
│   maternal voice in mother's language  │
│ - Pronounces medical vitals naturally  │
└──────────────────┬─────────────────────┘
                   │ High-fidelity WAV Audio
                   ▼
[Maternal Voice Out + Clinical Record Stream]
```

### 1. Multilingual Automatic Speech Recognition (ASR)
- Located at: `app/ai_models/asr_model.py`
- Recognizes voice queries in any language (English, Hindi, Tamil, Telugu, Kannada, Bengali, Marathi, Spanish, French, Swahili, etc.).
- Audio preprocessing, base64 decoding, language identification, and speech-to-text conversion.

### 2. Clinical Pregnancy Knowledge Intelligence Engine
- Located at: `app/ai_models/medical_pregnancy_model.py`
- Contains clinical knowledge across Trimesters 1–3, Intrapartum Delivery, Postpartum Mother (Day 1 to 1 Year), and Newborn Care (0 to 1 Year).
- Generates:
  1. Professional clinical summary with triage level for doctors.
  2. Empathetic, culturally sensitive, plain-language advice for the mother in her native language.

### 3. Multilingual Speech Synthesis (TTS)
- Located at: `app/ai_models/tts_model.py`
- Synthesizes natural spoken voice responses in the user's language.
- Phonetically normalizes vital signs (e.g., converts "BP 140/90" into "blood pressure 140 over 90").

### 4. Multi-Model Communication Orchestrator
- Located at: `app/ai_models/orchestrator.py`
- Coordinates data transfer and execution between ASR, Longitudinal Health Memory, Clinical Knowledge Engine, and TTS.
- Endpoint: `POST /api/v1/voice/consult`

---

## 📊 Longitudinal Test Datasets (CSV)

As requested, complete synthetic test datasets covering **Month 1 to Month 10 of pregnancy**, **1 full year of maternal postpartum follow-up**, and **1 full year of newborn care** are provided in both `app/data/` and the workspace root:

1. **`maternacare_pregnancy_months_1_to_10_longitudinal_data.csv`**:
   - Tracks 10 months of pregnancy (Weeks 4, 8, 12, 16, 20, 24, 28, 32, 36, 40).
   - Columns: `patient_id`, `pregnancy_id`, `gestational_age_weeks`, `visit_date`, `systolic_bp_mmHg`, `diastolic_bp_mmHg`, `pulse_bpm`, `fundal_height_cm`, `fetal_heart_rate_bpm`, `urine_protein`, `hemoglobin_g_dL`, `blood_glucose_mg_dL`, `lab_test_name`, `ultrasound_type`, `ultrasound_findings`, `reported_symptoms`, `prescribed_medications`, `risk_level`, `ai_pattern_detected`, `clinical_notes`.

2. **`maternacare_mother_1_year_postpartum_data.csv`**:
   - Tracks the mother over 1 full year postpartum (Day 1, Day 3, Day 7, Day 14, 6 Weeks, 3 Months, 6 Months, 9 Months, 12 Months).
   - Columns: `patient_id`, `delivery_id`, `postpartum_timeline`, `postpartum_day_number`, `systolic_bp_mmHg`, `diastolic_bp_mmHg`, `maternal_weight_kg`, `vaginal_bleeding_lochia`, `uterine_involution_status`, `wound_status`, `headache_or_vision_changes`, `urinary_and_bowel_function`, `breastfeeding_and_lactation`, `hemoglobin_g_dL`, `epds_depression_score`, `contraceptive_method`, `clinical_notes_and_guidance`.

3. **`maternacare_newborn_1_year_growth_followup_data.csv`**:
   - Tracks the newborn from birth to 1 year (Birth, Day 3, Day 7, Day 14, 6w, 10w, 14w, 6m, 9m, 12m).
   - Columns: `newborn_id`, `age_days`, `weight_grams`, `length_cm`, `head_circumference_cm`, `heart_rate_bpm`, `respiratory_rate_bpm`, `feeding_status`, `jaundice_observation`, `vaccines_administered`, `developmental_milestones`, `clinician_notes`.

---

## 🏗️ Longitudinal Health Modules

The backend implements 28 normalized, relational clinical modules:
1. **Patient Demographics & History**: Normalized Obstetric & Medical history.
2. **Pregnancy Module**: Gravida, para, gestational age, high-risk flags.
3. **Antenatal Care (ANC) Visits**: Standard ANC visits with automatic time-series sync.
4. **Time-Series Observations**: Scalable metric observations (BP, weight, SpO2, FHR, Hb, glucose).
5. **Structured Symptoms**: Severity, duration, onset, and verified flag.
6. **Laboratory Results**: Extensible test types, reference ranges, abnormality flags, verification.
7. **Ultrasound & Imaging**: Structured parameters (AFI, placenta, fetal count) + document links.
8. **Medications, Supplements & Vaccinations**: Prenatal & postnatal drug tracking.
9. **Document Intelligence**: UPLOAD → EXTRACT → STRUCTURE → HUMAN VERIFY → TRUSTED HISTORY.
10. **Delivery & Intrapartum**: Delivery mode, blood loss, complications, gestational age.
11. **Newborn & Growth Follow-Up**: APGAR, screening, weight/height longitudinal trajectories.
12. **Postpartum Mother Care**: In-depth lochia, uterine involution, BP, and mental health.
13. **Risk Intelligence & Explainability**: Configurable risk rules, SHAP-ready contributions, clinician review.
14. **Emergency Referrals**: Multi-state referral state machine with timestamps.
15. **Facilities & GPS Directory**: Service capabilities, emergency phone, GPS coordinates.
16. **Emergency Communications**: SMS, Voice, TTS alerts with delivery status.
17. **Authentication & RBAC**: JWT, bcrypt, roles (`ADMIN`, `DOCTOR`, `NURSE`, `MIDWIFE`, `HEALTH_WORKER`, etc.).
18. **Audit Logging**: Full traceability of all patient views, record edits, AI outputs, and reviews.
19. **Longitudinal Patient Timeline (`GET /api/v1/patients/{patient_id}/timeline`)**: Unified health memory.
20. **Patient Summary (`GET /api/v1/patients/{patient_id}/summary`)**: Unified single-page clinical view.

---

## 🚀 Getting Started

### Option 1: Run with Docker Compose (Recommended for Production)
```bash
cd backend
docker-compose up --build
```
- API & Swagger Docs: `http://localhost:8000/docs`
- PostgreSQL Port: `5432`

### Option 2: Run Locally with Python Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Seed the 1-to-10 month pregnancy and 1-year maternal/newborn test dataset:
python -m app.data.seed_data

# Start the FastAPI server:
uvicorn app.main:app --reload --port 8000
```

### Run Tests:
```bash
cd backend
pytest
```

---

## 📖 Key API Endpoints & Examples

### 1. Voice-to-Voice Multilingual Consultation
- **Endpoint**: `POST /api/v1/voice/consult`
- **Request Body**:
```json
{
  "text_query": "मुझे तेज सिरदर्द है और आंखों के आगे धुंधला दिख रहा है",
  "input_language": "hi",
  "output_audio": true
}
```
- **Response**:
```json
{
  "transcribed_query": "मुझे तेज सिरदर्द है और आंखों के आगे धुंधला दिख रहा है",
  "detected_language": "hi",
  "clinical_review_recommended": true,
  "potential_risk_flags": ["PREECLAMPSIA"],
  "medical_advice_text": "Potentially concerning pattern detected — clinical review recommended. Protocol flagged: PREECLAMPSIA_SIGNS...",
  "patient_friendly_text": "नमस्ते। आपने सिरदर्द या आंखों के आगे धुंधलापन महसूस होने की बात कही है। गर्भावस्था में यह रक्तचाप (बीपी) बढ़ने का संकेत हो सकता है...",
  "audio_response_base64": "UklGRi...",
  "audio_format": "audio/wav",
  "model_pipeline_trace": {
    "asr_model": "whisper-base-multilingual",
    "medical_model": "maternacare-clinical-kg-v1.0",
    "tts_engine": "neural-maternacare-tts-v1",
    "total_pipeline_ms": 12.4
  }
}
```

### 2. Patient Longitudinal Timeline
- **Endpoint**: `GET /api/v1/patients/{patient_id}/timeline`
- Returns unified chronological events connecting pre-pregnancy, all ANC visits, labs, ultrasounds, delivery, postpartum maternal visits, and newborn follow-ups.

### 3. Patient Unified Summary
- **Endpoint**: `GET /api/v1/patients/{patient_id}/summary`
- Returns patient demographics, current pregnancy status, latest observations, recent symptoms, active referrals, and postpartum/newborn records.

---

## 🧠 Model 4: Main Medical Brain (Clinical Reasoning Core)

Model 4 acts as the clinical reasoning brain of MaternaCare, specifically tailored for Indian maternal & neonatal health (incorporating FOGSI, DIPSI, MoHFW, WHO, and ACOG standards).

### Key Features:
1. **Master Diagnostic Catalog (122 Clinical Tests)**:
   - Full reference ranges, Indian protocols, and danger thresholds for every test from First Trimester through Infancy Month 12.
2. **Past Obstetric History Analyzer**:
   - Calculates recurrence risks for prior preeclampsia (15-50%), prior GDM (50-70%), prior cesarean scar rupture risk, prior preterm birth, prior stillbirth, and Rh isoimmunization.
   - Prescribes early preventive actions (Aspirin 150mg at bedtime, early 75g OGTT at booking, vaginal progesterone, serial Dopplers).
3. **The Human-In-The-Loop (HITL) Safety Gate**:
   - If the proposed clinical response contains any reference to medicine, tablets, syrup, injection, diet, food, or home remedies, it **pauses the pipeline** and marks status as `PENDING_APPROVAL`.
   - Sends notification to the Hospital Vercel Dashboard for doctor sign-off (`APPROVED`, `EDITED`, or `REJECTED`).
   - Only doctor-approved advice is sent forward to Model 1 (Translation) and Model 2 (TTS).

### Model 4 Endpoints:
- `POST /api/v1/medical-brain/analyze`: Comprehensive clinical reasoning across 122 tests, past history, and symptoms.
- `POST /api/v1/medical-brain/analyze-history`: Evaluates previous pregnancy issues and mandates surveillance tests.
- `GET /api/v1/medical-brain/catalog`: Returns all 122 test definitions with clinical protocols.
- `GET /api/v1/medical-brain/pending-approvals`: List of advice awaiting doctor sign-off on Vercel Dashboard.
- `POST /api/v1/medical-brain/review-approval`: Doctor approves/edits pending advice.
- `POST /api/v1/medical-brain/train`: Initiates neural training pipeline.

### Command to Train Model 4:
```bash
cd backend
python -m app.medical_brain.train_brain --epochs 20
```
