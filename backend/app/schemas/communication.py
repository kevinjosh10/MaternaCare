from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CommunicationBase(BaseModel):
    referral_id: Optional[str] = None
    channel: str = Field(..., example="SMS")  # SMS, VOICE, TTS, PHONE, IN_APP
    recipient: str = Field(..., example="+91 9876543210")
    language: str = Field("hi", example="hi")
    message: str = Field(..., example="MaternaCare Emergency Alert: Patient referral initiated. Ambulance requested.")
    message_type: str = Field("REFERRAL_ALERT", example="REFERRAL_ALERT")


class CommunicationCreate(CommunicationBase):
    pass


class CommunicationResponse(CommunicationBase):
    communication_id: str
    created_at: datetime
    sent_at: Optional[datetime] = None
    delivery_status: str
    acknowledgement_status: str
    provider_reference: Optional[str] = None

    class Config:
        from_attributes = True
