from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.models.history import ObstetricHistory, MedicalHistory
from app.models.pregnancy import Pregnancy
from app.models.visit import AntenatalVisit
from app.models.observation import Observation
from app.models.symptom import Symptom
from app.models.lab import LabResult
from app.models.ultrasound import UltrasoundRecord
from app.models.medication import MedicationRecord
from app.models.document import Document
from app.models.delivery import Delivery
from app.models.newborn import Newborn, NewbornVisit
from app.models.postpartum import PostpartumVisit
from app.models.risk import RiskAssessment
from app.models.referral import Referral

from app.schemas.timeline import TimelineEvent, PatientTimelineResponse, PatientSummaryResponse
from app.schemas.patient import PatientResponse, ObstetricHistoryResponse, MedicalHistoryResponse
from app.schemas.pregnancy import PregnancyResponse
from app.schemas.risk import RiskAssessmentResponse
from app.schemas.referral import ReferralResponse
from app.schemas.delivery import DeliveryResponse
from app.schemas.newborn import NewbornResponse


class TimelineService:

    @staticmethod
    def get_patient_timeline(db: Session, patient_id: str) -> Optional[PatientTimelineResponse]:
        patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
        if not patient:
            return None

        events: List[TimelineEvent] = []

        # 1. Obstetric History
        obs_hist = db.query(ObstetricHistory).filter(ObstetricHistory.patient_id == patient_id).first()
        if obs_hist:
            events.append(TimelineEvent(
                timestamp=obs_hist.created_at,
                date=obs_hist.created_at.strftime("%Y-%m-%d"),
                event_type="PREVIOUS_OBSTETRIC_HISTORY",
                title="Baseline Obstetric History Recorded",
                summary=(
                    f"Previous Pregnancies: {obs_hist.previous_pregnancies}, "
                    f"Live Births: {obs_hist.previous_live_births}, "
                    f"Prior Preeclampsia: {'Yes' if obs_hist.previous_preeclampsia else 'No'}"
                ),
                details={
                    "previous_c_sections": obs_hist.previous_c_sections,
                    "previous_abortions": obs_hist.previous_abortions,
                    "previous_preeclampsia": obs_hist.previous_preeclampsia,
                    "previous_gestational_diabetes": obs_hist.previous_gestational_diabetes
                }
            ))

        # 2. Pregnancies
        pregnancies = db.query(Pregnancy).filter(Pregnancy.patient_id == patient_id).all()
        for preg in pregnancies:
            dt = datetime.combine(preg.pregnancy_start_date or preg.created_at.date(), datetime.min.time())
            events.append(TimelineEvent(
                timestamp=dt,
                date=dt.strftime("%Y-%m-%d"),
                event_type="PREGNANCY_REGISTRATION",
                title=f"Pregnancy #{preg.pregnancy_number} Registered",
                summary=f"Gravida {preg.gravida} Para {preg.para}, Gestational Age: {preg.gestational_age or 'N/A'}w, High Risk: {preg.high_risk_flag}",
                details={"high_risk_reason": preg.high_risk_reason, "estimated_due_date": str(preg.estimated_due_date)},
                severity_or_status="HIGH_RISK" if preg.high_risk_flag else "ROUTINE"
            ))

        # 3. ANC Visits
        anc_visits = db.query(AntenatalVisit).filter(AntenatalVisit.patient_id == patient_id).all()
        for anc in anc_visits:
            dt = datetime.combine(anc.visit_date, datetime.min.time())
            events.append(TimelineEvent(
                timestamp=dt,
                date=anc.visit_date.strftime("%Y-%m-%d"),
                event_type="ANC_VISIT",
                title=f"Antenatal Care Visit ({anc.gestational_age or ''}w)",
                summary=f"BP: {int(anc.systolic_bp or 0)}/{int(anc.diastolic_bp or 0)} mmHg, FHR: {anc.fetal_heart_rate or 'N/A'} bpm, Fundal Ht: {anc.fundal_height or 'N/A'} cm",
                details={
                    "weight": anc.weight,
                    "symptoms": anc.symptoms,
                    "warning_signs": anc.warning_signs,
                    "edema": anc.edema,
                    "clinical_notes": anc.clinical_notes
                }
            ))

        # 4. Clinical Observations (Time series)
        observations = db.query(Observation).filter(Observation.patient_id == patient_id).all()
        for obs in observations:
            events.append(TimelineEvent(
                timestamp=obs.timestamp,
                date=obs.timestamp.strftime("%Y-%m-%d"),
                event_type="OBSERVATION",
                title=f"Observation: {obs.observation_type.replace('_', ' ').title()}",
                summary=f"{obs.observation_type}: {obs.value} {obs.unit} (Source: {obs.source}, Verified: {obs.verified})",
                details={"value": obs.value, "unit": obs.unit, "verified": obs.verified}
            ))

        # 5. Symptoms
        symptoms = db.query(Symptom).filter(Symptom.patient_id == patient_id).all()
        for sym in symptoms:
            events.append(TimelineEvent(
                timestamp=sym.date_time,
                date=sym.date_time.strftime("%Y-%m-%d"),
                event_type="SYMPTOM",
                title=f"Reported Symptom: {sym.symptom_type}",
                summary=f"Severity: {sym.severity}, Duration: {sym.duration or 'N/A'}, Onset: {sym.onset or 'N/A'}",
                details={"associated": sym.associated_symptoms, "reported_by": sym.reported_by},
                severity_or_status=sym.severity
            ))

        # 6. Labs
        labs = db.query(LabResult).filter(LabResult.patient_id == patient_id).all()
        for lab in labs:
            dt = datetime.combine(lab.test_date, datetime.min.time())
            events.append(TimelineEvent(
                timestamp=dt,
                date=lab.test_date.strftime("%Y-%m-%d"),
                event_type="LAB_RESULT",
                title=f"Lab Test: {lab.test_name}",
                summary=f"Result: {lab.result} {lab.unit or ''} (Abnormal: {lab.abnormal_flag}, Status: {lab.verification_status})",
                details={"reference_range": lab.reference_range, "verification_status": lab.verification_status},
                severity_or_status="ABNORMAL" if lab.abnormal_flag else "NORMAL"
            ))

        # 7. Ultrasound
        ultrasounds = db.query(UltrasoundRecord).filter(UltrasoundRecord.patient_id == patient_id).all()
        for us in ultrasounds:
            dt = datetime.combine(us.scan_date, datetime.min.time())
            events.append(TimelineEvent(
                timestamp=dt,
                date=us.scan_date.strftime("%Y-%m-%d"),
                event_type="ULTRASOUND",
                title=f"Ultrasound Scan: {us.scan_type}",
                summary=f"Fetal Count: {us.fetal_count}, FHR: {us.fetal_heart_rate or 'N/A'} bpm, Growth: {us.growth_assessment or 'N/A'}",
                details={"impression": us.impression, "placenta": us.placenta_information}
            ))

        # 8. Medications
        medications = db.query(MedicationRecord).filter(MedicationRecord.patient_id == patient_id).all()
        for med in medications:
            dt = datetime.combine(med.start_date, datetime.min.time())
            events.append(TimelineEvent(
                timestamp=dt,
                date=med.start_date.strftime("%Y-%m-%d"),
                event_type="MEDICATION",
                title=f"Prescription: {med.medicine_name}",
                summary=f"{med.medicine_name} {med.dose} ({med.frequency}) for {med.reason or 'obstetric management'}",
                details={"route": med.route, "status": med.status}
            ))

        # 9. Documents
        documents = db.query(Document).filter(Document.patient_id == patient_id).all()
        for doc in documents:
            events.append(TimelineEvent(
                timestamp=doc.upload_date,
                date=doc.upload_date.strftime("%Y-%m-%d"),
                event_type="DOCUMENT",
                title=f"Document Upload: {doc.document_type}",
                summary=f"Verification Status: {doc.verification_status} (Confidence: {int(doc.extraction_confidence * 100)}%)",
                details={"url": doc.file_url, "verified_by": doc.verified_by}
            ))

        # 10. Risk Assessments
        risks = db.query(RiskAssessment).filter(RiskAssessment.patient_id == patient_id).all()
        for r in risks:
            events.append(TimelineEvent(
                timestamp=r.timestamp,
                date=r.timestamp.strftime("%Y-%m-%d"),
                event_type="RISK_ASSESSMENT",
                title=f"AI Risk Pattern Detection: {r.risk_category}",
                summary=f"Risk Level: {r.risk_level} (Score: {r.risk_score}). Clinical Review Status: {r.clinician_review_status}",
                details={"explanation": r.explanation, "contributing_factors": r.contributing_factors},
                severity_or_status=r.risk_level
            ))

        # 11. Referrals
        referrals = db.query(Referral).filter(Referral.patient_id == patient_id).all()
        for ref in referrals:
            events.append(TimelineEvent(
                timestamp=ref.created_at,
                date=ref.created_at.strftime("%Y-%m-%d"),
                event_type="REFERRAL",
                title=f"Emergency Referral: {ref.reason}",
                summary=f"From {ref.source_facility} to {ref.destination_facility or 'TBD'}. Status: {ref.referral_status}",
                details={"risk_level": ref.risk_level, "transport_status": ref.transport_status},
                severity_or_status=ref.referral_status
            ))

        # 12. Deliveries
        deliveries = db.query(Delivery).filter(Delivery.patient_id == patient_id).all()
        for d in deliveries:
            dt = datetime.combine(d.delivery_date, d.delivery_time or datetime.min.time())
            events.append(TimelineEvent(
                timestamp=dt,
                date=d.delivery_date.strftime("%Y-%m-%d"),
                event_type="DELIVERY",
                title=f"Delivery Event: {d.delivery_mode}",
                summary=f"Mode: {d.delivery_mode}, Gestational Age: {d.gestational_age_at_delivery or 'Term'}w, Blood Loss: {d.blood_loss or 'N/A'} mL",
                details={"maternal_complications": d.maternal_complications, "labour_complications": d.labour_complications}
            ))

        # 13. Newborns & Follow-ups
        newborns = db.query(Newborn).filter(Newborn.mother_patient_id == patient_id).all()
        for nb in newborns:
            nb_dt = datetime.combine(nb.date_of_birth, nb.time_of_birth or datetime.min.time())
            events.append(TimelineEvent(
                timestamp=nb_dt,
                date=nb.date_of_birth.strftime("%Y-%m-%d"),
                event_type="NEWBORN_BIRTH",
                title=f"Newborn Birth: {nb.name}",
                summary=f"Sex: {nb.sex}, Birth Weight: {nb.birth_weight}g, APGAR: {nb.apgar_1_min}/{nb.apgar_5_min}",
                details={"breastfeeding": nb.breastfeeding_status, "vaccinations": nb.vaccinations}
            ))
            for nb_visit in nb.visits:
                v_dt = datetime.combine(nb_visit.visit_date, datetime.min.time())
                events.append(TimelineEvent(
                    timestamp=v_dt,
                    date=nb_visit.visit_date.strftime("%Y-%m-%d"),
                    event_type="NEWBORN_FOLLOWUP",
                    title=f"Newborn Follow-up (Day {nb_visit.age_days})",
                    summary=f"Weight: {nb_visit.weight}g, HR: {nb_visit.heart_rate} bpm, Jaundice: {nb_visit.jaundice_observation or 'None'}",
                    details={"activity": nb_visit.activity, "feeding": nb_visit.feeding, "notes": nb_visit.clinician_notes}
                ))

        # 14. Postpartum Visits
        postpartum_visits = db.query(PostpartumVisit).filter(PostpartumVisit.patient_id == patient_id).all()
        for pv in postpartum_visits:
            dt = datetime.combine(pv.visit_date, datetime.min.time())
            events.append(TimelineEvent(
                timestamp=dt,
                date=pv.visit_date.strftime("%Y-%m-%d"),
                event_type="POSTPARTUM_VISIT",
                title=f"Postpartum Visit (Day {pv.postpartum_day})",
                summary=f"BP: {int(pv.systolic_bp or 0)}/{int(pv.diastolic_bp or 0)} mmHg, Lochia: {pv.vaginal_bleeding or 'Normal'}, Mood: {pv.emotional_wellbeing.get('mood', 'Good') if pv.emotional_wellbeing else 'Good'}",
                details={"uterine_status": pv.uterine_status, "wound_status": pv.wound_status, "notes": pv.clinical_notes}
            ))

        # Sort all timeline events chronologically
        events.sort(key=lambda e: e.timestamp)

        return PatientTimelineResponse(
            patient_id=patient_id,
            patient_name=patient.name,
            total_events=len(events),
            timeline=events
        )

    @staticmethod
    def get_patient_summary(db: Session, patient_id: str) -> Optional[PatientSummaryResponse]:
        patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
        if not patient:
            return None

        obs_hist = db.query(ObstetricHistory).filter(ObstetricHistory.patient_id == patient_id).first()
        med_hist = db.query(MedicalHistory).filter(MedicalHistory.patient_id == patient_id).first()
        active_preg = db.query(Pregnancy).filter(
            Pregnancy.patient_id == patient_id,
            Pregnancy.status == "ACTIVE"
        ).order_by(Pregnancy.created_at.desc()).first()

        # Latest observations
        latest_obs = {}
        for obs_name in ["systolic_bp", "diastolic_bp", "pulse", "temperature", "spo2", "fetal_heart_rate", "weight"]:
            rec = db.query(Observation).filter(
                Observation.patient_id == patient_id,
                Observation.observation_type == obs_name
            ).order_by(Observation.timestamp.desc()).first()
            if rec:
                latest_obs[obs_name] = {"value": rec.value, "unit": rec.unit, "timestamp": rec.timestamp.isoformat()}

        recent_symptoms = [
            {"type": s.symptom_type, "severity": s.severity, "date": s.date_time.isoformat()}
            for s in db.query(Symptom).filter(Symptom.patient_id == patient_id).order_by(Symptom.date_time.desc()).limit(5).all()
        ]

        recent_labs = [
            {"test": l.test_name, "result": l.result, "unit": l.unit, "abnormal": l.abnormal_flag, "date": str(l.test_date)}
            for l in db.query(LabResult).filter(LabResult.patient_id == patient_id).order_by(LabResult.test_date.desc()).limit(5).all()
        ]

        latest_risk = db.query(RiskAssessment).filter(RiskAssessment.patient_id == patient_id).order_by(RiskAssessment.timestamp.desc()).first()

        active_referrals = db.query(Referral).filter(
            Referral.patient_id == patient_id,
            Referral.referral_status.notin_(["COMPLETED", "CANCELLED"])
        ).all()

        verified_docs_count = db.query(Document).filter(
            Document.patient_id == patient_id,
            Document.verification_status == "VERIFIED"
        ).count()

        latest_delivery = db.query(Delivery).filter(Delivery.patient_id == patient_id).order_by(Delivery.delivery_date.desc()).first()
        newborns = db.query(Newborn).filter(Newborn.mother_patient_id == patient_id).all()

        latest_pp = db.query(PostpartumVisit).filter(PostpartumVisit.patient_id == patient_id).order_by(PostpartumVisit.visit_date.desc()).first()
        latest_pp_data = None
        if latest_pp:
            latest_pp_data = {
                "postpartum_day": latest_pp.postpartum_day,
                "visit_date": str(latest_pp.visit_date),
                "bp": f"{int(latest_pp.systolic_bp or 0)}/{int(latest_pp.diastolic_bp or 0)}",
                "uterine_status": latest_pp.uterine_status,
                "lochia": latest_pp.vaginal_bleeding
            }

        return PatientSummaryResponse(
            patient_id=patient_id,
            demographics=PatientResponse.model_validate(patient),
            obstetric_history=ObstetricHistoryResponse.model_validate(obs_hist) if obs_hist else None,
            medical_history=MedicalHistoryResponse.model_validate(med_hist) if med_hist else None,
            current_pregnancy=PregnancyResponse.model_validate(active_preg) if active_preg else None,
            gestational_age_weeks=active_preg.gestational_age if active_preg else None,
            latest_observations=latest_obs,
            recent_symptoms=recent_symptoms,
            recent_labs=recent_labs,
            latest_risk_assessment=RiskAssessmentResponse.model_validate(latest_risk) if latest_risk else None,
            active_referrals=[ReferralResponse.model_validate(r) for r in active_referrals],
            verified_documents_count=verified_docs_count,
            delivery_status="DELIVERED" if latest_delivery else ("PREGNANT" if active_preg else "NON_PREGNANT"),
            delivery_record=DeliveryResponse.model_validate(latest_delivery) if latest_delivery else None,
            newborns=[NewbornResponse.model_validate(n) for n in newborns],
            latest_postpartum_visit=latest_pp_data
        )


timeline_service = TimelineService()
