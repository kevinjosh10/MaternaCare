from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.models.risk import RiskAssessment, ExplanationFeature
from app.models.observation import Observation
from app.models.symptom import Symptom
from app.models.pregnancy import Pregnancy
from app.schemas.risk import RiskAssessmentCreate, ClinicianReviewUpdate


class RiskAssessmentService:

    @staticmethod
    def evaluate_maternal_risk(
        db: Session,
        patient_id: str,
        pregnancy_id: Optional[str] = None
    ) -> RiskAssessment:
        """
        Calculates configurable clinical risk scores based on longitudinal vitals,
        symptoms, and historical risk flags.
        Adheres strictly to the requirement:
        'The AI must not claim to diagnose. Use language such as:
        Potentially concerning pattern detected — clinical review recommended.'
        """
        # Fetch latest vitals
        latest_systolic = db.query(Observation).filter(
            Observation.patient_id == patient_id,
            Observation.observation_type.in_(["systolic_bp", "systolic blood pressure"])
        ).order_by(Observation.timestamp.desc()).first()

        latest_diastolic = db.query(Observation).filter(
            Observation.patient_id == patient_id,
            Observation.observation_type.in_(["diastolic_bp", "diastolic blood pressure"])
        ).order_by(Observation.timestamp.desc()).first()

        # Fetch recent warning symptoms
        recent_symptoms = db.query(Symptom).filter(
            Symptom.patient_id == patient_id
        ).order_by(Symptom.date_time.desc()).limit(5).all()

        sys_val = latest_systolic.value if latest_systolic else 115.0
        dia_val = latest_diastolic.value if latest_diastolic else 75.0

        risk_score = 0.15
        risk_level = "LOW"
        risk_category = "GENERAL_OBSTETRIC"
        contributing_factors = []
        explanation_features = []
        rank = 1

        # Check blood pressure thresholds (aligned with WHO Preeclampsia protocols)
        if sys_val >= 160 or dia_val >= 110:
            risk_score = 0.92
            risk_level = "CRITICAL"
            risk_category = "SEVERE_PREECLAMPSIA"
            contributing_factors.append(f"Severe systolic/diastolic blood pressure elevation ({int(sys_val)}/{int(dia_val)} mmHg)")
            explanation_features.append({
                "feature": "blood_pressure_severity",
                "feature_value": f"{int(sys_val)}/{int(dia_val)} mmHg",
                "contribution": 0.48,
                "direction": "INCREASE_RISK",
                "rank": rank
            })
            rank += 1
        elif sys_val >= 140 or dia_val >= 90:
            risk_score = 0.68
            risk_level = "HIGH"
            risk_category = "GESTATIONAL_HYPERTENSION"
            contributing_factors.append(f"Elevated blood pressure ({int(sys_val)}/{int(dia_val)} mmHg)")
            explanation_features.append({
                "feature": "blood_pressure_severity",
                "feature_value": f"{int(sys_val)}/{int(dia_val)} mmHg",
                "contribution": 0.35,
                "direction": "INCREASE_RISK",
                "rank": rank
            })
            rank += 1

        # Symptom evaluation
        for sym in recent_symptoms:
            if sym.symptom_type in ["HEADACHE", "BLURRED_VISION", "EPIGASTRIC_PAIN"]:
                risk_score = min(0.95, risk_score + 0.20)
                if risk_level not in ["CRITICAL"]:
                    risk_level = "HIGH"
                contributing_factors.append(f"Reported warning sign: {sym.symptom_type} (Severity: {sym.severity})")
                explanation_features.append({
                    "feature": f"symptom_{sym.symptom_type.lower()}",
                    "feature_value": f"{sym.severity}",
                    "contribution": 0.25,
                    "direction": "INCREASE_RISK",
                    "rank": rank
                })
                rank += 1
            elif sym.symptom_type == "VAGINAL_BLEEDING":
                risk_score = 0.95
                risk_level = "CRITICAL"
                risk_category = "ANTEPARTUM_HEMORRHAGE"
                contributing_factors.append("Active vaginal bleeding reported")
                explanation_features.append({
                    "feature": "vaginal_bleeding",
                    "feature_value": "PRESENT",
                    "contribution": 0.50,
                    "direction": "INCREASE_RISK",
                    "rank": rank
                })
                rank += 1

        # Check pregnancy high_risk_flag
        if pregnancy_id:
            pregnancy = db.query(Pregnancy).filter(Pregnancy.pregnancy_id == pregnancy_id).first()
            if pregnancy and pregnancy.high_risk_flag:
                contributing_factors.append(f"Baseline pregnancy risk: {pregnancy.high_risk_reason or 'High Risk'}")
                explanation_features.append({
                    "feature": "prior_obstetric_risk_flag",
                    "feature_value": "TRUE",
                    "contribution": 0.15,
                    "direction": "INCREASE_RISK",
                    "rank": rank
                })

        # Safe clinical statement
        if risk_level in ["HIGH", "CRITICAL"]:
            explanation = (
                f"Potentially concerning pattern detected — clinical review recommended. "
                f"Elevated risk indicators identified for {risk_category}. "
                f"Immediate clinical evaluation of maternal vitals, fetal wellbeing, and laboratory panel advised."
            )
        elif risk_level == "MODERATE":
            explanation = (
                "Mild clinical variation observed. Regular clinical monitoring recommended "
                "at the next scheduled antenatal visit."
            )
        else:
            explanation = "Clinical parameters within observed normal ranges. Continue routine antenatal care protocol."

        assessment = RiskAssessment(
            patient_id=patient_id,
            pregnancy_id=pregnancy_id,
            risk_category=risk_category,
            risk_score=round(risk_score, 2),
            risk_level=risk_level,
            input_snapshot={
                "systolic_bp": sys_val,
                "diastolic_bp": dia_val,
                "recent_symptoms_count": len(recent_symptoms)
            },
            contributing_factors=contributing_factors,
            trend_features={"bp_status": "ELEVATED" if sys_val >= 140 else "NORMAL"},
            explanation=explanation,
            clinician_review_status="PENDING_REVIEW"
        )
        db.add(assessment)
        db.flush()

        for feat in explanation_features:
            ef = ExplanationFeature(
                assessment_id=assessment.assessment_id,
                feature=feat["feature"],
                feature_value=feat["feature_value"],
                contribution=feat["contribution"],
                direction=feat["direction"],
                rank=feat["rank"]
            )
            db.add(ef)

        db.commit()
        db.refresh(assessment)
        return assessment

    @staticmethod
    def get_assessment(db: Session, assessment_id: str) -> Optional[RiskAssessment]:
        return db.query(RiskAssessment).filter(RiskAssessment.assessment_id == assessment_id).first()

    @staticmethod
    def review_assessment(db: Session, assessment_id: str, review_in: ClinicianReviewUpdate) -> Optional[RiskAssessment]:
        assessment = RiskAssessmentService.get_assessment(db, assessment_id)
        if not assessment:
            return None
        assessment.clinician_review_status = review_in.clinician_review_status
        assessment.clinician_notes = review_in.clinician_notes
        db.commit()
        db.refresh(assessment)
        return assessment


risk_service = RiskAssessmentService()
