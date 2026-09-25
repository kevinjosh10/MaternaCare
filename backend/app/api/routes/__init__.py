from app.api.routes.auth import router as auth_router
from app.api.routes.patients import router as patients_router
from app.api.routes.pregnancies import router as pregnancies_router
from app.api.routes.visits import router as visits_router
from app.api.routes.observations import router as observations_router
from app.api.routes.symptoms import router as symptoms_router
from app.api.routes.labs import router as labs_router
from app.api.routes.ultrasounds import router as ultrasounds_router
from app.api.routes.medications import router as medications_router
from app.api.routes.documents import router as documents_router
from app.api.routes.deliveries import router as deliveries_router
from app.api.routes.newborns import router as newborns_router
from app.api.routes.postpartum import router as postpartum_router
from app.api.routes.risk import router as risk_router
from app.api.routes.referrals import router as referrals_router
from app.api.routes.facilities import router as facilities_router
from app.api.routes.communications import router as communications_router
from app.api.routes.audit import router as audit_router
from app.api.routes.timeline import router as timeline_router
from app.api.routes.voice import router as voice_router

__all__ = [
    "auth_router",
    "patients_router",
    "pregnancies_router",
    "visits_router",
    "observations_router",
    "symptoms_router",
    "labs_router",
    "ultrasounds_router",
    "medications_router",
    "documents_router",
    "deliveries_router",
    "newborns_router",
    "postpartum_router",
    "risk_router",
    "referrals_router",
    "facilities_router",
    "communications_router",
    "audit_router",
    "timeline_router",
    "voice_router"
]
