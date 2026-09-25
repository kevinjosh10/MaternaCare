"""
MaternaCare Model 4: Main Medical Brain (Clinical Reasoning Engine).
Acts as the clinical intelligence core for Indian maternal and neonatal healthcare.
Evaluates 122 diagnostic test parameters, past obstetric complications, and real-time symptoms.
Enforces Human-In-The-Loop (HITL) doctor approval whenever medical or dietary advice is proposed.
"""

import re
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from app.medical_brain.catalog import MASTER_TESTS_CATALOG, get_test_by_id, LifeStage
from app.medical_brain.past_history_analyzer import (
    PastObstetricHistoryProfile, PastHistoryAnalyzer, HistoryAnalysisReport
)


class TestResultInput(BaseModel):
    __test__ = False  # Prevent pytest from treating this Pydantic model as a test class
    test_id: int = Field(..., description="ID from Master Diagnostic Catalog (1 - 122)")
    value: Any = Field(..., description="Observed result or clinical value")
    date_performed: Optional[str] = None
    is_abnormal: Optional[bool] = None
    notes: Optional[str] = None


class PatientClinicalContext(BaseModel):
    patient_id: str = Field(default_factory=lambda: f"PAT-{uuid.uuid4().hex[:8].upper()}")
    patient_name: str = "Pregnant Mother"
    age: int = 25
    gestational_age_weeks: Optional[float] = None
    current_trimester: Optional[str] = "THIRD_TRIMESTER"
    life_stage: LifeStage = LifeStage.THIRD_TRIMESTER
    past_history: Optional[PastObstetricHistoryProfile] = None
    recent_symptoms: List[str] = []
    current_query_text: Optional[str] = None
    test_results: List[TestResultInput] = []


class HITLApprovalStatus(BaseModel):
    is_approval_required: bool
    status: str  # "APPROVED_DIRECT", "PENDING_APPROVAL", "DOCTOR_APPROVED", "DOCTOR_EDITED", "DOCTOR_REJECTED"
    trigger_reasons: List[str] = []
    proposed_advice: str
    doctor_notes: Optional[str] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None


class MedicalBrainAnalysisResponse(BaseModel):
    analysis_id: str = Field(default_factory=lambda: f"MBA-{uuid.uuid4().hex[:10].upper()}")
    patient_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_high_risk: bool
    risk_level: str  # LOW, MODERATE, HIGH, CRITICAL
    detected_syndromes: List[str] = []
    clinical_patterns_identified: List[str] = []
    abnormal_tests_detected: List[Dict[str, Any]] = []
    past_history_evaluation: Optional[HistoryAnalysisReport] = None
    medical_advice_english: str
    patient_friendly_english: str
    hitl_approval: HITLApprovalStatus
    referral_recommended: bool
    recommended_referral_facility: Optional[str] = None
    action_items_for_clinician: List[str] = []


