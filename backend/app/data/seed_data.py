import csv
import os
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.patient import Patient
from app.models.history import ObstetricHistory, MedicalHistory
from app.models.pregnancy import Pregnancy
from app.models.visit import AntenatalVisit
from app.models.observation import Observation
from app.models.symptom import Symptom
from app.models.lab import LabResult
from app.models.ultrasound import UltrasoundRecord
from app.models.medication import MedicationRecord, SupplementRecord, VaccinationRecord
from app.models.delivery import Delivery
from app.models.newborn import Newborn, NewbornVisit
from app.models.postpartum import PostpartumVisit
from app.models.facility import Facility
from app.models.referral import Referral
from app.core.security import get_password_hash


def seed_database():
    """
    Seeds database with test/demo data clearly labeled as synthetic.
    Never represented as real patient clinical data.
    """
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # 1. Seed Authorized Healthcare Users & Roles
        if not db.query(User).filter(User.username == "doctor_priya").first():
            db.add(User(
                username="doctor_priya",
                email="priya.patel@maternacare.org",
                hashed_password=get_password_hash("DoctorPass@123"),
                full_name="Dr. Priya Patel (Senior Obstetrician)",
                role=UserRole.DOCTOR.value,
                is_active=True
            ))
            db.add(User(
                username="anm_rekha",
                email="rekha.devi@maternacare.org",
                hashed_password=get_password_hash("WorkerPass@123"),
                full_name="Rekha Devi (Auxiliary Nurse Midwife)",
                role=UserRole.MIDWIFE.value,
                is_active=True
            ))
            db.add(User(
                username="admin_materna",
                email="admin@maternacare.org",
                hashed_password=get_password_hash("AdminPass@123"),
                full_name="System Clinical Administrator",
                role=UserRole.ADMIN.value,
                is_active=True
            ))
            db.commit()
            print("Users and roles seeded.")

        # 2. Seed Facility
        facility = db.query(Facility).filter(Facility.name.like("%District Women%")).first()
        if not facility:
            facility = Facility(
                name="District Women's & Children's Referral Hospital",
                type="DISTRICT_HOSPITAL",
                address="Pandeypur Main Road",
                district="Varanasi",
                state="Uttar Pradesh",
                latitude=25.3350,
                longitude=82.9912,
                phone="+91 542 2501234",
                emergency_phone="108",
                services=["24x7 Emergency C-Section", "Blood Bank", "SNCU Level 2", "High Dependency Unit"],
                specialties=["OBGYN", "PEDIATRICS", "ANESTHESIOLOGY"],
                operating_status="ACTIVE"
            )
            db.add(facility)
            db.commit()
            db.refresh(facility)
            print("Referral Facility seeded.")

        # 3. Seed Patient: Sunita Devi
        patient_id = "PAT-IN-2026-001"
        patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
        if not patient:
            patient = Patient(
                patient_id=patient_id,
                name="Sunita Devi",
                date_of_birth=date(2001, 4, 15),
                age=24,
                sex="Female",
                phone="+91 9876543210",
                address="House #42, Village Arajiline",
                district="Varanasi",
                state="Uttar Pradesh",
                preferred_language="hi",
                emergency_contact={"name": "Ramesh Kumar", "relation": "Husband", "phone": "+91 9876543211"},
                blood_group="B+",
                occupation="Homemaker",
                education="Higher Secondary",
                marital_status="Married"
            )
            db.add(patient)
            db.commit()
            print(f"Patient {patient.name} seeded.")

        # 4. Obstetric & Medical History
        if not db.query(ObstetricHistory).filter(ObstetricHistory.patient_id == patient_id).first():
            db.add(ObstetricHistory(
                patient_id=patient_id,
                previous_pregnancies=1,
                previous_live_births=1,
                previous_abortions=0,
                previous_stillbirths=0,
                previous_c_sections=0,
                previous_vaginal_deliveries=1,
                previous_preeclampsia=False,
                previous_gestational_diabetes=False,
                previous_postpartum_haemorrhage=False,
                complications_details=[{"year": 2022, "outcome": "Full term normal vaginal delivery", "birth_weight_kg": 2.9}]
            ))
            db.add(MedicalHistory(
                patient_id=patient_id,
                chronic_conditions=[],
                previous_surgeries=[],
                allergies=["No known drug allergies (NKDA)"],
                family_history=["Maternal hypertension"]
            ))
            db.commit()
            print("Obstetric and Medical history seeded.")

        # 5. Pregnancy
        pregnancy_id = "PREG-2026-001"
        pregnancy = db.query(Pregnancy).filter(Pregnancy.pregnancy_id == pregnancy_id).first()
        if not pregnancy:
            pregnancy = Pregnancy(
                pregnancy_id=pregnancy_id,
                patient_id=patient_id,
                pregnancy_number=2,
                gravida=2,
                para=1,
                living_children=1,
                abortion_count=0,
                stillbirth_count=0,
                last_menstrual_period=date(2024, 12, 1),
                estimated_due_date=date(2025, 9, 8),
                gestational_age=39.4,
                pregnancy_type="Spontaneous",
                singleton_or_multiple="Singleton",
                pregnancy_start_date=date(2024, 12, 1),
                high_risk_flag=True,
                high_risk_reason="Gestational hypertension at 32 weeks, controlled on Labetalol",
                status="DELIVERED"
            )
            db.add(pregnancy)
            db.commit()
            print(f"Pregnancy {pregnancy_id} seeded.")

        # 6. Parse and Seed Months 1-10 Pregnancy CSV
        csv_path = os.path.join(os.path.dirname(__file__), "maternacare_pregnancy_months_1_to_10_longitudinal_data.csv")
        if os.path.exists(csv_path):
            with open(csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    v_date = datetime.strptime(row["visit_date"], "%Y-%m-%d").date()
                    v_time = datetime.combine(v_date, datetime.min.time())

                    # Add ANC visit
                    if row["systolic_bp_mmHg"]:
                        anc = AntenatalVisit(
                            pregnancy_id=pregnancy_id,
                            patient_id=patient_id,
                            visit_date=v_date,
                            gestational_age=float(row["gestational_age_weeks"]),
                            weight=float(row["weight_kg"]) if row["weight_kg"] else None,
                            systolic_bp=float(row["systolic_bp_mmHg"]) if row["systolic_bp_mmHg"] else None,
                            diastolic_bp=float(row["diastolic_bp_mmHg"]) if row["diastolic_bp_mmHg"] else None,
                            pulse=float(row["pulse_bpm"]) if row["pulse_bpm"] else None,
                            temperature=float(row["temperature_C"]) if row["temperature_C"] else None,
                            fetal_heart_rate=float(row["fetal_heart_rate_bpm"]) if row["fetal_heart_rate_bpm"] else None,
                            fundal_height=float(row["fundal_height_cm"]) if row["fundal_height_cm"] else None,
                            fetal_movement=row["fetal_movement"] or "Normal",
                            urine_findings={"protein": row["urine_protein"], "sugar": row["urine_sugar"]},
                            symptoms=[s.strip() for s in row["reported_symptoms"].split(",") if s.strip() and s.strip() != "None"],
                            warning_signs=[w.strip() for w in row["warning_signs"].split(",") if w.strip() and w.strip() != "None"],
                            clinical_notes=row["clinical_notes"],
                            healthcare_worker="Dr. Priya Patel",
                            facility="District Referral Centre"
                        )
                        db.add(anc)

                        # Add Time-Series Observations
                        db.add(Observation(
                            patient_id=patient_id,
                            pregnancy_id=pregnancy_id,
                            timestamp=v_time,
                            observation_type="systolic_bp",
                            value=float(row["systolic_bp_mmHg"]),
                            unit="mmHg",
                            source="ANC_VISIT",
                            verified=True,
                            recorded_by="Dr. Priya Patel"
                        ))
                        db.add(Observation(
                            patient_id=patient_id,
                            pregnancy_id=pregnancy_id,
                            timestamp=v_time,
                            observation_type="diastolic_bp",
                            value=float(row["diastolic_bp_mmHg"]),
                            unit="mmHg",
                            source="ANC_VISIT",
                            verified=True,
                            recorded_by="Dr. Priya Patel"
                        ))

                    # Add Lab result
                    if row["lab_test_name"]:
                        db.add(LabResult(
                            patient_id=patient_id,
                            pregnancy_id=pregnancy_id,
                            test_date=v_date,
                            test_name=row["lab_test_name"],
                            test_category="HEMATOLOGY",
                            result=row["lab_test_result"],
                            unit="g/dL" if "Hb" in row["lab_test_name"] else "",
                            abnormal_flag=row["lab_abnormal_flag"].lower() == "true",
                            lab_name="District Hospital Pathology Lab",
                            verified_by="Dr. Priya Patel",
                            verification_status="VERIFIED"
                        ))

                    # Add Ultrasound
                    if row["ultrasound_type"]:
                        db.add(UltrasoundRecord(
                            pregnancy_id=pregnancy_id,
                            patient_id=patient_id,
                            scan_date=v_date,
                            gestational_age=float(row["gestational_age_weeks"]),
                            scan_type=row["ultrasound_type"],
                            findings=row["ultrasound_findings"],
                            impression="Normal interval progression",
                            verification_status="VERIFIED",
                            verified_by="Dr. Priya Patel"
                        ))
            db.commit()
            print("1-to-10 month pregnancy longitudinal data seeded.")

        # 7. Delivery
        delivery_id = "DELIV-2026-001"
        if not db.query(Delivery).filter(Delivery.delivery_id == delivery_id).first():
            db.add(Delivery(
                delivery_id=delivery_id,
                pregnancy_id=pregnancy_id,
                patient_id=patient_id,
                delivery_date=date(2025, 9, 10),
                facility="District Women's & Children's Referral Hospital",
                delivery_mode="SPONTANEOUS_VAGINAL",
                gestational_age_at_delivery=39.4,
                labour_complications=[],
                maternal_complications=["Episiotomy 2nd degree sutured"],
                blood_loss=250.0,
                post_delivery_vitals={"systolic_bp": 128, "diastolic_bp": 82, "pulse": 78},
                clinical_notes="Live term birth. Baby cried vigorously immediately after delivery."
            ))
            db.commit()
            print("Delivery record seeded.")

        # 8. Newborn
        newborn_id = "NB-2026-001"
        if not db.query(Newborn).filter(Newborn.newborn_id == newborn_id).first():
            db.add(Newborn(
                newborn_id=newborn_id,
                mother_patient_id=patient_id,
                pregnancy_id=pregnancy_id,
                delivery_id=delivery_id,
                name="Baby Aarav Kumar",
                sex="Male",
                date_of_birth=date(2025, 9, 10),
                gestational_age=39.4,
                birth_weight=3150.0,
                birth_length=49.5,
                head_circumference=34.0,
                apgar_1_min=8,
                apgar_5_min=9,
                delivery_status="LIVE_BIRTH",
                resuscitation_required=False,
                feeding_started=True,
                breastfeeding_status="EXCLUSIVE_BREASTFEEDING",
                vaccinations=["BCG", "OPV-0", "Hepatitis B (Birth Dose)"],
                clinical_notes="Healthy male neonate. Excellent reflexes."
            ))
            db.commit()
            print("Newborn record seeded.")

        # 9. 1-Year Mother Postpartum CSV Seed
        mother_pnc_csv = os.path.join(os.path.dirname(__file__), "maternacare_mother_1_year_postpartum_data.csv")
        if os.path.exists(mother_pnc_csv):
            with open(mother_pnc_csv, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pv_date = datetime.strptime(row["visit_date"], "%Y-%m-%d").date()
                    db.add(PostpartumVisit(
                        patient_id=patient_id,
                        delivery_id=delivery_id,
                        visit_date=pv_date,
                        postpartum_day=int(row["postpartum_day_number"]),
                        systolic_bp=float(row["systolic_bp_mmHg"]),
                        diastolic_bp=float(row["diastolic_bp_mmHg"]),
                        pulse=float(row["pulse_bpm"]),
                        temperature=float(row["temperature_C"]),
                        weight=float(row["maternal_weight_kg"]),
                        vaginal_bleeding=row["vaginal_bleeding_lochia"],
                        uterine_status=row["uterine_involution_status"],
                        wound_status=row["perineal_or_surgical_wound_status"],
                        pain=f"Scale {row['pain_scale_0_to_10']}/10",
                        headache=row["headache_or_vision_changes"],
                        urinary_status=row["urinary_and_bowel_function"],
                        breastfeeding=row["breastfeeding_and_lactation"],
                        breast_symptoms=row["breast_examination_findings"],
                        medications=[row["prescribed_medications_and_supplements"]],
                        emotional_wellbeing={"epds_score": int(row["epds_depression_score"]), "notes": row["emotional_wellbeing_and_bonding"]},
                        clinical_notes=row["clinical_notes_and_guidance"]
                    ))
            db.commit()
            print("1-year mother postpartum data seeded.")

        # 10. 1-Year Newborn Follow-up CSV Seed
        nb_csv = os.path.join(os.path.dirname(__file__), "maternacare_newborn_1_year_growth_followup_data.csv")
        if os.path.exists(nb_csv):
            with open(nb_csv, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    nb_date = datetime.strptime(row["visit_date"], "%Y-%m-%d").date()
                    db.add(NewbornVisit(
                        newborn_id=newborn_id,
                        visit_date=nb_date,
                        age_days=int(row["age_days"]),
                        weight=float(row["weight_grams"]),
                        length=float(row["length_cm"]),
                        head_circumference=float(row["head_circumference_cm"]),
                        heart_rate=float(row["heart_rate_bpm"]),
                        respiratory_rate=float(row["respiratory_rate_bpm"]),
                        temperature=float(row["temperature_C"]),
                        oxygen_saturation=float(row["spo2_percent"]),
                        feeding=row["feeding_status"],
                        urination=row["urination_frequency"],
                        stool=row["stool_characteristics"],
                        jaundice_observation=row["jaundice_observation"],
                        vaccinations=[v.strip() for v in row["vaccines_administered"].split(",") if v.strip() and v.strip() != "None"],
                        developmental_observations=[m.strip() for m in row["developmental_milestones"].split(";") if m.strip()],
                        clinical_findings=[row["clinical_findings"]],
                        clinician_notes=row["clinician_notes"]
                    ))
            db.commit()
            print("1-year newborn follow-up growth data seeded.")

        print("=== MATERNACARE DATABASE SEEDING COMPLETED SUCCESSFULLY ===")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
