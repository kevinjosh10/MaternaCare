<div align="center">
  
# 🤰 MaternaCare
**AI-Powered Maternal Continuity, Risk Triage, & Emergency Intelligence Platform**

[![Next.js](https://img.shields.io/badge/Next.js-16+-black?style=flat&logo=next.js)](#)
[![Python FastAPI](https://img.shields.io/badge/Python-FastAPI-009688?style=flat&logo=fastapi)](#)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Data-336791?style=flat&logo=postgresql)](#)
[![AWS](https://img.shields.io/badge/AWS-Cloud-232F3E?style=flat&logo=amazon-aws)](#)

*Bridging the gap between home care and hospital intervention for expectant mothers through multilingual AI, medical OCR, and synchronized clinical data.*

</div>

---

## 🚨 The Core Problem
Maternal mortality and preventable complications (such as preeclampsia, gestational diabetes, and postpartum hemorrhage) often escalate because expectant mothers lack immediate access to verified clinical triage. Furthermore, when emergencies arise, their scattered medical records are unavailable to first responders and emergency doctors during the critical "golden hour."

## 💡 Our Solution
MaternaCare is an end-to-end, multi-lingual AI ecosystem that serves as a 24/7 continuous health companion for mothers, while instantly synchronizing their critical medical data with a **Human-In-The-Loop (HITL) clinician dashboard** and **emergency ambulance dispatch**.

By unifying predictive risk modeling, voice-first AI accessibility, and medical document OCR, MaternaCare ensures mothers receive instant, personalized guidance while doctors retain complete oversight and control.

---

## 🌟 Key Technical Pillars & Features

### 1. Multilingual Voice-First AI Companion (Parent Portal)
* **What it is:** A highly accessible, conversational AI interface designed specifically for expectant mothers.
* **How it works:** Mothers can speak their symptoms directly into the app using real-time Speech-to-Text (STT). The AI processes the query in their preferred regional language (English, Hindi, Tamil, Telugu, etc.) and instantly speaks back clinical guidance using automated Text-to-Speech (TTS). 
* **The Magic:** It doesn't just give generic advice; it leverages a deep-memory payload. The AI intrinsically knows the mother’s gestational weeks, past medical conditions, and allergies, dynamically tailoring its advice to her exact medical history.

### 2. Clinical Intelligence & Human-In-The-Loop (HITL) Verification
* **What it is:** The safety-critical brain of the platform, powered by a Python microservice architecture.
* **How it works:** When a mother mentions a high-risk symptom (like bleeding, severe headaches, or extreme swelling), the AI’s obstetric risk engine immediately flags the urgency as HIGH. 
* **The Magic:** Instead of hallucinating medical advice, it intercepts the response and pushes it to a secure **Doctor Approvals Queue**. A human clinician must verify and approve the triage protocol before the system advises the mother, guaranteeing zero-hallucination medical safety.

### 3. Automated OCR Document Pipeline
* **What it is:** A seamless medical record ingestion engine.
* **How it works:** Mothers can take a photo of their physical lab reports or prescriptions. The platform uploads it via AWS S3 and processes it through an advanced OCR engine (powered by Jina AI). 
* **The Magic:** It automatically extracts crucial entities—like blood pressure readings, protein levels, and gestational age—and securely syncs them directly into the PostgreSQL database, updating the mother’s health trajectory without tedious manual data entry.

### 4. Unified Care Continuum (Clinician & Ambulance Portals)
* **What it is:** Synchronized dashboards for healthcare providers and emergency responders.
* **How it works:** If a mother’s condition deteriorates, EMTs and hospital staff log into their respective portals. Because the entire system runs on a unified PostgreSQL database, emergency responders have instantaneous access to the mother's encrypted health records, blood group, emergency contacts, and active risk factors the moment they are dispatched.

---

## 🛠️ Tech Stack & Architecture

### **Frontend Interface**
- **Framework:** Next.js 16 (App Router), React
- **Styling:** Tailwind CSS
- **Language:** TypeScript
- **Deployment:** Vercel

### **Backend Intelligence (Microservice)**
- **Framework:** Python, FastAPI, Uvicorn
- **Machine Learning:** Pandas, Scikit-Learn (Predictive Risk Modeling)
- **Deployment & Networking:** Ngrok secure tunneling (Linking Vercel Edge directly to the Python microservice)

### **Database & Cloud Infrastructure**
- **Database:** PostgreSQL
- **Storage:** AWS S3 (Secure medical document & report storage)
- **Monitoring:** AWS CloudWatch (Audit logging and compliance tracking)
- **OCR Engine:** Jina AI (Medical Document Extraction)

---

## 🚀 How It Works (The Data Flow)
1. **Input:** Mother asks a question via Voice (STT) or uploads a medical report via the Next.js Frontend.
2. **Processing:** The frontend securely routes the payload to the Python Backend Microservice.
3. **Analysis:** The AI cross-references the input with the mother's PostgreSQL medical history and evaluates against standardized obstetric guidelines.
4. **Triage:** 
   - *Routine Query:* AI responds immediately via Voice (TTS).
   - *Critical Query:* AI halts, queues the query in the HITL Clinician dashboard, and alerts the on-duty doctor.
5. **Action:** Doctors approve/modify the advice, or in severe cases, dispatch an ambulance—providing EMTs with full digital context before they arrive.

---

## ⚠️ Clinical Governance & Safety Notice
MaternaCare provides **Decision Support, Not Autonomous Diagnosis**. The AI is strictly bound by obstetric safety guidelines. All high-risk AI triage flags must be verified by an authorized clinician before becoming trusted clinical history. Patient data access is protected by Role-Based Access Control (RBAC) and immutable AWS CloudWatch Audit Logs.