class MainMedicalBrainEngine:
    """
    Model 4: Core Medical Knowledge & Reasoning Brain.
    Comprehensive diagnostic assessment across all 122 clinical parameters.
    """

    # HITL Trigger Keywords: If these appear in proposed advice, routing mandates doctor approval
    HITL_TRIGGER_KEYWORDS = [
        "medicine", "tablets", "tablet", "syrup", "injection", "infusion", "capsule", "dose", "dosage",
        "tea", "diet", "food", "remedy", "remedies", "supplement", "herbal", "aspirin", "labetalol",
        "nifedipine", "methyldopa", "insulin", "metformin", "betamethasone", "dexamethasone",
        "iron", "ferrous", "calcium", "folic acid", "progesterone", "oxytocin", "misoprostol",
        "magnesium sulfate", "mgso4", "antibiotic", "ampicillin", "ceftriaxone", "levothyroxine",
        "udca", "ursodeoxycholic", "paracetamol", "sertraline", "alprostadil"
    ]

    def __init__(self):
        self.catalog = MASTER_TESTS_CATALOG
        self.history_analyzer = PastHistoryAnalyzer()

    def evaluate_test_results(self, tests: List[TestResultInput]) -> List[Dict[str, Any]]:
        """
        Validates submitted tests against the 122 parameter catalog and detects abnormalities.
        Covers numeric boundaries, qualitative findings, and clinical danger thresholds.
        """
        abnormal_list = []
        for t in tests:
            cat_entry = get_test_by_id(t.test_id)
            if not cat_entry:
                continue

            val_str = str(t.value).lower().strip()
            is_abnormal = False
            clinical_interpretation = ""

            # Check explicit flag
            if t.is_abnormal is True:
                is_abnormal = True

            # Extract numbers for quantitative rules
            nums = [float(n) for n in re.findall(r"\d+\.?\d*", val_str)]

            # -----------------------------------------------------------------
            # 1. First Trimester Key Tests
            # -----------------------------------------------------------------
            if t.test_id == 1:  # Urine hCG
                if any(x in val_str for x in ["negative", "faint", "absent"]):
                    is_abnormal = True
                    clinical_interpretation = "Negative or faint hCG with amenorrhea requires exclusion of ectopic pregnancy."
            elif t.test_id == 2:  # Quantitative Serum Beta-hCG
                if any(x in val_str for x in ["subnormal", "plateau", "drop", "ectopic", "< 66%"]):
                    is_abnormal = True
                    clinical_interpretation = "Subnormal beta-hCG kinetics raises suspicion for non-viable or ectopic pregnancy."
            elif t.test_id == 3:  # Dating & Viability TVS
                if any(x in val_str for x in ["no heartbeat", "absent cardiac", "no fhr", "empty sac", "anembryonic"]):
                    is_abnormal = True
                    clinical_interpretation = "Absent cardiac activity or empty gestational sac indicates non-viable pregnancy."
            elif t.test_id == 4:  # Complete Blood Count (CBC)
                if nums:
                    hb_val = nums[0]
                    if hb_val < 7.0:
                        is_abnormal = True
                        clinical_interpretation = f"Severe Anemia detected (Hb {hb_val} g/dL, threshold < 7.0 g/dL)."
                    elif hb_val < 11.0:
                        is_abnormal = True
                        clinical_interpretation = f"Maternal Anemia detected (Hb {hb_val} g/dL, threshold < 11.0 g/dL)."
                if "platelet" in val_str or any(x in val_str for x in ["thrombocytopenia", "low plate"]):
                    is_abnormal = True
                    clinical_interpretation = "Thrombocytopenia flagged on CBC."
            elif t.test_id == 5:  # Blood Grouping & Rh(D) Factor
                if "negative" in val_str or "rh-" in val_str:
                    is_abnormal = True
                    clinical_interpretation = "Rh(D) Negative mother identified. Mandatory ICT surveillance & Anti-D prophylaxis required."
            elif t.test_id == 6:  # Indirect Coombs Test (ICT)
                if "positive" in val_str or "reactive" in val_str:
                    is_abnormal = True
                    clinical_interpretation = "Positive Indirect Coombs Test indicates maternal Rh isoimmunization."
            elif t.test_id in [7, 8, 9, 10]:  # Infectious Screen: VDRL, HBsAg, HIV, HCV
                if any(x in val_str for x in ["reactive", "positive", "+ve"]):
                    is_abnormal = True
                    clinical_interpretation = f"Seroreactive on {cat_entry['name']}. Immediate vertical transmission prevention protocol indicated."
            elif t.test_id == 11:  # Rubella
                if "igm positive" in val_str or "igm +" in val_str:
                    is_abnormal = True
                    clinical_interpretation = "Rubella IgM positive warns of primary maternal rubella infection."
            elif t.test_id == 12:  # TSH
                if nums and nums[0] > 2.5:
                    is_abnormal = True
                    clinical_interpretation = f"Elevated maternal TSH ({nums[0]} mIU/L). Risk of maternal hypothyroidism."
            elif t.test_id == 14:  # HPLC Thalassemia
                if any(x in val_str for x in ["hba2 > 3.5", "carrier", "trait", "sickle", "thalassemia"]):
                    is_abnormal = True
                    clinical_interpretation = "Hemoglobinopathy trait detected on HPLC. Paternal partner screening required."
            elif t.test_id == 15:  # Fasting Blood Sugar
                if nums and nums[0] >= 92.0:
                    is_abnormal = True
                    clinical_interpretation = f"Fasting blood sugar ({nums[0]} mg/dL) exceeds FOGSI/DIPSI cutoff (92 mg/dL)."
            elif t.test_id == 18:  # First Trimester Combined Screen (NT + Double Marker)
                if any(x in val_str for x in ["high risk", "screen positive", "> 3.0", "increased nt"]):
                    is_abnormal = True
                    clinical_interpretation = "Screen positive for fetal aneuploidy on combined screening."
            elif t.test_id == 24:  # Uterine Artery Doppler (T1)
                if any(x in val_str for x in ["notch", "high resistance", "> 1.5", "> 95"]):
                    is_abnormal = True
                    clinical_interpretation = "Abnormal Uterine Artery Doppler pulsatility index with notches. High risk for early preeclampsia/FGR."

            # -----------------------------------------------------------------
            # 2. Second Trimester Key Tests
            # -----------------------------------------------------------------
            elif t.test_id == 27:  # Targeted Anomaly Scan (Level II / TIFFA)
                if any(x in val_str for x in ["defect", "anomaly", "cleft", "ventriculomegaly", "holoprosencephaly", "spina bifida", "abnormal"]):
                    is_abnormal = True
                    clinical_interpretation = "Fetal structural anomaly detected on Targeted Ultrasound (Level II)."
            elif t.test_id == 28:  # Fetal Echocardiography
                if any(x in val_str for x in ["vsd", "asd", "tetralogy", "transposition", "chd", "abnormal"]):
                    is_abnormal = True
                    clinical_interpretation = "Fetal congenital heart disease identified on Fetal Echo."
            elif t.test_id == 29:  # Cervical Length (TVS)
                if nums and nums[0] < 25.0:
                    is_abnormal = True
                    clinical_interpretation = f"Shortened cervical length ({nums[0]} mm, cutoff < 25 mm). High risk for spontaneous preterm labor."
            elif t.test_id == 35:  # 75g OGTT (DIPSI / WHO)
                if any(x in val_str for x in ["gdm", "impaired", "elevated", ">= 140"]) or any(n >= 140.0 for n in nums):
                    is_abnormal = True
                    val_display = next((n for n in nums if n >= 140.0), t.value)
                    clinical_interpretation = f"75g OGTT confirms Gestational Diabetes Mellitus ({val_display} mg/dL >= 140 mg/dL cutoff per DIPSI)."

            # -----------------------------------------------------------------
            # 3. Third Trimester Key Tests
            # -----------------------------------------------------------------
            elif t.test_id == 40:  # Umbilical Artery Doppler
                if any(x in val_str for x in ["aedv", "redv", "absent", "reversed", "high pi", "elevated ri"]):
                    is_abnormal = True
                    clinical_interpretation = "Critical Umbilical Artery Doppler abnormality (AEDV/REDV). Severe placental insufficiency."
            elif t.test_id == 41:  # MCA Doppler (MCA-PSV / CPR)
                if any(x in val_str for x in ["brain sparing", "cpr < 1", "psv > 1.5", "anemia"]) or any(n >= 1.5 for n in nums):
                    is_abnormal = True
                    val_display = next((n for n in nums if n >= 1.5), t.value)
                    clinical_interpretation = f"Elevated MCA-PSV ({val_display} MoM >= 1.5 MoM cutoff). Severe fetal anemia / brain sparing."
            elif t.test_id == 42:  # Ductus Venosus Doppler
                if any(x in val_str for x in ["absent a", "reversed a", "negative a", "abnormal"]):
                    is_abnormal = True
                    clinical_interpretation = "Ductus Venosus reversed 'a' wave indicates severe fetal acidosis / impending demise."
            elif t.test_id == 44:  # Blood Pressure
                if len(nums) >= 2:
                    sys_p, dia_p = nums[0], nums[1]
                    if sys_p >= 140 or dia_p >= 90:
                        is_abnormal = True
                        if sys_p >= 160 or dia_p >= 110:
                            clinical_interpretation = f"Severe Preeclampsia BP ({int(sys_p)}/{int(dia_p)} mmHg)."
                        else:
                            clinical_interpretation = f"Hypertensive BP ({int(sys_p)}/{int(dia_p)} mmHg)."
            elif t.test_id == 45:  # Urine Protein / UPCR
                if any(x in val_str for x in ["proteinuria", ">= 0.3", "1+", "2+", "3+", "4+", "trace", "300 mg"]):
                    is_abnormal = True
                    clinical_interpretation = "Significant proteinuria detected on UPCR / dipstick."
            elif t.test_id == 46:  # Serum sFlt-1 / PlGF Ratio
                if nums and nums[0] > 38.0:
                    is_abnormal = True
                    clinical_interpretation = f"Elevated sFlt-1/PlGF ratio ({nums[0]}). Confirms high imminent preeclampsia risk."
            elif t.test_id == 47:  # Liver Function Tests (AST/ALT)
                if any(x in val_str for x in ["elevated", "> 70", "high ast", "high alt", "hellp"]):
                    is_abnormal = True
                    clinical_interpretation = "Elevated hepatic transaminases. HELLP syndrome concern."
                elif nums and max(nums) > 70.0:
                    is_abnormal = True
                    clinical_interpretation = f"Transaminases markedly elevated ({max(nums)} U/L > 70 U/L cutoff). HELLP syndrome alert."
            elif t.test_id == 49:  # Total Serum Bile Acids (TBA)
                if nums and nums[0] >= 10.0:
                    is_abnormal = True
                    severity = "Severe" if nums[0] >= 40.0 else "Mild"
                    clinical_interpretation = f"{severity} Intrahepatic Cholestasis of Pregnancy (TBA {nums[0]} umol/L)."
                elif any(x in val_str for x in ["icp", "cholestasis", "elevated bile", "pruritus", "palms"]):
                    is_abnormal = True
                    clinical_interpretation = "Intrahepatic Cholestasis of Pregnancy confirmed."
            elif t.test_id == 51:  # Coagulation Profile
                if any(x in val_str for x in ["dic", "fibrinogen < 200", "platelets < 100", "inr > 1.5", "abnormal"]):
                    is_abnormal = True
                    clinical_interpretation = "Disseminated Intravascular Coagulation (DIC) or consumptive coagulopathy."
            elif t.test_id == 52:  # Group B Strep (GBS)
                if "positive" in val_str or "+ve" in val_str:
                    is_abnormal = True
                    clinical_interpretation = "GBS culture positive. Intrapartum IV antibiotic prophylaxis mandatory."
            elif t.test_id == 54:  # Cardiotocography (CTG / NST)
                if any(x in val_str for x in ["category iii", "category 3", "non-reactive", "decelerations", "bradycardia"]):
                    is_abnormal = True
                    clinical_interpretation = "Abnormal / Category III CTG showing acute fetal compromise."
            elif t.test_id == 57:  # Amniotic Fluid Index (AFI)
                if nums:
                    afi_val = nums[0]
                    if afi_val < 5.0:
                        is_abnormal = True
                        clinical_interpretation = f"Oligohydramnios (AFI {afi_val} cm < 5.0 cm cutoff)."
                    elif afi_val > 25.0:
                        is_abnormal = True
                        clinical_interpretation = f"Polyhydramnios (AFI {afi_val} cm > 25.0 cm cutoff)."

            # -----------------------------------------------------------------
            # 4. Labor, Postpartum & Neonatal Tests
            # -----------------------------------------------------------------
            elif t.test_id == 66:  # Postpartum Blood Loss
                if nums and (nums[0] > 500.0 or any(x in val_str for x in ["pph", "hemorrhage", "heavy bleed"])):
                    is_abnormal = True
                    clinical_interpretation = f"Postpartum Hemorrhage detected (measured loss {nums[0]} mL)."
            elif t.test_id == 74:  # EPDS (Postnatal Depression)
                if (nums and nums[0] >= 13.0) or any(x in val_str for x in ["severe", "self harm", "suicid"]):
                    is_abnormal = True
                    clinical_interpretation = "High risk for Severe Postpartum Depression on EPDS."
            elif t.test_id == 77:  # APGAR Score
                if nums and nums[0] < 7:
                    is_abnormal = True
                    clinical_interpretation = f"Low APGAR score ({nums[0]} at 5 min). Birth depression requiring resuscitation."
            elif t.test_id == 80:  # CCHD Pulse Oximetry
                if any(x in val_str for x in ["fail", "refer", "gradient > 3", "< 90", "abnormal"]):
                    is_abnormal = True
                    clinical_interpretation = "Failed CCHD screen. Possible duct-dependent cyanotic heart disease."
            elif t.test_id == 81:  # Neonatal Bilirubin
                if (nums and nums[0] > 15.0) or any(x in val_str for x in ["jaundice", "phototherapy", "hyperbilirubinemia"]):
                    is_abnormal = True
                    clinical_interpretation = f"Significant neonatal hyperbilirubinemia ({t.value}). Phototherapy indicated."
            elif t.test_id == 82:  # Neonatal Glucose
                if nums and nums[0] < 45.0:
                    is_abnormal = True
                    clinical_interpretation = f"Neonatal Hypoglycemia ({nums[0]} mg/dL < 45 mg/dL cutoff)."
            elif t.test_id == 90:  # Guthrie TSH
                if any(x in val_str for x in ["> 20", "> 15", "elevated", "high", "positive"]) or (nums and nums[0] > 20.0):
                    is_abnormal = True
                    clinical_interpretation = "Elevated neonatal blood spot TSH. Congenital hypothyroidism alert."

            # Universal Fallback: Check danger threshold keywords in catalog
            if not is_abnormal:
                danger_text = str(cat_entry.get("danger_threshold", "")).lower()
                danger_keywords = [
                    "abnormal", "positive", "reactive", "fail", "refer", "elevated", "severe",
                    "critical", "high risk", "present", "notches", "aedv", "redv", "oligohydramnios"
                ]
                if any(kw in val_str for kw in danger_keywords):
                    is_abnormal = True
                    clinical_interpretation = f"Result flags clinical attention per {cat_entry['name']} danger guideline: {cat_entry['danger_threshold']}."

            if is_abnormal:
                abnormal_list.append({
                    "test_id": t.test_id,
                    "test_name": cat_entry["name"],
                    "stage": cat_entry["stage"].value,
                    "specimen": cat_entry["specimen"].value,
                    "observed_value": t.value,
                    "normal_range": cat_entry["normal_range"],
                    "danger_threshold": cat_entry["danger_threshold"],
                    "clinical_interpretation": clinical_interpretation or cat_entry["indian_clinical_protocol"]
                })

        return abnormal_list

    def check_hitl_approval_required(self, proposed_text: str) -> HITLApprovalStatus:
        """
        Scans proposed response. If it contains words like medicine, tablets, syrup, tea, diet, food, remedies,
        pauses pipeline and routes to PENDING_APPROVAL.
        """
        text_lower = proposed_text.lower()
        triggers = []
        for kw in self.HITL_TRIGGER_KEYWORDS:
            if re.search(r"\b" + re.escape(kw) + r"\b", text_lower):
                triggers.append(kw)

        triggers = sorted(list(set(triggers)))
        if triggers:
            return HITLApprovalStatus(
                is_approval_required=True,
                status="PENDING_APPROVAL",
                trigger_reasons=[f"Proposed advice contains clinical/dietary keywords: {', '.join(triggers)}"],
                proposed_advice=proposed_text
            )
        else:
            return HITLApprovalStatus(
                is_approval_required=False,
                status="APPROVED_DIRECT",
                trigger_reasons=[],
                proposed_advice=proposed_text
            )

    def analyze_patient(self, context: PatientClinicalContext) -> MedicalBrainAnalysisResponse:
        """
        Main entry point for Model 4 clinical reasoning.
        Evaluates history, tests, and clinical presentation into actionable triage.
        """
        concerning_patterns: List[str] = []
        detected_syndromes: List[str] = []
        action_items: List[str] = []
        is_high_risk = False
        risk_level = "LOW"
        referral_needed = False
        referral_facility = None

        # 1. Analyze Past Obstetric History
        history_report = None
        if context.past_history:
            history_report = self.history_analyzer.analyze_history(context.past_history)
            if history_report.is_high_risk_pregnancy:
                is_high_risk = True
                risk_level = history_report.risk_level
                concerning_patterns.extend(history_report.primary_risk_drivers)
                for alert in history_report.alerts:
                    action_items.append(f"History Action: {alert.clinical_action_plan}")

        # 2. Evaluate 122 Clinical Tests
        abnormal_tests = self.evaluate_test_results(context.test_results)
        test_ids_abnormal = {ab["test_id"] for ab in abnormal_tests}

        for ab in abnormal_tests:
            is_high_risk = True
            concerning_patterns.append(f"Abnormal {ab['test_name']}: {ab['observed_value']} ({ab['clinical_interpretation']})")

        # 3. Evaluate Current Symptoms & Voice Query
        query_text = (context.current_query_text or "").lower()
        all_symptoms = [s.lower() for s in context.recent_symptoms]

        # Safeguard against false positives and negation (e.g. "no bleeding", "normal movements", "blood group")
        def symptom_positive(keywords: List[str], text_sources: List[str]) -> bool:
            for text in text_sources:
                t = text.lower()
                for kw in keywords:
                    if kw in t:
                        negation_match = re.search(r"(no|not|neither|without|denies|negative for|normal)\s+([a-z\s]{0,15})" + re.escape(kw), t)
                        if not negation_match:
                            return True
            return False

        has_headache_or_vision = symptom_positive(
            ["headache", "blurred vision", "blurring", "vision loss", "scotoma", "epigastric pain", "epigastric discomfort"],
            [query_text] + all_symptoms
        )
        has_bleeding = symptom_positive(
            ["bleeding", "vaginal bleed", "blood loss", "discharge red", "spotting heavy", "blood clots", "passing blood"],
            [query_text] + all_symptoms
        )
        has_reduced_movements = symptom_positive(
            ["less move", "not moving", "reduced move", "decreased move", "no kicks", "stopped moving", "fetal movement decrease", "less kick", "reduced kick", "no movement", "less active"],
            [query_text] + all_symptoms
        )
        has_pruritus = symptom_positive(
            ["itching", "itchy", "scratching", "pruritus", "palms and soles", "itching on palms", "itching on feet"],
            [query_text] + all_symptoms
        )
        has_fluid_leak = symptom_positive(
            ["water broke", "leaking water", "fluid leaking", "amniotic leak", "copious watery", "rupture of membranes"],
            [query_text] + all_symptoms
        )

        # 4. Multi-Parameter Syndrome Pattern Recognition
        # Pattern A: Preeclampsia / Eclampsia Warning
        if (44 in test_ids_abnormal and 45 in test_ids_abnormal) or (44 in test_ids_abnormal and has_headache_or_vision):
            detected_syndromes.append("Preeclampsia with Severe Features / Impending Eclampsia")
            is_high_risk = True
            risk_level = "CRITICAL" if has_headache_or_vision else "HIGH"
            referral_needed = True
            referral_facility = "TERTIARY_CARE_CENTRE" if has_headache_or_vision else "DISTRICT_HOSPITAL"
            action_items.append("Admit immediately. Administer loading dose IV/IM Magnesium Sulfate (Pritchard/Zuspan regimen). Control BP with IV Labetalol or oral Nifedipine.")

        # Pattern B: HELLP Syndrome
        if 47 in test_ids_abnormal and (4 in test_ids_abnormal or 44 in test_ids_abnormal):
            detected_syndromes.append("HELLP Syndrome (Hemolysis, Elevated Liver Enzymes, Low Platelets)")
            is_high_risk = True
            risk_level = "CRITICAL"
            referral_needed = True
            referral_facility = "TERTIARY_CARE_CENTRE"
            action_items.append("Urgent obstetric stabilization, arrange cross-matched platelets and fresh frozen plasma, plan expedited delivery.")

        # Pattern C: Gestational Diabetes Mellitus (GDM)
        if 15 in test_ids_abnormal or 35 in test_ids_abnormal:
            detected_syndromes.append("Gestational Diabetes Mellitus (DIPSI Protocol)")
            is_high_risk = True
            if risk_level not in ["HIGH", "CRITICAL"]:
                risk_level = "MODERATE"
            action_items.append("Initiate Medical Nutrition Therapy (MNT). Target FBS < 90 mg/dL and 2h-PPBS < 120 mg/dL. Self-monitoring of blood glucose (SMBG).")

        # Pattern D: Intrahepatic Cholestasis of Pregnancy (ICP)
        if 49 in test_ids_abnormal or (has_pruritus and 47 in test_ids_abnormal):
            detected_syndromes.append("Intrahepatic Cholestasis of Pregnancy (ICP)")
            is_high_risk = True
            risk_level = "HIGH"
            referral_needed = True
            referral_facility = "DISTRICT_HOSPITAL"
            action_items.append("Prescribe Ursodeoxycholic Acid (UDCA) 300 mg TID, close fetal surveillance (bi-weekly CTG), plan delivery at 37 weeks to prevent stillbirth.")

        # Pattern E: Severe Fetal Compromise / Placental Insufficiency
        if 40 in test_ids_abnormal or 42 in test_ids_abnormal:
            detected_syndromes.append("Severe Placental Insufficiency with Fetal Compromise (Doppler AEDV/REDV)")
            is_high_risk = True
            risk_level = "CRITICAL"
            referral_needed = True
            referral_facility = "TERTIARY_CARE_CENTRE"
            action_items.append("Urgent admission to tertiary obstetrics with NICU backup. Administer antenatal corticosteroids (Betamethasone 12 mg IM). Plan timed delivery.")

        # Pattern F: Antepartum Hemorrhage (APH)
        if has_bleeding:
            detected_syndromes.append("Antepartum Hemorrhage (Suspected Placenta Previa or Abruptio Placentae)")
            is_high_risk = True
            risk_level = "CRITICAL"
            referral_needed = True
            referral_facility = "TERTIARY_CARE_CENTRE"
            concerning_patterns.append("Active vaginal bleeding reported (High risk of maternal-fetal exsanguination)")
            action_items.append("Do NOT perform digital vaginal examination. Insert two large-bore IV cannulae, type and cross-match 2 units packed RBCs, urgent bedside ultrasound.")

        # Pattern G: Decreased Fetal Movements
        if has_reduced_movements:
            is_high_risk = True
            if risk_level not in ["CRITICAL"]:
                risk_level = "HIGH"
            concerning_patterns.append("Subjective reduction in fetal movement (Fetal compromise alert)")
            action_items.append("Perform immediate Non-Stress Test (NST) and Biophysical Profile (mBPP).")

        # Pattern H: Premature Rupture of Membranes (PROM)
        if has_fluid_leak:
            is_high_risk = True
            if risk_level not in ["CRITICAL"]:
                risk_level = "HIGH"
            concerning_patterns.append("Sudden watery vaginal discharge concerning for Rupture of Membranes")
            action_items.append("Sterile speculum exam to assess pooling, check nitrazine/ferning, monitor maternal vitals for chorioamnionitis.")

        # Pattern I: Neonatal Urgent Emergencies
        if 80 in test_ids_abnormal:
            detected_syndromes.append("Failed CCHD Screening (Cyanotic Congenital Heart Defect Alert)")
            is_high_risk = True
            risk_level = "CRITICAL"
            referral_needed = True
            referral_facility = "TERTIARY_CARE_CENTRE"
            action_items.append("Immediate Pediatric Echocardiogram. Maintain patent ductus arteriosus with IV Alprostadil if indicated.")
        if 90 in test_ids_abnormal:
            detected_syndromes.append("Congenital Hypothyroidism Alert (Guthrie TSH)")
            is_high_risk = True
            if risk_level not in ["CRITICAL"]:
                risk_level = "HIGH"
            action_items.append("Confirmatory serum free T4 & total TSH within 48h. Initiate oral Levothyroxine 10-15 mcg/kg/day within 2 weeks of birth to prevent neurocognitive deficit.")

        # Pattern J: Rh Isoimmunization & Fetal Anemia
        if 6 in test_ids_abnormal or (5 in test_ids_abnormal and 41 in test_ids_abnormal):
            detected_syndromes.append("Rh Isoimmunization with Fetal Anemia Surveillance (Positive ICT)")
            is_high_risk = True
            risk_level = "CRITICAL" if 41 in test_ids_abnormal else "HIGH"
            referral_needed = True
            referral_facility = "TERTIARY_CARE_CENTRE"
            action_items.append("Immediate tertiary referral to Fetal Medicine Unit. Serial MCA-PSV Doppler tracking. Prepare for intrauterine fetal blood transfusion (IUT) if MCA-PSV > 1.5 MoM.")

        # Pattern K: Severe Maternal Anemia
        if 4 in test_ids_abnormal:
            for ab in abnormal_tests:
                if ab["test_id"] == 4 and "severe" in ab.get("clinical_interpretation", "").lower():
                    detected_syndromes.append("Severe Maternal Anemia (Hb < 7.0 g/dL)")
                    is_high_risk = True
                    if risk_level not in ["CRITICAL"]:
                        risk_level = "HIGH"
                    referral_needed = True
                    referral_facility = "DISTRICT_HOSPITAL"
                    action_items.append("Admit for parenteral iron sucrose or ferric carboxymaltose infusion under obstetric supervision per MoHFW Anemia Mukt Bharat guidelines.")

        # General Referral Logic
        if is_high_risk and not referral_needed:
            if risk_level in ["HIGH", "CRITICAL"]:
                referral_needed = True
                if not referral_facility:
                    referral_facility = "DISTRICT_HOSPITAL" if risk_level == "HIGH" else "TERTIARY_CARE_CENTRE"

        # 5. Formulate Authoritative Medical Advice & Patient Friendly Response
        # Dynamic response generation based on the query to prevent repetitive answers
        
        if is_high_risk:
            patterns_summary = f"{len(concerning_patterns)} concerning clinical risk indicators"
            if detected_syndromes:
                patterns_summary += f" ({', '.join(detected_syndromes)})"
            
            medical_advice_english = (
                f"Potentially concerning pattern detected — clinical review recommended. "
                f"Evaluation reveals {patterns_summary}. "
                f"{' '.join(action_items[:4]) if action_items else 'Urgent clinical assessment required.'} "
                f"Adheres to applicable FOGSI/WHO protocols."
            )
            patient_friendly_english = (
                f"I have reviewed your records. Based on your {patterns_summary}, this requires immediate medical attention. "
                f"Please do not wait. Go to your nearest healthcare facility or contact your doctor immediately."
            )
            
        else:
            # -------------------------------------------------------------------------
            # Patient-Specific Local Text Generation Model
            # -------------------------------------------------------------------------
            # We will use the dynamically trained local model specific to THIS woman's pregnancy
            try:
                from app.ai_models.patient_specific_model import patient_specific_qa_model
                
                patient_id = context.patient_id
                local_response = patient_specific_qa_model.generate_answer(query_text, patient_id)
                
                medical_advice_english = local_response["medical_advice_english"]
                patient_friendly_english = local_response["patient_friendly_english"]
            except ImportError:
                # Fallback if the personalized model isn't trained/available yet
                if "medicine" in query_text.lower() or "tablet" in query_text.lower() or "paracetamol" in query_text.lower():
                    medical_advice_english = "Patient inquired about medications. Advised standard paracetamol for pain relief."
                    patient_friendly_english = "For mild pain or fever, taking a standard paracetamol tablet is generally considered safe, but always verify with your doctor before starting any new medicine."
                else:
                    medical_advice_english = f"Patient inquired about: '{query_text}'. No clinical red flags identified. Advised standard antenatal care."
                    patient_friendly_english = f"Thank you for your question. As long as you are not experiencing severe pain, bleeding, or reduced baby movements, please continue your routine care and discuss this with your doctor."

        if history_report and history_report.preventive_prescriptions_indicated:
            medical_advice_english += " Recommended preventive medications to be confirmed by doctor: " + "; ".join(history_report.preventive_prescriptions_indicated) + "."

        # 7. Apply Human-In-The-Loop (HITL) Check
        hitl_status = self.check_hitl_approval_required(medical_advice_english + " " + patient_friendly_english)

        return MedicalBrainAnalysisResponse(
            patient_id=context.patient_id,
            is_high_risk=is_high_risk,
            risk_level=risk_level,
            detected_syndromes=detected_syndromes,
            clinical_patterns_identified=concerning_patterns,
            abnormal_tests_detected=abnormal_tests,
            past_history_evaluation=history_report,
            medical_advice_english=medical_advice_english,
            patient_friendly_english=patient_friendly_english,
            hitl_approval=hitl_status,
            referral_recommended=referral_needed,
            recommended_referral_facility=referral_facility,
            action_items_for_clinician=action_items
        )


medical_brain = MainMedicalBrainEngine()
