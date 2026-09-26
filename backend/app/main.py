from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.core.database import engine, Base
import app.models  # Ensure all models are registered with Base metadata

from app.api.routes import (
    auth_router,
    patients_router,
    pregnancies_router,
    visits_router,
    observations_router,
    symptoms_router,
    labs_router,
    ultrasounds_router,
    medications_router,
    documents_router,
    deliveries_router,
    newborns_router,
    postpartum_router,
    risk_router,
    referrals_router,
    facilities_router,
    communications_router,
    audit_router,
    timeline_router,
    voice_router
)
from app.medical_brain import medical_brain_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("maternacare")

# Initialize database schema tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal healthcare service error occurred. Please contact the clinical administrator."}
    )


# Register API v1 Routers
api_v1 = settings.API_V1_STR
app.include_router(auth_router, prefix=api_v1)
app.include_router(patients_router, prefix=api_v1)
app.include_router(pregnancies_router, prefix=api_v1)
app.include_router(visits_router, prefix=api_v1)
app.include_router(observations_router, prefix=api_v1)
app.include_router(symptoms_router, prefix=api_v1)
app.include_router(labs_router, prefix=api_v1)
app.include_router(ultrasounds_router, prefix=api_v1)
app.include_router(medications_router, prefix=api_v1)
app.include_router(documents_router, prefix=api_v1)
app.include_router(deliveries_router, prefix=api_v1)
app.include_router(newborns_router, prefix=api_v1)
app.include_router(postpartum_router, prefix=api_v1)
app.include_router(risk_router, prefix=api_v1)
app.include_router(referrals_router, prefix=api_v1)
app.include_router(facilities_router, prefix=api_v1)
app.include_router(communications_router, prefix=api_v1)
app.include_router(audit_router, prefix=api_v1)
app.include_router(timeline_router, prefix=api_v1)
app.include_router(voice_router, prefix=api_v1)
app.include_router(medical_brain_router, prefix=api_v1)


@app.get("/", tags=["Root"])
def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "OPERATIONAL",
        "docs_url": "/docs",
        "voice_pipeline": "ACTIVE",
        "supported_languages": settings.VOICE_SUPPORTED_LANGUAGES,
        "ethical_notice": (
            "This is a clinical decision-support and communication intelligence system. "
            "AI does not provide autonomous medical diagnosis. All patterns require clinical review."
        )
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "maternacare-backend"}

from pydantic import BaseModel
class ChatRequest(BaseModel):
    message: str
    patient_id: str = "PAT-DEMO"
    language: str = "en"
    source_lang: str = "en"

@app.post("/api/chat", tags=["Frontend Integration"])
def chat_endpoint(req: ChatRequest):
    """
    Hooks the Next.js frontend directly into the Core Medical Brain (Model 4)
    and the Emergency Guardian (Model 3).
    """
    from app.ai_models.orchestrator import voice_orchestrator
    
    # Process the query using the orchestrator
    res = voice_orchestrator.process_consultation(
        text_query=req.message,
        language_hint=req.language
    )
    
    status = res.get("status")
    requires_approval = False
    proposed_advice = None
    response_text = ""
    
    target_lang = (req.language or "en").lower().split("-")[0]

    if status == "EMERGENCY_DISPATCHED":
        response_text = "EMERGENCY DETECTED. An ambulance has been dispatched to your location immediately."
    elif status == "PENDING_DOCTOR_APPROVAL":
        requires_approval = True
        proposed_advice = res.get("proposedAdvice") or res.get("medical_advice_text", "Prescription requires review.")
        response_text = res.get("patient_friendly_text") or "Since you are asking about medication, I have forwarded your request to your doctor for review. After I get approval from the doctor, I will suggest you the tablet."
    else:
        response_text = res.get("patient_friendly_text", "I'm here to help you.")

    audio_b64 = res.get("audio_response_base64")

    # If audio is not yet synthesized (e.g. approval or emergency), synthesize it now in target language!
    if not audio_b64 and response_text:
        try:
            # If target language is non-English, translate response_text first
            if target_lang not in ["en", "english"]:
                import os, dotenv
                dotenv.load_dotenv()
                groq_k = os.environ.get("GROQ_API_KEY", "")
                if groq_k:
                    from groq import Groq
                    gc = Groq(api_key=groq_k)
                    comp = gc.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[{
                            "role": "system",
                            "content": f"Translate into language code '{target_lang}'. Return ONLY native script direct translation."
                        }, {"role": "user", "content": response_text}],
                        temperature=0.2,
                        max_tokens=150
                    )
                    trans = comp.choices[0].message.content.strip()
                    if trans:
                        response_text = trans

            from app.ai_models.tts_model import tts_engine
            synth = tts_engine.synthesize(text=response_text, language=target_lang)
            audio_b64 = synth.get("audio_base64")
        except Exception as e:
            pass
        
    return {
        "success": True,
        "response": response_text,
        "status": status,
        "requiresApproval": requires_approval,
        "proposedAdvice": proposed_advice,
        "source": "maternacare_core_brain",
        "audio_base64": audio_b64,
        "audio_format": res.get("audio_format", "audio/mp3")
    }
