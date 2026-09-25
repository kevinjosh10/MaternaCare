"""
MaternaCare Master Diagnostic Catalog (122 Parameters)
Unified Diagnostic & Clinical Parameter Dictionary for Indian Maternal & Neonatal Health.
Covers Conception to 1 Year Postpartum, incorporating FOGSI, DIPSI, MoHFW, WHO, and ACOG standards.
"""

from typing import Dict, Any, List, Optional
from enum import Enum


class LifeStage(str, Enum):
    FIRST_TRIMESTER = "FIRST_TRIMESTER"       # Weeks 1 - 13
    SECOND_TRIMESTER = "SECOND_TRIMESTER"     # Weeks 14 - 27
    THIRD_TRIMESTER = "THIRD_TRIMESTER"       # Weeks 28 - 40+
    LABOR_AND_DELIVERY = "LABOR_AND_DELIVERY" # Intrapartum
    POSTPARTUM_MOTHER = "POSTPARTUM_MOTHER"   # Day 1 - 1 Year
    IMMEDIATE_NEWBORN = "IMMEDIATE_NEWBORN"   # 0 - 72 Hours
    GUTHRIE_IEM_PANEL = "GUTHRIE_IEM_PANEL"   # 24 - 48 Hours
    EARLY_INFANCY = "EARLY_INFANCY"           # Weeks 1 - 4
    INFANCY_MONTHS_2_12 = "INFANCY_MONTHS_2_12" # Months 2 - 12


class SpecimenType(str, Enum):
    WHOLE_BLOOD = "WHOLE_BLOOD"
    SERUM = "SERUM"
    PLASMA = "PLASMA"
    URINE = "URINE"
    ULTRASOUND = "ULTRASOUND"
    DOPPLER = "DOPPLER"
    DRIED_BLOOD_SPOT = "DRIED_BLOOD_SPOT"
    SWAB = "SWAB"
    PHYSICAL_ASSESSMENT = "PHYSICAL_ASSESSMENT"
    CARDIOTOCOGRAPHY = "CARDIOTOCOGRAPHY"
    SURVEY_SCORE = "SURVEY_SCORE"


