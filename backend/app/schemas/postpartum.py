from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, Field


class PostpartumVisitBase(BaseModel):
    patient_id: str
    delivery_id: Optional[str] = None
    visit_date: date
    postpartum_day: int = Field(..., example=3)
    systolic_bp: Optional[float] = Field(None, example=120.0)
    diastolic_bp: Optional[float] = Field(None, example=78.0)
    pulse: Optional[float] = Field(None, example=78.0)
    temperature: Optional[float] = Field(None, example=36.7)
    weight: Optional[float] = Field(None, example=58.0)
    vaginal_bleeding: Optional[str] = Field("Lochia Rubra (moderate, normal)", example="Lochia Rubra")
    uterine_status: Optional[str] = Field("Firm, well-contracted below umbilicus", example="Well contracted")
    wound_status: Optional[str] = Field("Perineum intact/healing, no discharge", example="Healing well")
    pain: Optional[str] = Field("Mild cramping during feeds", example="Mild")
    headache: Optional[str] = Field("None", example="None")
    urinary_status: Optional[str] = Field("Normal, no burning", example="Normal")
    bowel_status: Optional[str] = Field("Bowels opened normally", example="Normal")
    breastfeeding: Optional[str] = Field("Exclusive breastfeeding established", example="Established")
    breast_symptoms: Optional[str] = Field("Soft, non-tender, no engorgement", example="Normal")
    medications: List[str] = ["Iron-Folic Acid", "Calcium D3"]
    nutrition: Optional[str] = Field("Nutritious warm diet, adequate fluids", example="Adequate")
    sleep: Optional[str] = Field("6 hours intermittent with baby feeds", example="6 hours")
    emotional_wellbeing: Dict[str, Any] = {"mood": "Good", "anxiety": "None", "support": "Family present"}
    clinical_notes: Optional[str] = None


class PostpartumVisitCreate(PostpartumVisitBase):
    pass


class PostpartumVisitResponse(PostpartumVisitBase):
    visit_id: str
    created_at: datetime

    class Config:
        from_attributes = True
