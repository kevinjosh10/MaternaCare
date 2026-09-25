import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    assessment_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False, index=True)
    pregnancy_id = Column(String(36), ForeignKey("pregnancies.pregnancy_id", ondelete="CASCADE"), nullable=True, index=True)
    newborn_id = Column(String(36), ForeignKey("newborns.newborn_id", ondelete="CASCADE"), nullable=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    model_version = Column(String(50), default="maternacare-risk-engine-v1.0")
    risk_category = Column(String(100), nullable=False)
    # e.g., PREECLAMPSIA, GESTATIONAL_DIABETES, PRETERM_LABOUR, FETAL_GROWTH_RESTRICTION, PPH, NEONATAL_SEPSIS, GENERAL_OBSTETRIC
    risk_score = Column(Float, nullable=False)  # 0.0 to 1.0
    risk_level = Column(String(50), nullable=False, index=True)  # LOW, MODERATE, HIGH, CRITICAL
    input_snapshot = Column(JSON, default=dict)
    contributing_factors = Column(JSON, default=list)
    trend_features = Column(JSON, default=dict)
    explanation = Column(
        Text,
        default="Potentially concerning pattern detected — clinical review recommended.",
        nullable=False
    )
    clinician_review_status = Column(String(50), default="PENDING_REVIEW")  # PENDING_REVIEW, REVIEWED_AGREED, REVIEWED_DISAGREED, OVERRIDDEN
    clinician_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    patient = relationship("Patient", back_populates="risk_assessments")
    pregnancy = relationship("Pregnancy", back_populates="risk_assessments")
    explanations = relationship("ExplanationFeature", back_populates="assessment", cascade="all, delete-orphan")


class ExplanationFeature(Base):
    __tablename__ = "explanation_features"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String(36), ForeignKey("risk_assessments.assessment_id", ondelete="CASCADE"), nullable=False, index=True)
    feature = Column(String(100), nullable=False)  # e.g., "systolic_bp_trajectory", "urine_protein", "gestational_age"
    feature_value = Column(String(100), nullable=False)  # e.g., "150 mmHg", "++", "32 weeks"
    contribution = Column(Float, nullable=False)  # SHAP value / contribution weight
    direction = Column(String(20), nullable=False)  # "INCREASE_RISK", "DECREASE_RISK"
    rank = Column(Integer, nullable=False)  # Rank 1, 2, 3 in feature importance

    assessment = relationship("RiskAssessment", back_populates="explanations")