# Complete Master Catalog of 122 Tests with Indian Guidelines (FOGSI / DIPSI / MoHFW / WHO)
MASTER_TESTS_CATALOG: Dict[int, Dict[str, Any]] = {
    # -------------------------------------------------------------
    # 1.1 FIRST TRIMESTER TESTS (Weeks 1 – 13)
    # -------------------------------------------------------------
    1: {
        "id": 1,
        "name": "Urine Pregnancy Test (hCG)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 1 – 4",
        "specimen": SpecimenType.URINE,
        "unit": "Qualitative",
        "normal_range": "Positive",
        "indian_clinical_protocol": "MoHFW RCH: Home or Sub-centre Nishchay kit qualitative test on first missed period.",
        "danger_threshold": "Negative with persistent amenorrhea / ectopic suspicion"
    },
    2: {
        "id": 2,
        "name": "Quantitative Serum Beta-hCG",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 1 – 6",
        "specimen": SpecimenType.SERUM,
        "unit": "mIU/mL",
        "normal_range": "Doubling every 48-72h in viable intrauterine pregnancy",
        "indian_clinical_protocol": "FOGSI Ectopic Guideline: Discriminatory zone 1500-2000 mIU/mL. Subnormal doubling (<66% in 48h) warns of ectopic pregnancy or early blighted ovum.",
        "danger_threshold": "< 66% rise in 48h or plateau"
    },
    3: {
        "id": 3,
        "name": "Dating & Viability Ultrasound (TVS)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 6 – 8",
        "specimen": SpecimenType.ULTRASOUND,
        "unit": "mm / bpm",
        "normal_range": "CRL concordant, FHR 110-160 bpm",
        "indian_clinical_protocol": "FOGSI Imaging Guideline: Earliest accurate EDD determination. Fetal cardiac pole must be visible if CRL >= 7 mm.",
        "danger_threshold": "CRL >= 7mm with absent heartbeat (missed miscarriage), adnexal mass with empty uterus"
    },
    4: {
        "id": 4,
        "name": "Complete Blood Count (CBC)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "g/dL, /uL",
        "normal_range": "Hb >= 11.0 g/dL, Platelets 150000-450000 /uL",
        "indian_clinical_protocol": "Anaemia Mukt Bharat: Moderate anemia Hb 8.0-9.9, Severe anemia Hb 5.0-7.9, Very severe < 5.0 g/dL. Platelets < 100000 mandates workup.",
        "danger_threshold": "Hb < 7.0 g/dL or Platelets < 50000 /uL"
    },
    5: {
        "id": 5,
        "name": "Blood Grouping (ABO) & Rh(D) Factor",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "Blood Group",
        "normal_range": "Rh Positive or Negative",
        "indian_clinical_protocol": "MoHFW ANC: Universal grouping. Rh-negative mothers flagged for ICT and anti-D prophylaxis at 28w and within 72h post-delivery.",
        "danger_threshold": "Rh Negative without prior documentation or sensitization"
    },
    6: {
        "id": 6,
        "name": "Indirect Coombs Test (ICT / Antibody Screen)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.SERUM,
        "unit": "Titer",
        "normal_range": "Negative",
        "indian_clinical_protocol": "FOGSI Rh Isoimmunization: Titer >= 1:16 is critical; mandates serial MCA Doppler PSV surveillance for fetal anemia.",
        "danger_threshold": "Positive Titer >= 1:16"
    },
    7: {
        "id": 7,
        "name": "HIV 1 & 2 ELISA / CLIA Screen",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.SERUM,
        "unit": "Reactive / Non-Reactive",
        "normal_range": "Non-Reactive",
        "indian_clinical_protocol": "NACO PPTCT: Universal opt-out testing. If reactive, immediate Triple Antiretroviral Therapy (TLD) initiation.",
        "danger_threshold": "Reactive"
    },
    8: {
        "id": 8,
        "name": "Hepatitis B Surface Antigen (HBsAg)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.SERUM,
        "unit": "Reactive / Non-Reactive",
        "normal_range": "Non-Reactive",
        "indian_clinical_protocol": "NVHCP MoHFW: If positive, baby requires Hepatitis B Immunoglobulin (HBIG) + Hep-B vaccine within 12h of birth. Check maternal viral load for Tenofovir.",
        "danger_threshold": "Reactive / Positive"
    },
    9: {
        "id": 9,
        "name": "Hepatitis C Antibody (Anti-HCV)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.SERUM,
        "unit": "Reactive / Non-Reactive",
        "normal_range": "Non-Reactive",
        "indian_clinical_protocol": "NVHCP MoHFW: Screen for active hepatitis C viremia via HCV-RNA PCR if antibody positive.",
        "danger_threshold": "Reactive"
    },
    10: {
        "id": 10,
        "name": "Syphilis Serology (VDRL / RPR / TPHA)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.SERUM,
        "unit": "Reactive / Non-Reactive",
        "normal_range": "Non-Reactive",
        "indian_clinical_protocol": "MoHFW National Syphilis Control: Immediate Benzathine Penicillin 2.4 million units IM single dose to prevent congenital syphilis, hydrops, stillbirth.",
        "danger_threshold": "Reactive with titer >= 1:8"
    },
    11: {
        "id": 11,
        "name": "Rubella IgG Antibody Titer",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.SERUM,
        "unit": "IU/mL",
        "normal_range": ">= 10.0 IU/mL (Immune)",
        "indian_clinical_protocol": "FOGSI TORCH: If < 10 IU/mL (non-immune), educate on avoiding rashes; administer postpartum MMR vaccine (live attenuated contraindicated during pregnancy).",
        "danger_threshold": "< 10.0 IU/mL (Non-immune) or Rubella IgM Positive"
    },
    12: {
        "id": 12,
        "name": "Varicella Zoster IgG",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.SERUM,
        "unit": "Positive / Negative",
        "normal_range": "Positive (Immune)",
        "indian_clinical_protocol": "If negative and exposed to chickenpox, Varicella Zoster Immunoglobulin (VZIG) within 96 hours.",
        "danger_threshold": "Negative (Susceptible to Congenital Varicella Syndrome)"
    },
    13: {
        "id": 13,
        "name": "Thyroid Stimulating Hormone (TSH)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.SERUM,
        "unit": "mIU/L",
        "normal_range": "0.1 - 2.5 mIU/L (T1 Indian target)",
        "indian_clinical_protocol": "Indian Thyroid Society & FOGSI: First trimester cutoff is 2.5 mIU/L. TSH > 2.5 with positive anti-TPO mandates Levothyroxine initiation to prevent fetal neurocognitive deficits.",
        "danger_threshold": "TSH > 4.5 mIU/L or TSH < 0.05 mIU/L"
    },
    14: {
        "id": 14,
        "name": "Free Thyroxine (Free T4)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.SERUM,
        "unit": "ng/dL",
        "normal_range": "0.8 - 1.8 ng/dL",
        "indian_clinical_protocol": "Evaluates overt vs subclinical hypothyroidism when TSH is elevated.",
        "danger_threshold": "< 0.7 ng/dL"
    },
    15: {
        "id": 15,
        "name": "Fasting Blood Sugar (FBS)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.PLASMA,
        "unit": "mg/dL",
        "normal_range": "< 92 mg/dL",
        "indian_clinical_protocol": "DIPSI / FOGSI: FBS >= 92 mg/dL indicates early GDM. FBS >= 126 mg/dL confirms overt pre-existing diabetes.",
        "danger_threshold": ">= 92 mg/dL"
    },
    16: {
        "id": 16,
        "name": "Glycated Hemoglobin (HbA1c)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "%",
        "normal_range": "< 5.7%",
        "indian_clinical_protocol": "HbA1c >= 6.5% indicates pre-existing overt diabetes with high teratogenic cardiac anomaly risk.",
        "danger_threshold": ">= 6.5%"
    },
    17: {
        "id": 17,
        "name": "Urine Routine & Microscopic Exam (R/M)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.URINE,
        "unit": "Dipstick / Microscopy",
        "normal_range": "Protein: Nil, Sugar: Nil, Pus cells < 5/HPF",
        "indian_clinical_protocol": "MoHFW ANC: Essential early screen for pre-existing nephropathy, glucosuria, and pyuria.",
        "danger_threshold": "Protein >= 1+ or Pus cells > 10/HPF"
    },
    18: {
        "id": 18,
        "name": "Urine Culture & Sensitivity (ASB Screen)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.URINE,
        "unit": "CFU/mL",
        "normal_range": "< 10^4 CFU/mL or No growth",
        "indian_clinical_protocol": "WHO & FOGSI: Asymptomatic Bacteriuria (ASB) >= 10^5 CFU/mL must be treated with culture-directed safe antibiotics (Amoxicillin/Nitrofurantoin) to prevent pyelonephritis and preterm delivery.",
        "danger_threshold": ">= 10^5 CFU/mL of a single uropathogen"
    },
    19: {
        "id": 19,
        "name": "Hemoglobin HPLC / Hb Electrophoresis",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 8 – 10",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "%",
        "normal_range": "HbA2 <= 3.5%, HbF < 1.0%, No variant Hb",
        "indian_clinical_protocol": "National Thalassemia Control: Essential in Indian populations (Punjab, Gujarat, Bengal, Sindhi, tribal belts). HbA2 > 3.5% confirms Beta-Thalassemia Carrier; mandates partner screening to prevent Thalassemia Major.",
        "danger_threshold": "HbA2 > 3.5% or presence of HbS / HbE"
    },
    20: {
        "id": 20,
        "name": "Cell-Free DNA (cfDNA / NIPT)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 10 – 13+",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "Risk Ratio",
        "normal_range": "Low Risk (< 1:10000) for Trisomy 21, 18, 13",
        "indian_clinical_protocol": "High sensitivity (>99% for Down syndrome). Fetal fraction must be >= 4%.",
        "danger_threshold": "High Risk (> 1:100) or Fetal Fraction < 4%"
    },
    21: {
        "id": 21,
        "name": "Nuchal Translucency (NT) Scan",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 11 – 13+6",
        "specimen": SpecimenType.ULTRASOUND,
        "unit": "mm",
        "normal_range": "NT < 2.5 mm, Nasal Bone Present",
        "indian_clinical_protocol": "Fetal Medicine Foundation (FMF) certified scan. NT >= 3.0 mm or absent nasal bone strongly indicates chromosomal aneuploidy or congenital heart disease.",
        "danger_threshold": "NT >= 3.0 mm or Absent Nasal Bone"
    },
    22: {
        "id": 22,
        "name": "Serum PAPP-A",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 11 – 13+6",
        "specimen": SpecimenType.SERUM,
        "unit": "MoM (Multiples of Median)",
        "normal_range": "0.5 - 2.0 MoM",
        "indian_clinical_protocol": "Low PAPP-A (< 0.4 MoM) indicates Down syndrome, severe early placental insufficiency, and FGR risk.",
        "danger_threshold": "< 0.4 MoM"
    },
    23: {
        "id": 23,
        "name": "Serum Free Beta-hCG (First Trimester)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 11 – 13+6",
        "specimen": SpecimenType.SERUM,
        "unit": "MoM",
        "normal_range": "0.5 - 2.0 MoM",
        "indian_clinical_protocol": "Elevated Free Beta-hCG (> 2.0 MoM) combined with low PAPP-A elevates Down syndrome index.",
        "danger_threshold": "> 2.5 MoM or < 0.3 MoM"
    },
    24: {
        "id": 24,
        "name": "Uterine Artery Doppler (T1 Preeclampsia Screen)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 11 – 13+6",
        "specimen": SpecimenType.DOPPLER,
        "unit": "Mean Pulsatility Index (PI)",
        "normal_range": "Mean UtA-PI < 95th percentile (~1.4-1.6)",
        "indian_clinical_protocol": "FOGSI Preeclampsia Prevention: High Mean UtA-PI > 95th percentile mandates early Aspirin 150mg at bedtime before 16 weeks.",
        "danger_threshold": "Mean UtA-PI > 95th percentile or bilateral early diastolic notching"
    },
    25: {
        "id": 25,
        "name": "Serum Placental Growth Factor (PlGF)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 11 – 13+6",
        "specimen": SpecimenType.SERUM,
        "unit": "pg/mL / MoM",
        "normal_range": "> 0.5 MoM",
        "indian_clinical_protocol": "Low PlGF reflects impaired trophoblastic invasion; key input in FMF preeclampsia risk algorithm.",
        "danger_threshold": "< 0.4 MoM"
    },
    26: {
        "id": 26,
        "name": "Chorionic Villus Sampling (CVS)",
        "stage": LifeStage.FIRST_TRIMESTER,
        "timing": "Weeks 10 – 13+6",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Karyotype / Microarray",
        "normal_range": "46,XX or 46,XY Euploid",
        "indian_clinical_protocol": "Invasive diagnostic test indicated for high-risk combined screen, parental balanced translocation, or single gene disorders.",
        "danger_threshold": "Aneuploidy / Pathogenic Copy Number Variant"
    },

    # -------------------------------------------------------------
    # 1.2 SECOND TRIMESTER TESTS (Weeks 14 – 27)
    # -------------------------------------------------------------
    27: {
        "id": 27,
        "name": "Maternal Serum Alpha-Fetoprotein (MSAFP)",
        "stage": LifeStage.SECOND_TRIMESTER,
        "timing": "Weeks 15 – 20",
        "specimen": SpecimenType.SERUM,
        "unit": "MoM",
        "normal_range": "0.5 - 2.0 MoM",
        "indian_clinical_protocol": "MSAFP > 2.5 MoM flags Open Neural Tube Defects (Anencephaly, Spina Bifida) or omphalocele.",
        "danger_threshold": "> 2.5 MoM"
    },
    28: {
        "id": 28,
        "name": "Second Trimester Total hCG",
        "stage": LifeStage.SECOND_TRIMESTER,
        "timing": "Weeks 15 – 20",
        "specimen": SpecimenType.SERUM,
        "unit": "MoM",
        "normal_range": "0.5 - 2.0 MoM",
        "indian_clinical_protocol": "Part of Quadruple screen (elevated in Trisomy 21).",
        "danger_threshold": "> 2.5 MoM"
    },
    29: {
        "id": 29,
        "name": "Unconjugated Estriol (uE3)",
        "stage": LifeStage.SECOND_TRIMESTER,
        "timing": "Weeks 15 – 20",
        "specimen": SpecimenType.SERUM,
        "unit": "MoM",
        "normal_range": "> 0.5 MoM",
        "indian_clinical_protocol": "Very low uE3 (< 0.2 MoM) alerts to steroid sulfatase deficiency (X-linked ichthyosis) or Smith-Lemli-Opitz syndrome.",
        "danger_threshold": "< 0.3 MoM"
    },
    30: {
        "id": 30,
        "name": "Dimeric Inhibin-A (DIA)",
        "stage": LifeStage.SECOND_TRIMESTER,
        "timing": "Weeks 15 – 20",
        "specimen": SpecimenType.SERUM,
        "unit": "MoM",
        "normal_range": "0.5 - 2.0 MoM",
        "indian_clinical_protocol": "Elevated in Down syndrome and subsequent preeclampsia.",
        "danger_threshold": "> 2.0 MoM"
    },
    31: {
        "id": 31,
        "name": "Diagnostic Amniocentesis",
        "stage": LifeStage.SECOND_TRIMESTER,
        "timing": "Weeks 15 – 22",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Cytogenetic / Molecular",
        "normal_range": "Normal Euploid",
        "indian_clinical_protocol": "Definitive prenatal diagnosis for abnormal TIFFA scan or high-risk Quadruple screen. Miscarriage risk ~0.1-0.2%.",
        "danger_threshold": "Aneuploidy, Monogenic defect, or CMV PCR positive"
    },
    32: {
        "id": 32,
        "name": "Level-II Target / TIFFA Anatomy Scan",
        "stage": LifeStage.SECOND_TRIMESTER,
        "timing": "Weeks 18 – 22",
        "specimen": SpecimenType.ULTRASOUND,
        "unit": "Morphology Score",
        "normal_range": "Normal intracranial ventricles (<10mm), 4-chamber heart, intact spine, kidneys, lips",
        "indian_clinical_protocol": "Mandatory under Indian MTP Act (before 24 weeks legal ceiling). Examines 28 structural anatomical checkpoints.",
        "danger_threshold": "Major structural anomaly, severe ventriculomegaly (>=15mm), CDH, or bilateral renal agenesis"
    },
    33: {
        "id": 33,
        "name": "Transvaginal Cervical Length Measurement",
        "stage": LifeStage.SECOND_TRIMESTER,
        "timing": "Weeks 18 – 22",
        "specimen": SpecimenType.ULTRASOUND,
        "unit": "mm",
        "normal_range": "> 25 mm",
        "indian_clinical_protocol": "Cervical length <= 25 mm indicates high risk of spontaneous preterm birth. Mandates vaginal micronized progesterone 200mg daily or cervical cerclage.",
        "danger_threshold": "<= 20 mm or Funneling > 50%"
    },
    34: {
        "id": 34,
        "name": "Fetal Echocardiography",
        "stage": LifeStage.SECOND_TRIMESTER,
        "timing": "Weeks 20 – 24",
        "specimen": SpecimenType.ULTRASOUND,
        "unit": "Hemodynamic evaluation",
        "normal_range": "Normal concordant cardiac anatomy, normal outflow tracts",
        "indian_clinical_protocol": "Indicated in IVF, pre-gestational diabetes, maternal anti-Ro/SSA antibodies, or suspected cardiac defect on TIFFA.",
        "danger_threshold": "Congenital heart defect (HLHS, Coarctation, AVSD, Complete Heart Block)"
    },
    35: {
        "id": 35,
        "name": "75g 2-Hour Oral Glucose Tolerance Test (OGTT)",
        "stage": LifeStage.SECOND_TRIMESTER,
        "timing": "Weeks 24 – 28",
        "specimen": SpecimenType.PLASMA,
        "unit": "mg/dL",
        "normal_range": "Fasting < 92, 1-hr < 180, 2-hr < 153 mg/dL (or DIPSI non-fasting 2hr < 140 mg/dL)",
        "indian_clinical_protocol": "DIPSI / FOGSI National Guideline: In high-prevalence Indian mothers, universal 75g OGTT at 24-28w. If 2-hr glucose >= 140 mg/dL, GDM diagnosed. Medical Nutrition Therapy (MNT) initiated; Insulin / Metformin if targets exceeded.",
        "danger_threshold": "2-hr plasma glucose >= 140 mg/dL"
    },
    36: {
        "id": 36,
        "name": "Repeat Complete Blood Count (CBC - T2)",
        "stage": LifeStage.SECOND_TRIMESTER,
        "timing": "Weeks 24 – 28",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "g/dL",
        "normal_range": "Hb >= 10.5 g/dL",
        "indian_clinical_protocol": "Checks physiological hemodilution nadir. Severe anemia requires IV Iron Sucrose or Ferric Carboxymaltose (FCM).",
        "danger_threshold": "Hb < 8.0 g/dL"
    },
    37: {
        "id": 37,
        "name": "Repeat Indirect Coombs Test (ICT - T2)",
        "stage": LifeStage.SECOND_TRIMESTER,
        "timing": "Weeks 24 – 28",
        "specimen": SpecimenType.SERUM,
        "unit": "Titer",
        "normal_range": "Negative",
        "indian_clinical_protocol": "Administer 300 mcg Anti-D Immunoglobulin at 28 weeks if ICT remains negative in Rh-negative mothers.",
        "danger_threshold": "Seroconversion to Positive"
    },

    # -------------------------------------------------------------
    # 1.3 THIRD TRIMESTER TESTS (Weeks 28 – 40+)
    # -------------------------------------------------------------
    38: {
        "id": 38,
        "name": "Third Trimester Growth Ultrasound",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 28 – 32",
        "specimen": SpecimenType.ULTRASOUND,
        "unit": "Percentile / grams",
        "normal_range": "Hadlock EFW 10th - 90th percentile (Appropriate for Gestational Age - AGA)",
        "indian_clinical_protocol": "FOGSI FGR Guideline: EFW < 10th percentile defines SGA. EFW < 3rd percentile or Abdominal Circumference (AC) < 10th percentile with abnormal Doppler defines Fetal Growth Restriction (FGR).",
        "danger_threshold": "EFW < 3rd percentile or AC < 5th percentile"
    },
    39: {
        "id": 39,
        "name": "Amniotic Fluid Index (AFI) / SDP",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 28 – 40",
        "specimen": SpecimenType.ULTRASOUND,
        "unit": "cm",
        "normal_range": "AFI 8.0 - 24.0 cm, Single Deepest Pocket (SDP) 2.0 - 8.0 cm",
        "indian_clinical_protocol": "AFI < 5.0 cm or SDP < 2.0 cm indicates severe Oligohydramnios (placental insufficiency or PROM). AFI > 25.0 cm indicates Polyhydramnios (GDM or fetal anomaly).",
        "danger_threshold": "AFI < 5.0 cm or SDP < 2.0 cm (Oligohydramnios)"
    },
    40: {
        "id": 40,
        "name": "Umbilical Artery (UA) Doppler",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 28 – 40",
        "specimen": SpecimenType.DOPPLER,
        "unit": "Pulsatility Index (PI) & Waveform",
        "normal_range": "Forward end-diastolic flow, PI < 95th percentile",
        "indian_clinical_protocol": "Absent End-Diastolic Velocity (AEDV) indicates severe placental resistance; plan delivery by 34w. Reversed End-Diastolic Velocity (REDV) indicates impending fetal demise; emergency C-section by 30-32w after steroids.",
        "danger_threshold": "AEDV or REDV"
    },
    41: {
        "id": 41,
        "name": "Middle Cerebral Artery (MCA) Doppler",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 28 – 40",
        "specimen": SpecimenType.DOPPLER,
        "unit": "MoM / PI",
        "normal_range": "Peak Systolic Velocity (PSV) < 1.5 MoM; PI normal",
        "indian_clinical_protocol": "MCA-PSV > 1.5 MoM diagnoses moderate-to-severe fetal anemia (Rh isoimmunization or Parvovirus B19). MCA-PI < 5th percentile reveals brain-sparing redistribution in chronic hypoxia.",
        "danger_threshold": "PSV > 1.5 MoM or brain sparing MCA vasodilation"
    },
    42: {
        "id": 42,
        "name": "Ductus Venosus (DV) Doppler",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 28 – 40",
        "specimen": SpecimenType.DOPPLER,
        "unit": "A-wave direction",
        "normal_range": "Positive forward A-wave",
        "indian_clinical_protocol": "Absent or reversed A-wave in DV indicates fetal cardiac decompensation and acidemia; immediate delivery mandated regardless of gestational age.",
        "danger_threshold": "Reversed or Absent A-wave"
    },
    43: {
        "id": 43,
        "name": "Cerebroplacental Ratio (CPR)",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 28 – 40",
        "specimen": SpecimenType.DOPPLER,
        "unit": "Ratio (MCA-PI / UA-PI)",
        "normal_range": "CPR >= 1.08",
        "indian_clinical_protocol": "CPR < 1.0 indicates early placental insufficiency even when individual Dopplers appear borderline.",
        "danger_threshold": "< 1.0"
    },
    44: {
        "id": 44,
        "name": "Serial Antenatal Blood Pressure Monitoring",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Every Visit",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "mmHg",
        "normal_range": "Systolic < 120, Diastolic < 80 mmHg",
        "indian_clinical_protocol": "FOGSI Gestational Hypertension: BP >= 140/90 on two readings 4h apart defines Gestational Hypertension. BP >= 160/110 mmHg defines Severe Preeclampsia; requires urgent IV Labetalol / oral Nifedipine and Magnesium Sulfate loading to prevent eclamptic seizures.",
        "danger_threshold": ">= 140/90 (Mild) or >= 160/110 mmHg (Severe Preeclampsia Emergency)"
    },
    45: {
        "id": 45,
        "name": "Urine Protein Dipstick / Spot UPCR",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Every Visit",
        "specimen": SpecimenType.URINE,
        "unit": "mg/mg or Dipstick",
        "normal_range": "Dipstick Nil / Trace; Spot UPCR < 0.3 mg/mg",
        "indian_clinical_protocol": "Spot UPCR >= 0.3 mg/mg (or 24h urine protein >= 300 mg) confirms Preeclampsia when associated with hypertension.",
        "danger_threshold": "UPCR >= 0.3 mg/mg or Dipstick >= 2+"
    },
    46: {
        "id": 46,
        "name": "Serum sFlt-1 / PlGF Biomarker Ratio",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 28 – 37",
        "specimen": SpecimenType.SERUM,
        "unit": "Ratio",
        "normal_range": "<= 38 (Rules out preeclampsia for 1-4 weeks)",
        "indian_clinical_protocol": "Ratio > 85 (or > 110 in late pregnancy) predicts imminent preeclampsia onset, HELLP, and adverse maternal-fetal outcome.",
        "danger_threshold": "> 85"
    },
    47: {
        "id": 47,
        "name": "Liver Function Tests (AST / ALT / Bilirubin)",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Third Trimester",
        "specimen": SpecimenType.SERUM,
        "unit": "IU/L",
        "normal_range": "AST < 35, ALT < 35 IU/L, Total Bilirubin < 1.0 mg/dL",
        "indian_clinical_protocol": "AST / ALT >= 70 IU/L (double upper limit) with epigastric pain diagnostic of HELLP Syndrome. Emergent delivery indicated.",
        "danger_threshold": "AST or ALT >= 70 IU/L"
    },
    48: {
        "id": 48,
        "name": "Renal Function Tests (Creatinine / Uric Acid)",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Third Trimester",
        "specimen": SpecimenType.SERUM,
        "unit": "mg/dL",
        "normal_range": "Creatinine 0.4 - 0.8 mg/dL, Uric Acid < 5.5 mg/dL",
        "indian_clinical_protocol": "Serum Creatinine > 1.1 mg/dL indicates severe renal impairment in preeclampsia.",
        "danger_threshold": "Creatinine > 1.1 mg/dL"
    },
    49: {
        "id": 49,
        "name": "Serum Lactate Dehydrogenase (LDH)",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Third Trimester",
        "specimen": SpecimenType.SERUM,
        "unit": "IU/L",
        "normal_range": "100 - 300 IU/L",
        "indian_clinical_protocol": "LDH > 600 IU/L indicates microangiopathic intravascular hemolysis (Hemolysis component of HELLP syndrome).",
        "danger_threshold": "> 600 IU/L"
    },
    50: {
        "id": 50,
        "name": "Fasting Total Serum Bile Acids (TBA)",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Third Trimester",
        "specimen": SpecimenType.SERUM,
        "unit": "umol/L",
        "normal_range": "< 10 umol/L",
        "indian_clinical_protocol": "FOGSI Cholestasis Guideline: Nocturnal palm/sole pruritus without primary rash. TBA >= 10 confirms Intrahepatic Cholestasis of Pregnancy (ICP). TBA >= 40-100 umol/L is severe ICP with high stillbirth risk; delivery at 36-37 weeks.",
        "danger_threshold": ">= 40 umol/L"
    },
    51: {
        "id": 51,
        "name": "Group B Streptococcus (GBS) Swab",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 35 – 37",
        "specimen": SpecimenType.SWAB,
        "unit": "Culture",
        "normal_range": "Negative",
        "indian_clinical_protocol": "Positive GBS colonization mandates intrapartum IV Ampicillin 2g loading then 1g q4h to prevent early neonatal sepsis.",
        "danger_threshold": "Positive"
    },
    52: {
        "id": 52,
        "name": "Coagulation Profile (PT / INR / aPTT / Fibrinogen)",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 36 – 38",
        "specimen": SpecimenType.PLASMA,
        "unit": "Seconds / mg/dL",
        "normal_range": "INR 0.9 - 1.1, Fibrinogen 300 - 600 mg/dL",
        "indian_clinical_protocol": "Fibrinogen < 200 mg/dL in severe PPH or abruption warns of disseminated intravascular coagulation (DIC). Cryoprecipitate needed.",
        "danger_threshold": "Fibrinogen < 200 mg/dL or INR > 1.5"
    },
    53: {
        "id": 53,
        "name": "Fetal Presentation Ultrasound",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 36 – 38",
        "specimen": SpecimenType.ULTRASOUND,
        "unit": "Presentation / Lie",
        "normal_range": "Cephalic Longitudinal Lie",
        "indian_clinical_protocol": "Breech or transverse presentation evaluated for External Cephalic Version (ECV) or elective cesarean section.",
        "danger_threshold": "Transverse Lie or Footling Breech"
    },
    54: {
        "id": 54,
        "name": "Cardiotocography (CTG) / Non-Stress Test (NST)",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 36 – 40+",
        "specimen": SpecimenType.CARDIOTOCOGRAPHY,
        "unit": "Reactivity Pattern",
        "normal_range": "Reactive: Baseline 110-160 bpm, moderate variability (6-25 bpm), >= 2 accelerations of 15 bpm x 15 sec in 20 min",
        "indian_clinical_protocol": "FOGSI CTG Guideline: Non-reactive or persistent late decelerations require immediate clinical resuscitation and emergency delivery.",
        "danger_threshold": "Non-Reactive with late decelerations or minimal variability (<5 bpm)"
    },
    55: {
        "id": 55,
        "name": "Manning's Biophysical Profile (BPP)",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 36 – 40+",
        "specimen": SpecimenType.SURVEY_SCORE,
        "unit": "Score / 10",
        "normal_range": "8/10 or 10/10 (Normal)",
        "indian_clinical_protocol": "5 components: Fetal breathing, gross movement, fetal tone, amniotic fluid, and NST. Score <= 4/10 indicates chronic asphyxia; requires delivery.",
        "danger_threshold": "<= 4/10"
    },
    56: {
        "id": 56,
        "name": "Modified Biophysical Profile (mBPP)",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 36 – 40+",
        "specimen": SpecimenType.SURVEY_SCORE,
        "unit": "NST + SDP",
        "normal_range": "Reactive NST + Single Deepest Pocket >= 2.0 cm",
        "indian_clinical_protocol": "Practical weekly surveillance test in high-risk pregnancies.",
        "danger_threshold": "Non-Reactive or SDP < 2.0 cm"
    },
    57: {
        "id": 57,
        "name": "Cervical Bishop Score",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Weeks 38 – 41+",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Score / 13",
        "normal_range": "Score >= 8 (Favorable for induction)",
        "indian_clinical_protocol": "FOGSI Induction of Labor: Score < 6 indicates unfavorable cervix requiring Dinoprostone (PGE2) gel or Foley bulb cervical ripening.",
        "danger_threshold": "< 5 at 41 weeks"
    },
    58: {
        "id": 58,
        "name": "Daily Fetal Kick Count Assessment (DFKC)",
        "stage": LifeStage.THIRD_TRIMESTER,
        "timing": "Daily (W28+)",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Kicks / 2 hours",
        "normal_range": ">= 10 discrete kicks within 2 hours",
        "indian_clinical_protocol": "Sadovsky / Cardiff count. < 10 movements in 2 hours requires immediate non-stress test and Doppler scan.",
        "danger_threshold": "< 10 kicks in 2 hours or acute cessation of movement"
    },

    # -------------------------------------------------------------
    # 1.4 LABOR & DELIVERY MATERNAL TESTS
    # -------------------------------------------------------------
    59: {
        "id": 59,
        "name": "Admission Blood Type & Antibody Screen (Type & Crossmatch)",
        "stage": LifeStage.LABOR_AND_DELIVERY,
        "timing": "On Admission",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "Crossmatch",
        "normal_range": "Compatible units reserved",
        "indian_clinical_protocol": "Mandatory in all delivery centers. High-risk mothers (prior CS, placenta previa, severe anemia) require 2 units PRBC cross-matched.",
        "danger_threshold": "Antibody incompatibility with acute hemorrhage"
    },
    60: {
        "id": 60,
        "name": "Intrapartum Continuous / Intermittent CTG",
        "stage": LifeStage.LABOR_AND_DELIVERY,
        "timing": "Active Labor",
        "specimen": SpecimenType.CARDIOTOCOGRAPHY,
        "unit": "Classification (Normal / Suspicious / Pathological)",
        "normal_range": "Normal Category I (110-160 bpm, moderate variability, no late decels)",
        "indian_clinical_protocol": "Pathological CTG (prolonged bradycardia < 100 bpm > 3 min or repetitive late decelerations) mandates intrauterine resuscitation (left lateral position, IV fluids, stop oxytocin) and prompt delivery.",
        "danger_threshold": "Category III Pathological CTG"
    },
    61: {
        "id": 61,
        "name": "Partogram Cervical Progression Tracking",
        "stage": LifeStage.LABOR_AND_DELIVERY,
        "timing": "Active Labor",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "cm / hr",
        "normal_range": "Cervical dilation >= 1 cm/hr on or to left of Alert Line",
        "indian_clinical_protocol": "MoHFW & WHO Modified Partograph: If dilation crosses Alert line, augment with oxytocin. If dilation crosses Action Line (4h delay), prepare for emergency cesarean section for obstructed labor.",
        "danger_threshold": "Crossing the Action Line"
    },
    62: {
        "id": 62,
        "name": "Fetal Scalp Blood Lactate / pH",
        "stage": LifeStage.LABOR_AND_DELIVERY,
        "timing": "Active Labor",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "pH / mmol/L",
        "normal_range": "pH >= 7.25, Lactate <= 4.1 mmol/L",
        "indian_clinical_protocol": "pH < 7.20 or Lactate > 4.8 mmol/L confirms intrapartum fetal acidosis. Expedited delivery indicated.",
        "danger_threshold": "pH < 7.20 or Lactate > 4.8 mmol/L"
    },

    # -------------------------------------------------------------
    # 1.5 POSTPARTUM MATERNAL TESTS (Day 1 to 1 Year)
    # -------------------------------------------------------------
    63: {
        "id": 63,
        "name": "Post-Delivery Complete Blood Count (CBC)",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Day 1 – 2",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "g/dL",
        "normal_range": "Hb >= 10.0 g/dL",
        "indian_clinical_protocol": "Quantifies post-delivery blood loss. Hb < 7.0 g/dL requires blood transfusion.",
        "danger_threshold": "Hb < 7.0 g/dL or Platelets < 50000 /uL"
    },
    64: {
        "id": 64,
        "name": "Cord Blood ABO / Rh Typing",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Day 1 (At Birth)",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "Blood Group",
        "normal_range": "Rh Positive or Negative",
        "indian_clinical_protocol": "If mother is Rh-negative and baby is Rh-positive, administer 300 mcg Anti-D Immunoglobulin within 72 hours.",
        "danger_threshold": "Rh mismatch without Anti-D administration"
    },
    65: {
        "id": 65,
        "name": "Kleihauer-Betke (KB) Acid Elution Test / Rosette Screen",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Day 1 – 2",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "mL fetal blood",
        "normal_range": "< 30 mL fetal whole blood",
        "indian_clinical_protocol": "Quantifies massive feto-maternal hemorrhage to scale Anti-D dose (extra 10 mcg Anti-D per 1 mL fetal blood).",
        "danger_threshold": "Feto-maternal hemorrhage > 30 mL"
    },
    66: {
        "id": 66,
        "name": "Postpartum Uterine Tone & Lochia Assessment",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Day 1 – 14",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Tone & Character",
        "normal_range": "Uterus firmly contracted below umbilicus, Lochia Rubra without foul odor",
        "indian_clinical_protocol": "MoHFW PNC: Boggy uterus and soakage of > 1 pad/hr indicates Primary PPH (uterine atony). Uterotonics (Oxytocin, Misoprostol, Tranexamic Acid) immediately.",
        "danger_threshold": "Uterine atony with active gush of blood"
    },
    67: {
        "id": 67,
        "name": "Early Postpartum Blood Pressure Profile",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Days 3 – 7",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "mmHg",
        "normal_range": "Systolic < 130, Diastolic < 85 mmHg",
        "indian_clinical_protocol": "Screens for Delayed Postpartum Preeclampsia. BP >= 140/90 with headache warrants immediate readmission and antihypertensive therapy.",
        "danger_threshold": ">= 150/100 mmHg"
    },
    68: {
        "id": 68,
        "name": "Surgical Incision & Perineal Healing Exam (REEDA)",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Week 1 – 2",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "REEDA Scale (0-15)",
        "normal_range": "REEDA score 0 - 2 (Redness, Edema, Ecchymosis, Discharge, Approximation)",
        "indian_clinical_protocol": "Checks Pfannenstiel or episiotomy wound for surgical site infection (SSI) or wound dehiscence.",
        "danger_threshold": "REEDA >= 6 or purulent discharge"
    },
    69: {
        "id": 69,
        "name": "Postpartum 75g 2-Hour Oral Glucose Tolerance Test",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Week 6",
        "specimen": SpecimenType.PLASMA,
        "unit": "mg/dL",
        "normal_range": "Fasting < 100 mg/dL, 2-hr < 140 mg/dL (Normal)",
        "indian_clinical_protocol": "FOGSI & DIPSI: Mandatory at 6 weeks for all mothers who had GDM. Reclassifies status into Normal, Impaired Glucose Tolerance (140-199 mg/dL), or Type 2 Diabetes (>= 200 mg/dL).",
        "danger_threshold": "Fasting >= 126 or 2-hr >= 200 mg/dL (Type 2 Diabetes)"
    },
    70: {
        "id": 70,
        "name": "Postpartum Thyroid Function Panel (TSH & Free T4)",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Week 6 – Month 6",
        "specimen": SpecimenType.SERUM,
        "unit": "mIU/L, ng/dL",
        "normal_range": "TSH 0.4 - 4.5 mIU/L, FT4 0.8 - 1.8 ng/dL",
        "indian_clinical_protocol": "Screens for Postpartum Thyroiditis (common in anti-TPO positive mothers).",
        "danger_threshold": "TSH > 10.0 mIU/L or TSH < 0.1 mIU/L"
    },
    71: {
        "id": 71,
        "name": "Edinburgh Postnatal Depression Scale (EPDS / PHQ-9)",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Week 6 & Months 3, 6, 12",
        "specimen": SpecimenType.SURVEY_SCORE,
        "unit": "Score / 30",
        "normal_range": "EPDS < 10",
        "indian_clinical_protocol": "EPDS >= 10-13 indicates probable postnatal depression. Question 10 (self-harm ideation) > 0 requires immediate psychiatric crisis evaluation.",
        "danger_threshold": "EPDS >= 13 or any self-harm ideation"
    },
    72: {
        "id": 72,
        "name": "Cervical Cytology (Pap Smear / Liquid-Based)",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Week 6+",
        "specimen": SpecimenType.SWAB,
        "unit": "Bethesda System",
        "normal_range": "NILM (Negative for Intraepithelial Lesion or Malignancy)",
        "indian_clinical_protocol": "Resumption of cervical cancer screening after 6 weeks postpartum.",
        "danger_threshold": "HSIL, ASC-H, or Invasive Carcinoma"
    },
    73: {
        "id": 73,
        "name": "Postnatal Pelvic Floor & Musculoskeletal Assessment",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Week 6",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Oxford Scale (0-5)",
        "normal_range": "Pelvic floor muscle strength >= 3/5, Diastasis recti < 2 cm",
        "indian_clinical_protocol": "Screens for urinary incontinence and pelvic organ prolapse. Prescribes structured Kegel exercises.",
        "danger_threshold": "Severe POP-Q Stage 3/4 or fecal incontinence"
    },
    74: {
        "id": 74,
        "name": "Maternal Micronutrient Panel (Ferritin, Vit D, B12)",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Month 3 – 6",
        "specimen": SpecimenType.SERUM,
        "unit": "ng/mL, pg/mL",
        "normal_range": "Ferritin > 30 ng/mL, Vitamin D > 30 ng/mL, B12 > 200 pg/mL",
        "indian_clinical_protocol": "Essential in Indian mothers on vegetarian diets during exclusive lactation.",
        "danger_threshold": "B12 < 150 pg/mL or Ferritin < 15 ng/mL"
    },
    75: {
        "id": 75,
        "name": "Annual Cardiometabolic Profile (Lipids + FBS + HbA1c)",
        "stage": LifeStage.POSTPARTUM_MOTHER,
        "timing": "Month 12",
        "specimen": SpecimenType.SERUM,
        "unit": "Lipid profile & glucose",
        "normal_range": "LDL < 100, HDL > 50, Triglycerides < 150 mg/dL, HbA1c < 5.7%",
        "indian_clinical_protocol": "Long-term cardiovascular risk stratification for mothers with past history of preeclampsia, GDM, or preterm birth.",
        "danger_threshold": "HbA1c >= 6.5% or Total Cholesterol > 240 mg/dL"
    },

    # -------------------------------------------------------------
    # 2.1 IMMEDIATE NEWBORN TESTS (0 – 72 Hours)
    # -------------------------------------------------------------
    76: {
        "id": 76,
        "name": "1-Minute Apgar Scoring",
        "stage": LifeStage.IMMEDIATE_NEWBORN,
        "timing": "1 Min Post-Birth",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Score / 10",
        "normal_range": "7 - 10",
        "indian_clinical_protocol": "NSSK / NRP: Heart rate, respiratory effort, muscle tone, reflex irritability, color. Score <= 3 mandates active PPV and chest compressions.",
        "danger_threshold": "<= 3 (Severe depression)"
    },
    77: {
        "id": 77,
        "name": "5-Minute Apgar Scoring",
        "stage": LifeStage.IMMEDIATE_NEWBORN,
        "timing": "5 Min Post-Birth",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Score / 10",
        "normal_range": "7 - 10",
        "indian_clinical_protocol": "Gold standard of resuscitation response. Score < 7 mandates ongoing resuscitation and NICU/SNCU admission.",
        "danger_threshold": "< 7"
    },
    78: {
        "id": 78,
        "name": "10-Minute Apgar Scoring",
        "stage": LifeStage.IMMEDIATE_NEWBORN,
        "timing": "10 Min Post-Birth",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Score / 10",
        "normal_range": ">= 7",
        "indian_clinical_protocol": "Assesses prognosis and candidacy for Therapeutic Hypothermia in Hypoxic-Ischemic Encephalopathy (HIE).",
        "danger_threshold": "<= 5"
    },
    79: {
        "id": 79,
        "name": "Umbilical Cord Blood Gas Analysis (pH & Base Deficit)",
        "stage": LifeStage.IMMEDIATE_NEWBORN,
        "timing": "Immediate Birth",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "pH / mmol/L",
        "normal_range": "pH > 7.15, Base Deficit < 8 mmol/L",
        "indian_clinical_protocol": "Cord arterial pH < 7.00 or Base Deficit >= 12 mmol/L validates severe intrapartum metabolic acidemia.",
        "danger_threshold": "pH < 7.00 or Base Deficit >= 12 mmol/L"
    },
    80: {
        "id": 80,
        "name": "Critical Congenital Heart Disease (CCHD) Pulse Oximetry",
        "stage": LifeStage.IMMEDIATE_NEWBORN,
        "timing": ">= 24 Hours",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "SpO2 %",
        "normal_range": "SpO2 >= 95% in right hand and foot, difference <= 3%",
        "indian_clinical_protocol": "MoHFW RBSK: Screen for duct-dependent cardiac lesions. If SpO2 < 90% or 90-94% on 3 repeats, urgent pediatric echocardiogram.",
        "danger_threshold": "< 90% in either extremity or difference > 3%"
    },
    81: {
        "id": 81,
        "name": "Automated Auditory Brainstem Response (AABR)",
        "stage": LifeStage.IMMEDIATE_NEWBORN,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Pass / Refer",
        "normal_range": "Pass in both ears",
        "indian_clinical_protocol": "RBSK Universal Newborn Hearing Screening: Detects neural and sensory hearing loss.",
        "danger_threshold": "Refer in one or both ears"
    },
    82: {
        "id": 82,
        "name": "Otoacoustic Emissions (OAE / DPOAE)",
        "stage": LifeStage.IMMEDIATE_NEWBORN,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Pass / Refer",
        "normal_range": "Pass in both ears",
        "indian_clinical_protocol": "Cochlear outer hair cell function test.",
        "danger_threshold": "Refer (Failure to detect emissions)"
    },
    83: {
        "id": 83,
        "name": "Transcutaneous Bilirubin (TcB)",
        "stage": LifeStage.IMMEDIATE_NEWBORN,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "mg/dL",
        "normal_range": "< 75th percentile on Bhutani nomogram",
        "indian_clinical_protocol": "Non-invasive skin optical sensor. If TcB exceeds phototherapy threshold or >= 12 mg/dL, confirm with serum TSB.",
        "danger_threshold": "> 95th percentile for age in hours"
    },
    84: {
        "id": 84,
        "name": "Total Serum Bilirubin (TSB) & Direct Bilirubin",
        "stage": LifeStage.IMMEDIATE_NEWBORN,
        "timing": "24 – 72 Hours",
        "specimen": SpecimenType.SERUM,
        "unit": "mg/dL",
        "normal_range": "Age-appropriate safe zone (< 12 mg/dL at 48h)",
        "indian_clinical_protocol": "Plotted on AAP / Indian Academy of Pediatrics (IAP) phototherapy nomograms. Direct bilirubin > 1.0 mg/dL flags neonatal cholestasis (biliary atresia).",
        "danger_threshold": ">= Phototherapy / Exchange transfusion cutoff or Direct Bilirubin > 1.0 mg/dL"
    },
    85: {
        "id": 85,
        "name": "Point-of-Care Neonatal Blood Glucose",
        "stage": LifeStage.IMMEDIATE_NEWBORN,
        "timing": "1 – 24 Hours",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "mg/dL",
        "normal_range": ">= 45 mg/dL (after 4 hours of life)",
        "indian_clinical_protocol": "Essential in infants of diabetic mothers, preterm, SGA, or LGA. Blood glucose < 40-45 mg/dL requires immediate feeding or IV 10% Dextrose bolus (2 mL/kg).",
        "danger_threshold": "< 40 mg/dL (Symptomatic or refractory hypoglycemia)"
    },

    # -------------------------------------------------------------
    # 2.2 INBORN ERRORS OF METABOLISM (Guthrie Blood Spot Panel)
    # -------------------------------------------------------------
    86: {
        "id": 86,
        "name": "Phenylketonuria (PKU) Screen",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "umol/L",
        "normal_range": "Phenylalanine < 120 umol/L, Phe/Tyr < 2.0",
        "indian_clinical_protocol": "Early diagnosis prevents irreversible microcephaly and profound intellectual disability through phenylalanine-free diet.",
        "danger_threshold": "Phenylalanine >= 120 umol/L"
    },
    87: {
        "id": 87,
        "name": "Maple Syrup Urine Disease (MSUD)",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "umol/L",
        "normal_range": "Leucine + Isoleucine < 200 umol/L",
        "indian_clinical_protocol": "Branched-chain ketoaciduria causes acute ketoacidosis, cerebral edema, and neonatal coma.",
        "danger_threshold": "Elevated branched chain amino acids"
    },
    88: {
        "id": 88,
        "name": "Homocystinuria",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "umol/L",
        "normal_range": "Methionine < 50 umol/L",
        "indian_clinical_protocol": "Prevents thromboembolism, lens dislocation (ectopia lentis), and cognitive delays.",
        "danger_threshold": "Methionine > 50 umol/L"
    },
    89: {
        "id": 89,
        "name": "Classic Galactosemia",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "U/g Hb / mg/dL",
        "normal_range": "GALT enzyme activity normal, Total Galactose < 10 mg/dL",
        "indian_clinical_protocol": "GALT enzyme deficiency. Ingestion of breastmilk/lactose triggers fatal E. coli sepsis, cataracts, and liver failure. Immediate soy-based lactose-free formula.",
        "danger_threshold": "Low GALT activity (< 3.5 U/g Hb) or Total Galactose > 10 mg/dL"
    },
    90: {
        "id": 90,
        "name": "Congenital Hypothyroidism (CH)",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "mIU/L",
        "normal_range": "Neonatal TSH < 10 - 20 mIU/L",
        "indian_clinical_protocol": "Most common preventable cause of intellectual disability in India. TSH > 20 mIU/L requires immediate serum free T4 check and Levothyroxine 10-15 mcg/kg/day within 2 weeks of life.",
        "danger_threshold": "Heel-prick TSH > 20 mIU/L"
    },
    91: {
        "id": 91,
        "name": "Congenital Adrenal Hyperplasia (CAH)",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "ng/mL",
        "normal_range": "17-OHP < 10 - 20 ng/mL (weight adjusted)",
        "indian_clinical_protocol": "High prevalence in consanguineous Indian families. 21-hydroxylase deficiency triggers fatal neonatal salt-wasting crisis (hyponatremia, hyperkalemia, shock) by Day 7-14.",
        "danger_threshold": "17-OHP > 20 ng/mL"
    },
    92: {
        "id": 92,
        "name": "Medium-Chain Acyl-CoA Dehydrogenase (MCAD) Deficiency",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "umol/L",
        "normal_range": "Octanoylcarnitine (C8) < 0.3 umol/L",
        "indian_clinical_protocol": "Prevents sudden unexpected infant death triggered by fasting and hypoketotic hypoglycemia.",
        "danger_threshold": "C8 >= 0.3 umol/L"
    },
    93: {
        "id": 93,
        "name": "Very Long-Chain Acyl-CoA Dehydrogenase (VLCAD) Deficiency",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "umol/L",
        "normal_range": "C14:1 acylcarnitine normal",
        "indian_clinical_protocol": "Prevents lethal neonatal cardiomyopathy and metabolic arrest.",
        "danger_threshold": "Elevated C14:1"
    },
    94: {
        "id": 94,
        "name": "Carnitine Palmitoyltransferase (CPT-I & II) Deficiency",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "umol/L",
        "normal_range": "Free carnitine (C0) normal",
        "indian_clinical_protocol": "Prevents cardiac arrhythmias and rhabdomyolysis.",
        "danger_threshold": "Abnormal C0 / (C16+C18) ratio"
    },
    95: {
        "id": 95,
        "name": "Propionic Acidemia (PA)",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "umol/L",
        "normal_range": "Propionylcarnitine (C3) < 4.0 umol/L",
        "indian_clinical_protocol": "Prevents hyperammonemic coma and metabolic stroke.",
        "danger_threshold": "C3 > 5.0 umol/L"
    },
    96: {
        "id": 96,
        "name": "Methylmalonic Acidemia (MMA)",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "umol/L",
        "normal_range": "C3 and Methylmalonic acid normal",
        "indian_clinical_protocol": "Prevents metabolic ketoacidosis and renal failure.",
        "danger_threshold": "Elevated C3 with methylmalonic acid elevation"
    },
    97: {
        "id": 97,
        "name": "Isovaleric Acidemia (IVA)",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "umol/L",
        "normal_range": "Isovalerylcarnitine (C5) < 0.5 umol/L",
        "indian_clinical_protocol": "Characterized by 'sweaty feet' odor, ketoacidosis, and coma.",
        "danger_threshold": "C5 >= 0.5 umol/L"
    },
    98: {
        "id": 98,
        "name": "Glutaric Acidemia Type 1 (GA-1)",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "umol/L",
        "normal_range": "Glutarylcarnitine (C5DC) < 0.2 umol/L",
        "indian_clinical_protocol": "Untreated causes bilateral striatal necrosis and irreversible dystonic cerebral palsy during minor febrile illness.",
        "danger_threshold": "Elevated C5DC"
    },
    99: {
        "id": 99,
        "name": "Cystic Fibrosis (CF)",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "ng/mL",
        "normal_range": "Immunoreactive Trypsinogen (IRT) < 60 ng/mL",
        "indian_clinical_protocol": "Elevated IRT triggers CFTR DNA mutation reflex testing.",
        "danger_threshold": "IRT > 60 ng/mL with CFTR mutation"
    },
    100: {
        "id": 100,
        "name": "Severe Combined Immunodeficiency (SCID)",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "copies/uL",
        "normal_range": "T-cell Receptor Excision Circles (TREC) >= 25 copies/uL",
        "indian_clinical_protocol": "Undetectable TREC warns of fatal T-cell deficiency. Infant must NOT receive live BCG or OPV vaccine to prevent fatal disseminated BCG infection.",
        "danger_threshold": "TREC < 25 copies/uL (Positive SCID screen)"
    },
    101: {
        "id": 101,
        "name": "Spinal Muscular Atrophy (SMA)",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "Real-time PCR",
        "normal_range": "SMN1 Exon 7 Present (Homozygous normal)",
        "indian_clinical_protocol": "Absence of SMN1 Exon 7 identifies SMA Type 1. Early gene therapy (Zolgensma / Nusinersen) preserves motor neurons.",
        "danger_threshold": "Homozygous deletion of SMN1 exon 7"
    },
    102: {
        "id": 102,
        "name": "Sickle Cell Anemia & Hemoglobinopathies",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "HPLC fraction",
        "normal_range": "HbFA (Normal fetal/adult pattern)",
        "indian_clinical_protocol": "National Sickle Cell Elimination Mission: Identifies HbSS and HbS-beta-thalassemia. Daily prophylactic Penicillin V and pneumococcal vaccination prevents early pneumococcal sepsis.",
        "danger_threshold": "HbFS or HbSS phenotype"
    },
    103: {
        "id": 103,
        "name": "Biotinidase Deficiency",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "Enzyme Activity",
        "normal_range": "Normal colorimetric activity",
        "indian_clinical_protocol": "Prevents intractable infantile seizures, hypotonia, ataxia, alopecia, and hearing loss with oral biotin.",
        "danger_threshold": "Deficient enzyme activity (< 10%)"
    },
    104: {
        "id": 104,
        "name": "Glucose-6-Phosphate Dehydrogenase (G6PD) Deficiency",
        "stage": LifeStage.GUTHRIE_IEM_PANEL,
        "timing": "24 – 48 Hours",
        "specimen": SpecimenType.DRIED_BLOOD_SPOT,
        "unit": "U/g Hb",
        "normal_range": "G6PD activity >= 7.0 U/g Hb",
        "indian_clinical_protocol": "High prevalence in tribal and Mediterranean/Indian communities. G6PD deficiency triggers massive acute neonatal hyperbilirubinemia, Kernicterus, and hemolytic crises on exposure to oxidant drugs.",
        "danger_threshold": "< 2.0 U/g Hb (Severe deficiency)"
    },

    # -------------------------------------------------------------
    # 2.3 EARLY INFANCY TESTS (Weeks 1 – 4)
    # -------------------------------------------------------------
    105: {
        "id": 105,
        "name": "Newborn Weight Nadir & Regain Assessment",
        "stage": LifeStage.EARLY_INFANCY,
        "timing": "Days 3 – 14",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "% loss / grams",
        "normal_range": "Max loss < 7 - 10%, Birth weight regained by Day 10 - 14",
        "indian_clinical_protocol": "Weight loss > 10% indicates severe lactation failure, dehydration, and hypernatremia.",
        "danger_threshold": "Weight loss > 10% or failure to regain birth weight by Day 14"
    },
    106: {
        "id": 106,
        "name": "Umbilical Cord Stump & Granuloma Evaluation",
        "stage": LifeStage.EARLY_INFANCY,
        "timing": "Week 1 – 2",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Inspection",
        "normal_range": "Dry, clean, separated by Day 7 - 14",
        "indian_clinical_protocol": "Periumbilical erythema and purulent discharge indicates Omphalitis (high risk of neonatal septicemia). Silver nitrate application for persistent granuloma.",
        "danger_threshold": "Periumbilical erythema extending to abdominal wall (Omphalitis emergency)"
    },
    107: {
        "id": 107,
        "name": "Neonatal Primitive Reflex Examination",
        "stage": LifeStage.EARLY_INFANCY,
        "timing": "Week 1 – 4",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Symmetry & Presence",
        "normal_range": "Symmetric Moro, Rooting, Sucking, Palmar grasp present",
        "indian_clinical_protocol": "Asymmetric Moro indicates clavicle fracture or Erb's palsy (brachial plexus injury). Absent reflexes indicate severe central nervous system depression.",
        "danger_threshold": "Absent or markedly asymmetric reflexes"
    },
    108: {
        "id": 108,
        "name": "Ophthalmic Red Reflex Examination (Bruckner Test)",
        "stage": LifeStage.EARLY_INFANCY,
        "timing": "Week 2 – Month 1",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Red Reflex Symmetry",
        "normal_range": "Symmetric bright red-orange reflex in both eyes",
        "indian_clinical_protocol": "Universal screen for Retinoblastoma (life-threatening intraocular cancer) and congenital cataracts. Leukocoria (white pupil reflex) mandates immediate pediatric ophthalmology referral.",
        "danger_threshold": "White reflex (Leukocoria) or dark spot in pupillary axis"
    },
    109: {
        "id": 109,
        "name": "Developmental Hip Stability (Barlow & Ortolani Tests)",
        "stage": LifeStage.EARLY_INFANCY,
        "timing": "Week 2 – Month 1",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Stability",
        "normal_range": "Negative (No clunk or dislocatability)",
        "indian_clinical_protocol": "Barlow detects dislocatable hip; Ortolani detects reducible hip. Positive test mandates Pavlik harness before femoral head ossification.",
        "danger_threshold": "Palpable clunk / positive Ortolani or Barlow maneuver"
    },

    # -------------------------------------------------------------
    # 2.4 INFANCY DIAGNOSTIC & MILESTONE TESTS (Months 2 – 12)
    # -------------------------------------------------------------
    110: {
        "id": 110,
        "name": "Selective Infant Hip Ultrasound (Graf Classification)",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Weeks 4 – 6",
        "specimen": SpecimenType.ULTRASOUND,
        "unit": "Alpha and Beta angles",
        "normal_range": "Graf Type 1 (Alpha angle >= 60 degrees)",
        "indian_clinical_protocol": "Indicated in breech presentation, female infant with positive family history, or clinical click.",
        "danger_threshold": "Alpha angle < 50 degrees (Dysplastic hip)"
    },
    111: {
        "id": 111,
        "name": "WHO Growth Velocity Profiling (Weight, Length, OFC)",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Months 2, 4, 6, 9, 12",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Z-score / Percentiles",
        "normal_range": "-2 to +2 Z-score (3rd - 97th percentile)",
        "indian_clinical_protocol": "MoHFW ICDS / MCP Card: Crossing two major centile downward curves defines Failure to Thrive (FTT). Weight-for-height < -3 Z-score defines Severe Acute Malnutrition (SAM).",
        "danger_threshold": "Weight-for-age or Weight-for-height < -3 Z-score (SAM)"
    },
    112: {
        "id": 112,
        "name": "Visual Tracking & Strabismus Screen (Cover/Uncover)",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Months 2 – 6",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Visual Alignment",
        "normal_range": "Smooth 180 degree tracking; Hirschberg light reflex centered",
        "indian_clinical_protocol": "Persistent strabismus beyond 4 months requires pediatric ophthalmology evaluation to prevent amblyopia (lazy eye).",
        "danger_threshold": "Persistent inward/outward squint or absent visual fixation at 3 months"
    },
    113: {
        "id": 113,
        "name": "Auditory Behavioral Localization Test",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Months 4 – 6",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Auditory Orientation",
        "normal_range": "Direct head-turn to whisper / rattle sound at 4-6 months",
        "indian_clinical_protocol": "Failure to turn head toward mother's voice or loud noise indicates acquired or late-onset sensorineural hearing impairment.",
        "danger_threshold": "No auditory response or localization by 6 months"
    },
    114: {
        "id": 114,
        "name": "Complementary Solid Feeding Readiness Assessment",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Months 4 – 6",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Oral Motor Development",
        "normal_range": "Good head stability, loss of tongue-thrust reflex at 6 completed months",
        "indian_clinical_protocol": "MoHFW Infant and Young Child Feeding (IYCF): Exclusive breastfeeding for 6 completed months, followed by hygienic introduction of mashed semi-solid foods (dalia, khichdi, ragi).",
        "danger_threshold": "Severe dysphagia or persistent tongue-thrust reflex preventing feeding"
    },
    115: {
        "id": 115,
        "name": "Primary Dentition Eruption & Caries Risk Inspection",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Months 6 – 12",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Tooth Count & Enamel",
        "normal_range": "Eruption of lower/upper central incisors by 6-10 months",
        "indian_clinical_protocol": "Counsels against night bottle feeding with sweet liquids to prevent Early Childhood Caries (Nursing bottle syndrome).",
        "danger_threshold": "Severe enamel hypoplasia or complete absence of teeth by 13 months"
    },
    116: {
        "id": 116,
        "name": "Targeted Infant Anemia Fingerstick Screen",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Month 9",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "g/dL",
        "normal_range": "Hb >= 11.0 g/dL",
        "indian_clinical_protocol": "Anaemia Mukt Bharat: Prophylactic Iron-Folic Acid syrup (1 mL containing 20mg elemental iron + 100mcg folic acid bi-weekly) for all infants aged 6-59 months.",
        "danger_threshold": "Hb < 8.0 g/dL"
    },
    117: {
        "id": 117,
        "name": "Standardized Developmental Screening (ASQ-3 / SWYC)",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Month 9",
        "specimen": SpecimenType.SURVEY_SCORE,
        "unit": "Score across 5 domains",
        "normal_range": "Above screening cutoff in Gross Motor, Fine Motor, Communication, Problem Solving, Personal-Social",
        "indian_clinical_protocol": "RBSK Child Health Screening: Infant must sit without support, transfer objects hand-to-hand, and respond to own name by 9 months.",
        "danger_threshold": "Failure to sit without support at 9 months or regression of milestones"
    },
    118: {
        "id": 118,
        "name": "Universal Capillary / Venous Blood Lead Level (BLL)",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Month 12",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "ug/dL",
        "normal_range": "< 3.5 ug/dL (CDC reference level)",
        "indian_clinical_protocol": "High risk in India from traditional cosmetics (surma/kajal), lead-soldered plumbing, paint, and battery recycling. BLL >= 3.5 ug/dL mandates environmental decontamination.",
        "danger_threshold": ">= 3.5 ug/dL (Elevated toxic lead level)"
    },
    119: {
        "id": 119,
        "name": "Universal Infant Hemoglobin & Hematocrit Blood Test",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Month 12",
        "specimen": SpecimenType.WHOLE_BLOOD,
        "unit": "g/dL, %",
        "normal_range": "Hb >= 11.0 g/dL, Hematocrit >= 33%",
        "indian_clinical_protocol": "Universal screen for nutritional iron-deficiency anemia at 12 months. Treat with therapeutic iron 3 mg/kg/day for 3 months.",
        "danger_threshold": "Hb < 9.0 g/dL"
    },
    120: {
        "id": 120,
        "name": "Serum Ferritin & C-Reactive Protein (CRP)",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Month 12",
        "specimen": SpecimenType.SERUM,
        "unit": "ng/mL, mg/L",
        "normal_range": "Ferritin > 12 ng/mL, CRP < 5 mg/L",
        "indian_clinical_protocol": "Confirms true iron deficiency depletion when baseline Hb is borderline or when infection is ruled out by normal CRP.",
        "danger_threshold": "Ferritin < 12 ng/mL with normal CRP"
    },
    121: {
        "id": 121,
        "name": "Tuberculosis (TB) Risk Assessment Questionnaire",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Month 12",
        "specimen": SpecimenType.SURVEY_SCORE,
        "unit": "Questionnaire",
        "normal_range": "Negative exposure risk",
        "indian_clinical_protocol": "National Tuberculosis Elimination Program (NTEP): Positive contact with adult pulmonary TB case mandates Mantoux Tuberculin Skin Test (TST) and Isoniazid Preventive Therapy (IPT).",
        "danger_threshold": "Active contact with pulmonary TB patient"
    },
    122: {
        "id": 122,
        "name": "Pediatric Oral Health Exam & Fluoride Varnish Application",
        "stage": LifeStage.INFANCY_MONTHS_2_12,
        "timing": "Month 12",
        "specimen": SpecimenType.PHYSICAL_ASSESSMENT,
        "unit": "Topical Varnish",
        "normal_range": "5% NaF varnish applied to primary teeth",
        "indian_clinical_protocol": "Professional topical application of 5% Sodium Fluoride varnish to protect primary tooth enamel.",
        "danger_threshold": "Visible demineralization / white spot lesions"
    }
}


def get_test_by_id(test_id: int) -> Optional[Dict[str, Any]]:
    return MASTER_TESTS_CATALOG.get(test_id)


def search_tests_by_name(query: str) -> List[Dict[str, Any]]:
    q = query.lower()
    return [t for t in MASTER_TESTS_CATALOG.values() if q in t["name"].lower()]


def get_tests_by_stage(stage: LifeStage) -> List[Dict[str, Any]]:
    return [t for t in MASTER_TESTS_CATALOG.values() if t["stage"] == stage]
