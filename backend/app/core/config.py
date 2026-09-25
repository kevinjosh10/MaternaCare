from typing import List, Union
import json
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "MaternaCare — Maternal & Neonatal Health Intelligence"
    PROJECT_DESCRIPTION: str = (
        "AI-Powered Maternal & Neonatal Continuity, Risk & Emergency Referral Intelligence "
        "with Multilingual Voice-to-Voice Pregnancy AI Model Pipeline."
    )
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "maternacare-super-secret-jwt-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Database
    DATABASE_URL: str = "sqlite:///./maternacare.db"
    SQLITE_FALLBACK: bool = True

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str):
            return json.loads(v)
        return v

    # Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 25

    # Voice & AI Engine Settings
    VOICE_SUPPORTED_LANGUAGES: List[str] = [
        "en", "hi", "ta", "te", "kn", "bn", "mr", "gu", "ml", "es", "fr", "sw"
    ]
    DEFAULT_VOICE_LANGUAGE: str = "en"
    VOICE_SAMPLE_RATE: int = 16000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )


settings = Settings()
