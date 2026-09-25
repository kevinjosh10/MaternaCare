from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    username: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    role: str = "HEALTH_WORKER"
    facility_id: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    role: str
    facility_id: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True
