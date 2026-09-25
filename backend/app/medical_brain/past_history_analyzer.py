"""
MaternaCare Previous Pregnancy & Obstetric History Clinical Intelligence Engine.
Analyzes prior maternal complications, obstetric indices (Gravida, Para, Abortions, Living, Stillbirths),
and calculates empirical recurrence risks with preventive clinical actions adhering to FOGSI & Indian National protocols.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class PastObstetricHistoryProfile(BaseModel):
    gravida: int = Field(1, description="Total number of confirmed pregnancies including current")
    para: int = Field(0, description="Number of viable births (> 24 weeks)")
    living_children: int = Field(0, description="Current living children")
    abortions: int = Field(0, description="Total pregnancy losses before 20-24 weeks")
    spontaneous_abortions: int = Field(0, description="Natural miscarriages")
    stillbirths: int = Field(0, description="Intrauterine fetal demises after 24 weeks")
    previous_c_sections: int = Field(0, description="Number of previous cesarean deliveries")
    inter_pregnancy_interval_months: Optional[int] = Field(None, description="Months between last delivery and current conception")
    
    # Specific previous pregnancy complications
    prior_preeclampsia: bool = Field(False, description="Did she have preeclampsia or eclampsia in any previous pregnancy?")
    prior_early_onset_preeclampsia: bool = Field(False, description="Was the preeclampsia early onset (< 34 weeks)?")
    prior_gestational_diabetes: bool = Field(False, description="Did she have Gestational Diabetes Mellitus (GDM)?")
    prior_postpartum_hemorrhage: bool = Field(False, description="Did she experience major PPH (> 500 mL vaginal or > 1000 mL CS)?")
    prior_preterm_delivery: bool = Field(False, description="Did she deliver spontaneously before 37 completed weeks?")
    prior_low_birth_weight: bool = Field(False, description="Did she deliver a baby weighing < 2500 grams?")
    prior_fetal_growth_restriction: bool = Field(False, description="Was there documented IUGR / FGR?")
    prior_stillbirth_or_neonatal_death: bool = Field(False, description="Did a previous baby die in utero or in first 28 days of life?")
    prior_rh_isoimmunization: bool = Field(False, description="Was there documented Rh sensitization / positive antibody titer?")
    prior_cervical_incompetence: bool = Field(False, description="Did she have mid-trimester painless cervical dilation or prior cerclage?")
    
    # Medical and Genetic Co-morbidities
    chronic_hypertension: bool = Field(False, description="Pre-existing hypertension before pregnancy")
    pregestational_diabetes: bool = Field(False, description="Pre-existing Type 1 or Type 2 Diabetes")
    hypothyroidism: bool = Field(False, description="Diagnosed thyroid disorder")
    thalassemia_trait: bool = Field(False, description="Maternal beta-thalassemia carrier / HbA2 > 3.5%")
    consanguineous_marriage: bool = Field(False, description="Is the couple related (1st or 2nd cousins)?")


class HistoryRiskAlert(BaseModel):
    complication_name: str
    recurrence_risk_percentage: str
    clinical_significance: str
    mandated_tests: List[int]  # Corresponds to Master Test IDs (1 - 122)
    clinical_action_plan: str
    indian_guideline_reference: str


class HistoryAnalysisReport(BaseModel):
    is_high_risk_pregnancy: bool
    risk_level: str  # LOW, MODERATE, HIGH, CRITICAL
    gravida_para_status: str
    primary_risk_drivers: List[str]
    alerts: List[HistoryRiskAlert]
    preventive_prescriptions_indicated: List[str]
    special_surveillance_schedule: List[str]


class PastHistoryAnalyzer:
    """
    Expert Obstetric Risk Engine specialized in evaluating Indian women's prior pregnancy complications.
    """

    @staticmethod
    def analyze_history(profile: PastObstetricHistoryProfile) -> HistoryAnalysisReport:
        alerts: List[HistoryRiskAlert] = []
        risk_drivers: List[str] = []
        prescriptions: List[str] = []
        surveillance: List[str] = []

        is_high_risk = False
        overall_severity = "LOW"

        # 1. Prior Pre-eclampsia / Eclampsia Analysis
        if profile.prior_preeclampsia:
            is_high_risk = True
            overall_severity = "HIGH"
            recurrence = "25% - 50%" if profile.prior_early_onset_preeclampsia else "15% - 20%"
            risk_drivers.append("Previous Pregnancy Preeclampsia (Elevated Endothelial Dysfunction Risk)")
            prescriptions.append("Low-Dose Aspirin 150 mg PO once daily at bedtime from 11-14 weeks until 36 weeks (FOGSI Recommendation)")
            prescriptions.append("Calcium Carbonate 1000 - 1500 mg daily in divided doses (WHO Maternal Supplementation)")
            surveillance.append("First Trimester Mean Uterine Artery Doppler at 11-13+6w (Test #24)")
            surveillance.append("Serum sFlt-1 / PlGF biomarker ratio at 24-28w and 32w (Test #46)")
            surveillance.append("Bi-weekly blood pressure tracking and spot urine protein:creatinine ratio (Tests #44, #45)")

            alerts.append(HistoryRiskAlert(
                complication_name="Recurrent Preeclampsia / Gestational Hypertension",
                recurrence_risk_percentage=recurrence,
                clinical_significance="History of prior preeclampsia increases risk of early-onset preeclampsia, placental abruption, and fetal growth restriction.",
                mandated_tests=[24, 25, 44, 45, 46, 47, 48],
                clinical_action_plan="Initiate Aspirin 150mg at bedtime before 16 weeks. Screen uterine artery Doppler. Educate on warning signs: severe frontal headache, scotoma, and epigastric pain.",
                indian_guideline_reference="FOGSI Good Clinical Practice Recommendations for Hypertensive Disorders of Pregnancy (2022)"
            ))

        # 2. Prior Gestational Diabetes Mellitus (GDM)
        if profile.prior_gestational_diabetes:
            is_high_risk = True
            if overall_severity != "HIGH":
                overall_severity = "MODERATE"
            risk_drivers.append("Prior Gestational Diabetes (Pancreatic Beta-Cell Decompensation Tendency)")
            surveillance.append("Immediate early 75g OGTT or FBS at first booking visit (Tests #15, #35) instead of waiting for 24 weeks")
            surveillance.append("Repeat 75g OGTT at 24-28 weeks if initial first-trimester test is normal")
            surveillance.append("Third-trimester serial fetal biometry to monitor for fetal macrosomia and polyhydramnios (Tests #38, #39)")

            alerts.append(HistoryRiskAlert(
                complication_name="Recurrent Gestational Diabetes Mellitus (GDM)",
                recurrence_risk_percentage="50% - 70% in Indian Women",
                clinical_significance="South Asian ethnicity carries the world's highest baseline insulin resistance. Recurrence rate in subsequent pregnancies exceeds 50%.",
                mandated_tests=[15, 16, 35, 38, 39],
                clinical_action_plan="Perform early 75g OGTT at booking. Provide Medical Nutrition Therapy (MNT: 3 meals, 3 snacks, low glycemic index carbs). Target fasting < 90 mg/dL, 1-hr post-meal < 130 mg/dL, 2-hr < 120 mg/dL.",
                indian_guideline_reference="DIPSI Guidelines / MoHFW National Guidelines for Diagnosis & Management of GDM in India"
            ))

        # 3. Prior Cesarean Section (Previous LSCS)
        if profile.previous_c_sections > 0:
            is_high_risk = True
            risk_drivers.append(f"Previous Cesarean Section (Count: {profile.previous_c_sections})")
            surveillance.append("Targeted early anatomy scan to assess placental relationship to hysterotomy scar (TIFFA, Test #32)")
            surveillance.append("Third-trimester uterine lower segment thickness scan (< 2.0 - 2.5 mm warns of scar dehiscence)")

            interval_note = ""
            if profile.inter_pregnancy_interval_months and profile.inter_pregnancy_interval_months < 18:
                overall_severity = "HIGH"
                interval_note = " SHORT INTER-PREGNANCY INTERVAL (< 18 months) significantly multiplies scar rupture risk."

            alerts.append(HistoryRiskAlert(
                complication_name="Uterine Scar / Morbidly Adherent Placenta (Placenta Accreta Spectrum)",
                recurrence_risk_percentage=f"Uterine rupture risk ~0.5% for 1 CS, ~1.5-2.0% for >=2 CS.{interval_note}",
                clinical_significance="Risk of anterior low-lying placenta implanting over previous scar causing Placenta Previa-Accreta spectrum. In labor, risk of scar dehiscence.",
                mandated_tests=[3, 32, 38, 53, 59, 60],
                clinical_action_plan="Screen placental site on ultrasound. If placenta previa is anterior over scar, perform color Doppler / MRI for accreta. If candidate for VBAC, continuous intrapartum CTG is mandatory.",
                indian_guideline_reference="FOGSI Guidelines for Vaginal Birth After Cesarean Section (VBAC) & Placenta Accreta"
            ))

        # 4. Prior Spontaneous Preterm Birth (< 37 weeks)
        if profile.prior_preterm_delivery:
            is_high_risk = True
            overall_severity = "HIGH"
            risk_drivers.append("History of Spontaneous Preterm Delivery")
            prescriptions.append("Vaginal Micronized Progesterone 200 mg nightly from 16 to 36 weeks")
            surveillance.append("Serial transvaginal cervical length (TVCL) ultrasound every 2 weeks from 16 to 24 weeks (Test #33)")

            alerts.append(HistoryRiskAlert(
                complication_name="Recurrent Spontaneous Preterm Birth",
                recurrence_risk_percentage="25% - 35% (Increases with each additional preterm delivery)",
                clinical_significance="Short cervical length (< 25 mm) or history of preterm birth indicates premature cervical ripening or subclinical intra-amniotic inflammation.",
                mandated_tests=[18, 33, 51],
                clinical_action_plan="Start vaginal progesterone at 16 weeks. Screen cervical length. If TVCL <= 25 mm before 24 weeks, cervical cerclage indicated.",
                indian_guideline_reference="FOGSI Recommendations on Prevention and Management of Preterm Labor"
            ))

        # 5. Prior Postpartum Hemorrhage (PPH)
        if profile.prior_postpartum_hemorrhage:
            is_high_risk = True
            risk_drivers.append("History of Major Postpartum Hemorrhage (PPH)")
            prescriptions.append("Aggressive antenatal correction of anemia (Target Hb >= 11.5 g/dL before delivery)")
            surveillance.append("Delivery strictly in a facility with 24x7 blood bank and obstetrician (Test #59 Type & Screen reserved)")

            alerts.append(HistoryRiskAlert(
                complication_name="Recurrent Postpartum Hemorrhage",
                recurrence_risk_percentage="15% - 20%",
                clinical_significance="Prior uterine atony or abnormal placentation increases risk of acute, life-threatening intrapartum blood loss.",
                mandated_tests=[4, 36, 52, 59, 63, 66],
                clinical_action_plan="Delivery planned at tertiary facility. Secure two wide-bore IV cannulae (16G) in active labor. Cross-match 2 units PRBC. Immediate Active Management of Third Stage of Labor (IV Oxytocin 10 IU, Carbetocin, or Misoprostol + Tranexamic Acid 1g IV).",
                indian_guideline_reference="FOGSI Postpartum Hemorrhage Clinical Practice Guidelines & MoHFW Dakshata Protocol"
            ))

        # 6. Prior Stillbirth / Intrauterine Fetal Demise (IUFD)
        if profile.stillbirths > 0 or profile.prior_stillbirth_or_neonatal_death:
            is_high_risk = True
            overall_severity = "CRITICAL"
            risk_drivers.append("Previous Unexplained Stillbirth / Intrauterine Fetal Demise")
            surveillance.append("Serial third-trimester fetal surveillance: Weekly CTG/NST (Test #54) + Umbilical/MCA Doppler (Tests #40, #41) from 32 weeks")
            surveillance.append("Planned induction of labor by 37-38 weeks (or 1-2 weeks earlier than gestational age of prior demise)")

            alerts.append(HistoryRiskAlert(
                complication_name="Recurrent Fetal Demise / Unexplained Stillbirth",
                recurrence_risk_percentage="2 to 5 times population baseline risk",
                clinical_significance="Demands intensive search for antiphospholipid antibody syndrome (APLA), maternal thrombophilia, severe GDM, or fetomaternal hemorrhage.",
                mandated_tests=[15, 19, 35, 38, 40, 41, 54, 55, 58],
                clinical_action_plan="Thorough maternal thrombophilia and metabolic workup. Initiate rigorous DFKC kick counting from 28w. Weekly Doppler and biophysical profile from 32w. Plan delivery by 38 weeks.",
                indian_guideline_reference="FOGSI Guidelines on Evaluation and Management of Stillbirth"
            ))

        # 7. Recurrent Pregnancy Loss (>= 2 or 3 miscarriages)
        if profile.abortions >= 2:
            is_high_risk = True
            if overall_severity == "LOW":
                overall_severity = "MODERATE"
            risk_drivers.append(f"Recurrent Pregnancy Loss / Miscarriage History (Abortions: {profile.abortions})")
            surveillance.append("Early viability TVS at 6-8 weeks (Test #3)")
            surveillance.append("Maternal TSH, HbA1c, and Antiphospholipid Antibody (aPL) panel (Tests #13, #16)")

            alerts.append(HistoryRiskAlert(
                complication_name="Recurrent Pregnancy Loss (RPL)",
                recurrence_risk_percentage="25% - 40% after 2-3 consecutive losses",
                clinical_significance="Underlying causes include parental balanced chromosomal translocations, uterine septa, luteal phase defect, or Antiphospholipid Syndrome.",
                mandated_tests=[2, 3, 13, 16],
                clinical_action_plan="Perform early ultrasound to confirm intrauterine pregnancy. Screen for Antiphospholipid Syndrome (Lupus Anticoagulant, Anticardiolipin, Anti-Beta2-Glycoprotein-I). If APLA positive, initiate Low Molecular Weight Heparin (LMWH) + Low Dose Aspirin.",
                indian_guideline_reference="FOGSI Guidelines for Management of Recurrent Pregnancy Loss (RPL)"
            ))

        # 8. Prior FGR / Low Birth Weight
        if profile.prior_fetal_growth_restriction or profile.prior_low_birth_weight:
            is_high_risk = True
            if overall_severity == "LOW":
                overall_severity = "MODERATE"
            risk_drivers.append("History of Fetal Growth Restriction / Low Birth Weight")
            prescriptions.append("Low-Dose Aspirin 150 mg at bedtime if associated with prior placental insufficiency")
            surveillance.append("Serial growth scans every 3-4 weeks from 26 weeks (Test #38) + Umbilical artery Doppler (Test #40)")

            alerts.append(HistoryRiskAlert(
                complication_name="Recurrent Fetal Growth Restriction (FGR)",
                recurrence_risk_percentage="20% - 25%",
                clinical_significance="Maternal vascular malperfusion of the placenta tends to recur in subsequent pregnancies.",
                mandated_tests=[24, 38, 39, 40, 41, 43],
                clinical_action_plan="Serial ultrasound biometry and Doppler velocimetry to track abdominal circumference and cerebroplacental ratio (CPR). Delivery timed according to Doppler ductus venosus criteria.",
                indian_guideline_reference="FOGSI Fetal Growth Restriction Clinical Practice Protocol"
            ))

        # 9. Consanguinity & Thalassemia Carrier Trait
        if profile.consanguineous_marriage or profile.thalassemia_trait:
            is_high_risk = True
            risk_drivers.append("Genetic / Hemoglobinopathy Risk (Consanguinity or Thalassemia Carrier)")
            surveillance.append("Hemoglobin HPLC of the husband / partner (Test #19)")
            surveillance.append("Targeted prenatal genetic diagnosis (CVS / Amniocentesis, Tests #26, #31) if both parents are carriers")

            alerts.append(HistoryRiskAlert(
                complication_name="Hemoglobinopathy / Inborn Error of Metabolism Risk",
                recurrence_risk_percentage="25% chance of Thalassemia Major / Autosomal Recessive Disorder if both parents carriers",
                clinical_significance="High priority under Indian National Thalassemia Elimination Guidelines. Beta-Thalassemia Major causes transfusion-dependent severe anemia in the child.",
                mandated_tests=[19, 26, 31, 86, 91, 102],
                clinical_action_plan="Mandatory partner screening via Hb HPLC. If husband is also a Beta-Thalassemia carrier (HbA2 > 3.5%), offer prenatal diagnostic CVS at 11-13 weeks.",
                indian_guideline_reference="MoHFW National Guidelines on Hemoglobinopathies in India"
            ))

        gp_str = f"G{profile.gravida} P{profile.para} L{profile.living_children} A{profile.abortions} S{profile.stillbirths}"

        return HistoryAnalysisReport(
            is_high_risk_pregnancy=is_high_risk,
            risk_level=overall_severity if is_high_risk else "LOW",
            gravida_para_status=gp_str,
            primary_risk_drivers=risk_drivers if risk_drivers else ["No significant previous obstetric complications reported."],
            alerts=alerts,
            preventive_prescriptions_indicated=list(set(prescriptions)),
            special_surveillance_schedule=list(set(surveillance))
        )


past_history_analyzer = PastHistoryAnalyzer()
