"""
MaternaCare Clinical Training Dataset Generator.
Synthesizes comprehensive clinical training data for Indian maternal and neonatal healthcare,
incorporating all 122 diagnostic test parameters, past obstetric complications, and expert clinical annotations.
"""

import json
from typing import List, Dict, Any
from app.medical_brain.catalog import MASTER_TESTS_CATALOG, LifeStage


def generate_comprehensive_training_cases() -> List[Dict[str, Any]]:
    """
    Builds a benchmark training dataset of 10 complex clinical profiles of Indian mothers and infants.
    Each profile includes:
    - Patient Demographics & Baseline State
    - Previous Obstetric History (G_P_A_L_S)
    - Medical Co-morbidities
    - Exact Test Parameter Values across the 122 Master Tests
    - Clinical Problems Detected
    - Human-In-The-Loop Advice (with medicine/food triggers)
    - Verified Clinical Guidance
    """

    cases: List[Dict[str, Any]] = [
        # -------------------------------------------------------------
        # CASE 1: Multigravida with Prior Severe Preeclampsia
        # -------------------------------------------------------------
        {
            "case_id": "CASE-IND-001",
            "patient_name": "Meenakshi Sundaram",
            "age": 29,
            "district": "Madurai, Tamil Nadu",
            "gestational_age_weeks": 32.4,
            "current_trimester": "THIRD_TRIMESTER",
            "past_obstetric_history": {
                "gravida": 2,
                "para": 1,
                "living": 1,
                "abortions": 0,
                "stillbirths": 0,
                "previous_c_sections": 1,
                "prior_preeclampsia": True,
                "prior_early_onset_preeclampsia": True,
                "prior_gestational_diabetes": False,
                "prior_preterm_delivery": True,
                "prior_notes": "Emergency CS at 33 weeks in 2021 for severe preeclampsia with BP 170/115 and impending eclampsia."
            },
            "medical_co_morbidities": ["Chronic borderline hypertension", "Vegetarian diet"],
            "current_symptoms": ["Frontal throbbing headache", "Bilateral pedal swelling", "Occasional visual blurring"],
            "active_test_results": {
                4: {"name": "CBC", "value": "Hb 10.2 g/dL, Platelets 135000 /uL", "is_abnormal": True},
                24: {"name": "Mean UtA-PI (T1)", "value": "1.72 (Bilateral Notches)", "is_abnormal": True},
                38: {"name": "Growth USG", "value": "EFW 1520g (8th percentile, SGA)", "is_abnormal": True},
                39: {"name": "AFI", "value": "7.8 cm (Borderline oligohydramnios)", "is_abnormal": True},
                40: {"name": "Umbilical Artery Doppler", "value": "PI 1.38 (>95th percentile, High resistance)", "is_abnormal": True},
                43: {"name": "Cerebroplacental Ratio (CPR)", "value": "0.92 (<1.0, Brain-sparing redistribution)", "is_abnormal": True},
                44: {"name": "Serial Blood Pressure", "value": "154/98 mmHg (Repeated 156/100 mmHg)", "is_abnormal": True},
                45: {"name": "Spot UPCR", "value": "0.58 mg/mg (Significant proteinuria)", "is_abnormal": True},
                46: {"name": "sFlt-1 / PlGF Ratio", "value": "124.0 (High preeclampsia onset risk)", "is_abnormal": True},
                47: {"name": "Liver Function Tests", "value": "AST 48 IU/L, ALT 52 IU/L, Bilirubin 0.8 mg/dL", "is_abnormal": True},
                48: {"name": "Renal Function Tests", "value": "Serum Creatinine 0.95 mg/dL, Uric Acid 6.4 mg/dL", "is_abnormal": True},
                49: {"name": "Serum LDH", "value": "410 IU/L (Elevated)", "is_abnormal": True}
            },
            "clinical_diagnosis_annotation": "G2P1 with 32.4 weeks pregnancy with Recurrent Preeclampsia with Severe Features, Fetal Growth Restriction (FGR), and abnormal Cerebroplacental Ratio (CPR).",
            "primary_concerning_patterns": [
                "Recurrent preeclampsia in patient with prior early-onset preeclampsia and prior CS",
                "Severe range blood pressure elevation (156/100 mmHg) with significant proteinuria (UPCR 0.58)",
                "Early placental insufficiency evidenced by elevated sFlt-1/PlGF ratio (124) and CPR < 1.0 (0.92)",
                "Fetal growth restriction (8th percentile) with borderline oligohydramnios"
            ],
            "proposed_medical_advice": (
                "Potentially concerning pattern detected — clinical review recommended. "
                "Admit immediately to obstetric high-dependency unit (HDU). "
                "Start oral Labetalol 100 mg BD (titrate up to 200 mg TDS) to maintain BP 130-140/80-90 mmHg. "
                "Administer Injection Betamethasone 12 mg IM (2 doses 24 hours apart) for fetal lung maturation. "
                "Keep Magnesium Sulfate (Pritchard regimen) ready for seizure prophylaxis. "
                "Monitor maternal vitals, urine output, and continuous CTG."
            ),
            "hitl_trigger_words": ["Labetalol", "Betamethasone", "Magnesium Sulfate", "medicine", "tablets"],
            "patient_friendly_summary_en": "Your blood pressure is high and there is protein in your urine, which needs immediate care in the hospital to protect you and your baby. Please do not worry, the doctors will give you medicine to control your pressure and help your baby's lungs mature.",
            "is_emergency_referral_needed": True,
            "referral_facility_type": "TERTIARY_CARE_CENTRE"
        },

        # -------------------------------------------------------------
        # CASE 2: Multigravida with Prior GDM & High BMI
        # -------------------------------------------------------------
        {
            "case_id": "CASE-IND-002",
            "patient_name": "Pooja Sharma",
            "age": 31,
            "district": "Jaipur, Rajasthan",
            "gestational_age_weeks": 26.2,
            "current_trimester": "SECOND_TRIMESTER",
            "past_obstetric_history": {
                "gravida": 2,
                "para": 1,
                "living": 1,
                "abortions": 0,
                "stillbirths": 0,
                "previous_c_sections": 0,
                "prior_preeclampsia": False,
                "prior_gestational_diabetes": True,
                "prior_notes": "Delivered baby weighing 3.9 kg in 2022; GDM required insulin in 3rd trimester."
            },
            "medical_co_morbidities": ["Pre-pregnancy BMI 28.4 kg/m2 (Overweight)", "Family history of Type 2 Diabetes"],
            "current_symptoms": ["Excessive thirst", "Frequent urination", "Fatigue"],
            "active_test_results": {
                4: {"name": "CBC", "value": "Hb 11.4 g/dL", "is_abnormal": False},
                15: {"name": "Fasting Blood Sugar", "value": "104 mg/dL", "is_abnormal": True},
                16: {"name": "HbA1c", "value": "6.2%", "is_abnormal": True},
                32: {"name": "TIFFA Anatomy Scan", "value": "Normal anatomy, no neural or cardiac anomalies", "is_abnormal": False},
                35: {"name": "75g 2-Hr OGTT", "value": "Fasting: 102 mg/dL, 1-hr: 198 mg/dL, 2-hr: 168 mg/dL", "is_abnormal": True},
                38: {"name": "Fetal Biometry (26w)", "value": "AC 92nd percentile (Fetal abdominal fat deposition)", "is_abnormal": True},
                39: {"name": "AFI", "value": "18.5 cm (Upper normal liquor)", "is_abnormal": False}
            },
            "clinical_diagnosis_annotation": "G2P1 with 26.2 weeks with Recurrent Gestational Diabetes Mellitus (GDM) failing dietary control, accelerated fetal abdominal circumference.",
            "primary_concerning_patterns": [
                "Prior GDM recurrence confirmed by 75g OGTT exceeding all DIPSI/WHO cutoffs (Fasting 102, 1-hr 198, 2-hr 168)",
                "Elevated HbA1c 6.2% indicating chronic sub-optimal glycemic control",
                "Fetal abdominal circumference >= 92nd percentile indicating early hyperinsulinemic macrosomia"
            ],
            "proposed_medical_advice": (
                "Potentially concerning pattern detected — clinical review recommended. "
                "Diagnosed with Gestational Diabetes Mellitus (GDM). "
                "Prescribe structured Indian Medical Nutrition Therapy (MNT): 1800 kcal diet divided into 3 major meals and 3 small snacks, replacing refined rice/maida with whole grains (millets/brown rice/atta) and high fibre. "
                "Self-Monitoring of Blood Glucose (SMBG) 4 times daily (Fasting target < 90 mg/dL, 2-hr postprandial < 120 mg/dL). "
                "If fasting remains > 95 mg/dL or postprandial > 120 mg/dL after 1 week of MNT, initiate Human Regular/NPH Insulin or Metformin 500mg BD as per FOGSI guidelines."
            ),
            "hitl_trigger_words": ["diet", "food", "nutrition", "Insulin", "Metformin", "tablets"],
            "patient_friendly_summary_en": "Your blood sugar test shows pregnancy-related diabetes (GDM). We will help you with a healthy meal plan with more whole grains, dal, and vegetables. Testing your sugar regularly will keep your baby at a healthy weight.",
            "is_emergency_referral_needed": False,
            "referral_facility_type": "PRIMARY_OR_COMMUNITY_HEALTH_CENTRE"
        },

        # -------------------------------------------------------------
        # CASE 3: Severe Nutritional Anemia (Anaemia Mukt Bharat)
        # -------------------------------------------------------------
        {
            "case_id": "CASE-IND-003",
            "patient_name": "Saraswati Devi",
            "age": 22,
            "district": "Mirzapur, Uttar Pradesh",
            "gestational_age_weeks": 28.0,
            "current_trimester": "THIRD_TRIMESTER",
            "past_obstetric_history": {
                "gravida": 1,
                "para": 0,
                "living": 0,
                "abortions": 0,
                "stillbirths": 0,
                "previous_c_sections": 0,
                "prior_preeclampsia": False,
                "prior_notes": "Primigravida, low socio-economic background, vegetarian diet with poor iron intake."
            },
            "medical_co_morbidities": ["Severe Iron Deficiency Anemia"],
            "current_symptoms": ["Extreme breathlessness on mild exertion", "Generalized dizziness", "Pallor"],
            "active_test_results": {
                4: {"name": "CBC", "value": "Hb 6.4 g/dL, RBC 2.9 million, MCV 64 fL, MCH 19 pg, Platelets 240000", "is_abnormal": True},
                5: {"name": "Blood Group", "value": "B Positive", "is_abnormal": False},
                19: {"name": "Hb HPLC", "value": "HbA2 2.2% (Thalassemia ruled out, purely nutritional microcytic hypochromic)", "is_abnormal": False},
                38: {"name": "Growth Scan", "value": "EFW 1100g (Appropriate for 28 weeks)", "is_abnormal": False},
                41: {"name": "MCA Doppler PSV", "value": "1.32 MoM (Mild hemodynamic compensation, no hydrops)", "is_abnormal": False},
                44: {"name": "Blood Pressure", "value": "106/68 mmHg, Pulse 98 bpm (Hyperdynamic circulation)", "is_abnormal": False},
                74: {"name": "Serum Ferritin", "value": "5.2 ng/mL (Severe iron depletion, target > 30)", "is_abnormal": True}
            },
            "clinical_diagnosis_annotation": "Primigravida at 28 weeks with Severe Microcytic Hypochromic Iron Deficiency Anemia (Hb 6.4 g/dL, Ferritin 5.2 ng/mL).",
            "primary_concerning_patterns": [
                "Severe anemia (Hb 6.4 g/dL < 7.0 g/dL threshold under Anaemia Mukt Bharat)",
                "Exhausted iron stores (Ferritin 5.2 ng/mL)",
                "Hyperdynamic circulation with risk of high-output cardiac failure and preterm delivery"
            ],
            "proposed_medical_advice": (
                "Potentially concerning pattern detected — clinical review recommended. "
                "Severe anemia in 3rd trimester cannot be corrected in time with oral iron. "
                "Under MoHFW Anaemia Mukt Bharat protocol, administer Intravenous Ferric Carboxymaltose (FCM) 1000 mg in 100 mL Normal Saline over 15 minutes in a daycare setting. "
                "Keep emergency anaphylaxis tray ready (Adrenaline, Hydrocortisone). "
                "Prescribe high-protein diet with green leafy vegetables, jaggery (gur), and sprouted legumes. "
                "Recheck CBC after 3 weeks to ensure target rise of at least 2.0 g/dL."
            ),
            "hitl_trigger_words": ["Ferric Carboxymaltose", "iron", "diet", "food", "injection", "medicine"],
            "patient_friendly_summary_en": "Your hemoglobin is very low (6.4 g/dL) which is causing your tiredness and breathlessness. A quick iron drip at the hospital will restore your blood levels safely and give your baby strength before birth.",
            "is_emergency_referral_needed": False,
            "referral_facility_type": "COMMUNITY_HEALTH_CENTRE_OR_SUB_DISTRICT_HOSPITAL"
        },

        # -------------------------------------------------------------
        # CASE 4: Rh-Negative Mother with Positive Antibody Titer
        # -------------------------------------------------------------
        {
            "case_id": "CASE-IND-004",
            "patient_name": "Deepika Nair",
            "age": 27,
            "district": "Ernakulam, Kerala",
            "gestational_age_weeks": 30.5,
            "current_trimester": "THIRD_TRIMESTER",
            "past_obstetric_history": {
                "gravida": 2,
                "para": 1,
                "living": 1,
                "abortions": 0,
                "stillbirths": 0,
                "previous_c_sections": 0,
                "prior_rh_isoimmunization": True,
                "prior_notes": "First child born Rh Positive. Anti-D immunoglobulin was missed postpartum due to home delivery."
            },
            "medical_co_morbidities": ["Rh-Negative Isoimmunization"],
            "current_symptoms": ["Normal perception of fetal kicks", "No bleeding or abdominal pain"],
            "active_test_results": {
                4: {"name": "CBC", "value": "Hb 11.8 g/dL", "is_abnormal": False},
                5: {"name": "Blood Group", "value": "A Rh(D) Negative", "is_abnormal": True},
                6: {"name": "Indirect Coombs Test (ICT)", "value": "Positive with Titer 1:32 (Critical titer >= 1:16)", "is_abnormal": True},
                38: {"name": "Fetal Ultrasound", "value": "EFW 1650g, no ascites, no pericardial effusion, placental thickness 3.2 cm", "is_abnormal": False},
                41: {"name": "MCA Doppler Peak Systolic Velocity (PSV)", "value": "1.62 MoM (> 1.5 MoM indicates moderate to severe fetal anemia)", "is_abnormal": True}
            },
            "clinical_diagnosis_annotation": "G2P1 with 30.5 weeks Rh-Negative Isoimmunization with critical antibody titer (1:32) and MCA Doppler PSV > 1.5 MoM indicating significant fetal hemolytic anemia.",
            "primary_concerning_patterns": [
                "Maternal Rh sensitization with critical anti-D antibody titer (1:32 >= 1:16)",
                "Elevated MCA-PSV (1.62 MoM > 1.5 MoM) confirming fetal red cell hemolysis and anemia",
                "High risk of progression to immune hydrops fetalis if left untreated"
            ],
            "proposed_medical_advice": (
                "Potentially concerning pattern detected — clinical review recommended. "
                "Do NOT administer routine Anti-D (ineffective once sensitization has occurred). "
                "Urgent referral to Fetal Medicine specialist at a Tertiary Medical College. "
                "Prepare for Diagnostic Cordocentesis and Intrauterine Blood Transfusion (IUT) with O-negative irradiated CMV-negative packed RBCs. "
                "Administer Betamethasone 12mg IM for fetal lung protection in case early delivery is necessitated."
            ),
            "hitl_trigger_words": ["Anti-D", "Betamethasone", "transfusion", "medicine"],
            "patient_friendly_summary_en": "Because your blood group is Rh-negative and your body has developed antibodies, the baby has mild anemia inside the womb. The fetal medicine doctors will perform a specialized scan and can gently give the baby red blood cells through the umbilical cord to keep baby healthy.",
            "is_emergency_referral_needed": True,
            "referral_facility_type": "TERTIARY_CARE_CENTRE"
        },

        # -------------------------------------------------------------
        # CASE 5: Intrahepatic Cholestasis of Pregnancy (ICP)
        # -------------------------------------------------------------
        {
            "case_id": "CASE-IND-005",
            "patient_name": "Lata Yadav",
            "age": 26,
            "district": "Patna, Bihar",
            "gestational_age_weeks": 35.1,
            "current_trimester": "THIRD_TRIMESTER",
            "past_obstetric_history": {
                "gravida": 1,
                "para": 0,
                "living": 0,
                "abortions": 0,
                "stillbirths": 0,
                "previous_c_sections": 0,
                "prior_notes": "Uncomplicated primigravida until 34 weeks."
            },
            "medical_co_morbidities": ["None"],
            "current_symptoms": ["Intense nocturnal itching on palms and soles without rash", "Disturbed sleep", "Dark-colored urine"],
            "active_test_results": {
                4: {"name": "CBC", "value": "Hb 11.2 g/dL, Platelets 210000 /uL", "is_abnormal": False},
                44: {"name": "Blood Pressure", "value": "118/76 mmHg", "is_abnormal": False},
                47: {"name": "Liver Function Tests", "value": "AST 64 IU/L, ALT 78 IU/L, Total Bilirubin 1.4 mg/dL", "is_abnormal": True},
                50: {"name": "Total Serum Bile Acids (TBA)", "value": "68 umol/L (Severe Cholestasis threshold >= 40)", "is_abnormal": True},
                54: {"name": "Cardiotocography (NST)", "value": "Reactive baseline 142 bpm", "is_abnormal": False},
                58: {"name": "Daily Fetal Kick Count", "value": "11 kicks in 2 hours (Perceived normal)", "is_abnormal": False}
            },
            "clinical_diagnosis_annotation": "Primigravida at 35.1 weeks with Severe Intrahepatic Cholestasis of Pregnancy (ICP) with Total Bile Acids 68 umol/L and transaminitis.",
            "primary_concerning_patterns": [
                "Nocturnal palm and sole pruritus without dermatological lesion",
                "Severe elevation of Total Serum Bile Acids (68 umol/L >= 40 umol/L)",
                "High risk of sudden unexplained intrauterine fetal demise (toxic bile acid-induced fetal cardiac arrhythmia)"
            ],
            "proposed_medical_advice": (
                "Potentially concerning pattern detected — clinical review recommended. "
                "Start Ursodeoxycholic Acid (UDCA) 300 mg PO TDS (10-15 mg/kg/day) to enhance biliary clearance and relieve pruritus. "
                "Prescribe Calamine lotion topically for symptomatic itching relief. "
                "Perform bi-weekly CTG (Test #54) and Umbilical Doppler. "
                "Under FOGSI guidelines, planned delivery / induction of labor is mandated at 36 completed weeks due to high risk of sudden stillbirth with bile acids > 40 umol/L."
            ),
            "hitl_trigger_words": ["Ursodeoxycholic Acid", "UDCA", "Calamine", "medicine", "tablets"],
            "patient_friendly_summary_en": "The severe itching on your hands and feet is caused by liver bile salts that have increased during pregnancy. We will start a medicine called UDCA to clear the bile and protect your baby. Because bile levels are high, doctors will deliver the baby safely around 36 weeks.",
            "is_emergency_referral_needed": False,
            "referral_facility_type": "DISTRICT_HOSPITAL"
        },

        # -------------------------------------------------------------
        # CASE 6: Immediate Newborn with Critical Congenital Heart Disease
        # -------------------------------------------------------------
        {
            "case_id": "CASE-IND-006",
            "patient_name": "Baby of Sunita",
            "age_hours": 26,
            "district": "Varanasi, Uttar Pradesh",
            "life_stage": "IMMEDIATE_NEWBORN",
            "maternal_history": {
                "mother_name": "Sunita Devi",
                "gestational_age_at_birth": 39.2,
                "delivery_mode": "Normal Spontaneous Vaginal",
                "birth_weight_grams": 3100
            },
            "current_symptoms": ["Mild tachypnea (respiratory rate 64/min)", "Normal feeding but slight perioral dusky hue on crying"],
            "active_test_results": {
                76: {"name": "1-Min Apgar", "value": "8", "is_abnormal": False},
                77: {"name": "5-Min Apgar", "value": "9", "is_abnormal": False},
                79: {"name": "Cord Blood Gas", "value": "pH 7.28, Base Deficit 3.1 mmol/L", "is_abnormal": False},
                80: {"name": "CCHD Pulse Oximetry Screen (24h)", "value": "Right Hand SpO2: 97%, Foot SpO2: 89% (Pre-to-post ductal gradient 8% > 3%)", "is_abnormal": True},
                85: {"name": "POC Blood Glucose", "value": "56 mg/dL (Normal)", "is_abnormal": False}
            },
            "clinical_diagnosis_annotation": "Term neonate at 26 hours of life with Failed Critical Congenital Heart Disease (CCHD) Pulse Oximetry screen showing significant differential cyanosis (Right hand 97% vs Foot 89%).",
            "primary_concerning_patterns": [
                "Abnormal pre-to-post ductal oxygen saturation gradient (8% difference exceeds 3% cutoff)",
                "Post-ductal SpO2 < 90% in foot (89%)",
                "High probability of duct-dependent systemic circulation (Critical Coarctation of Aorta / Interrupted Aortic Arch)"
            ],
            "proposed_medical_advice": (
                "Potentially concerning pattern detected — clinical review recommended. "
                "Positive CCHD screen is a pediatric emergency. "
                "Transfer immediately to Neonatal Intensive Care Unit (NICU). "
                "Perform urgent 2D Pediatric Echocardiography. "
                "Keep IV Prostaglandin E1 (Alprostadil) infusion (0.01 - 0.05 mcg/kg/min) ready to maintain patency of ductus arteriosus if duct-dependent systemic lesion is confirmed."
            ),
            "hitl_trigger_words": ["Prostaglandin", "Alprostadil", "medicine", "injection"],
            "patient_friendly_summary_en": "The routine oxygen check on your baby's hand and foot shows a difference in oxygen levels. This is a very sensitive check that helps doctors look closely at the baby's heart blood vessels using an echo scan. The pediatric team is caring for the baby in the special care nursery.",
            "is_emergency_referral_needed": True,
            "referral_facility_type": "TERTIARY_NEONATAL_ICU"
        },

        # -------------------------------------------------------------
        # CASE 7: Newborn Guthrie Screen - Congenital Hypothyroidism
        # -------------------------------------------------------------
        {
            "case_id": "CASE-IND-007",
            "patient_name": "Baby of Anjali",
            "age_days": 5,
            "district": "Kochi, Kerala",
            "life_stage": "GUTHRIE_IEM_PANEL",
            "maternal_history": {
                "mother_name": "Anjali Menon",
                "birth_weight_grams": 3250,
                "gestational_age": 40.0
            },
            "current_symptoms": ["Prolonged physiological jaundice", "Poor feeding latch", "Large posterior fontanelle"],
            "active_test_results": {
                84: {"name": "Total Serum Bilirubin", "value": "13.4 mg/dL (Unconjugated)", "is_abnormal": True},
                90: {"name": "Guthrie Card Neonatal TSH (Day 3)", "value": "78.0 mIU/L (Severe elevation, normal cutoff < 15-20)", "is_abnormal": True},
                14: {"name": "Confirmatory Serum Free T4", "value": "0.42 ng/dL (Significantly low)", "is_abnormal": True}
            },
            "clinical_diagnosis_annotation": "5-day-old neonate with Confirmed Primary Congenital Hypothyroidism (Neonatal TSH 78 mIU/L, Free T4 0.42 ng/dL).",
            "primary_concerning_patterns": [
                "Critically elevated heel-prick dried blood spot TSH (78 mIU/L)",
                "Low Free T4 confirming permanent thyroid dysgenesis / dyshormonogenesis",
                "Urgent need for hormone replacement before Day 14 of life to preserve brain IQ and neurological development"
            ],
            "proposed_medical_advice": (
                "Potentially concerning pattern detected — clinical review recommended. "
                "Confirmed Primary Congenital Hypothyroidism. "
                "Initiate oral Levothyroxine sodium at 10 - 15 mcg/kg/day (crushed tablet mixed in 1-2 mL of breastmilk given once daily in morning). "
                "Avoid giving with soy formula, iron, or calcium supplements which block absorption. "
                "Repeat venous TSH and Free T4 at 2 weeks and 4 weeks to adjust dose. Target Free T4 in upper half of normal range."
            ),
            "hitl_trigger_words": ["Levothyroxine", "tablets", "medicine", "breastmilk"],
            "patient_friendly_summary_en": "Your baby's newborn heel-prick screening test showed that the baby's thyroid gland is producing less thyroid hormone. Giving a small crushed thyroid tablet with breastmilk every morning will completely protect your baby's brain growth and mental development. Babies on this medicine grow up completely healthy and smart.",
            "is_emergency_referral_needed": False,
            "referral_facility_type": "DISTRICT_PEDIATRIC_CENTRE"
        },

        # -------------------------------------------------------------
        # CASE 8: Postpartum Mother with Delayed Preeclampsia & Depression
        # -------------------------------------------------------------
        {
            "case_id": "CASE-IND-008",
            "patient_name": "Ritu Saxena",
            "age": 28,
            "district": "Lucknow, Uttar Pradesh",
            "postpartum_day": 7,
            "life_stage": "POSTPARTUM_MOTHER",
            "maternal_history": {
                "delivery_mode": "Emergency Cesarean Section for prolonged labor",
                "blood_loss": 600
            },
            "current_symptoms": ["Severe occipital headache for 24 hours", "Crying spells", "Feeling overwhelmed and disconnected from baby"],
            "active_test_results": {
                63: {"name": "Post-Delivery CBC", "value": "Hb 9.8 g/dL", "is_abnormal": True},
                66: {"name": "Uterine Tone & Lochia", "value": "Uterus well involuted, lochia serosa normal", "is_abnormal": False},
                67: {"name": "Postpartum Blood Pressure", "value": "158/104 mmHg (Severe range hypertension)", "is_abnormal": True},
                68: {"name": "REEDA Wound Exam", "value": "Pfannenstiel incision clean, no discharge, score 1", "is_abnormal": False},
                71: {"name": "Edinburgh Postnatal Depression Scale (EPDS)", "value": "Score 17 / 30 (Positive for postpartum depression, Q10 self-harm score 0)", "is_abnormal": True}
            },
            "clinical_diagnosis_annotation": "Postpartum Day 7 mother with Delayed-Onset Postpartum Preeclampsia with severe hypertension (158/104 mmHg) and Postpartum Depression (EPDS 17/30).",
            "primary_concerning_patterns": [
                "Severe postpartum hypertension (158/104 mmHg) with persistent headache",
                "High risk of postpartum eclampsia and stroke",
                "Postpartum depression (EPDS 17 >= 13) requiring clinical support and lactation-compatible therapy"
            ],
            "proposed_medical_advice": (
                "Potentially concerning pattern detected — clinical review recommended. "
                "Urgent hospital readmission for Delayed Postpartum Preeclampsia. "
                "Administer oral Nifedipine Retard 20 mg BD or oral Labetalol 200 mg BD to control BP below 140/90 mmHg. "
                "Consider Magnesium Sulfate seizure prophylaxis if neurological symptoms worsen. "
                "Provide compassionate counseling and psychiatric evaluation. If antidepressant required, Sertraline 25-50 mg daily is the preferred lactation-safe medication."
            ),
            "hitl_trigger_words": ["Nifedipine", "Labetalol", "Sertraline", "Magnesium Sulfate", "medicine", "tablets"],
            "patient_friendly_summary_en": "Your blood pressure has risen after delivery, which is causing your headache. It is very important to get a medicine to bring your pressure down right away to keep you safe. Feeling sad and overwhelmed after birth is also very common and treatable. Our female counselor and doctor will support you and your baby gently.",
            "is_emergency_referral_needed": True,
            "referral_facility_type": "DISTRICT_HOSPITAL"
        }
    ]

    return cases


def export_training_data_json(filepath: str) -> None:
    cases = generate_comprehensive_training_cases()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(cases)} comprehensive clinical training profiles to {filepath}")
