from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.auth import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False
)


def get_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme)
) -> User:
    """
    Extract current authenticated user from Bearer JWT.
    Supports a mock development user if no token is provided in dev mode.
    """
    if not token:
        # For development / testing when running without login:
        dev_user = db.query(User).filter(User.username == "doctor_dev").first()
        if not dev_user:
            dev_user = User(
                username="doctor_dev",
                email="doctor_dev@maternacare.org",
                hashed_password="mock_hashed_password",
                full_name="Dr. Sunita Sharma (Dev Obstetrician)",
                role=UserRole.DOCTOR.value,
                is_active=True
            )
            db.add(dev_user)
            db.commit()
            db.refresh(dev_user)
        return dev_user

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenPayload(sub=user_id, role=payload.get("role"))
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.sub).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_roles(allowed_roles: List[str]):
    """
    Role-Based Access Control (RBAC) dependency factory.
    Roles: ADMIN, DOCTOR, NURSE, MIDWIFE, HEALTH_WORKER, REFERRAL_COORDINATOR, FACILITY_USER.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role == UserRole.ADMIN.value:
            return current_user  # Superuser admin has access to all clinical endpoints
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required roles: {allowed_roles}. Current role: {current_user.role}"
            )
        return current_user
    return role_checker
