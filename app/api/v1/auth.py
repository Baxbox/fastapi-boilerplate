from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    LoginRequest,
)
from app.services.auth_service import (
    request_password_reset,
    reset_password,
    login_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    access_token = login_user(data.email, data.password, db)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    request_password_reset(data.email, db)
    return {"message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password")
def reset_password_endpoint(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    success = reset_password(data.token, data.new_password, db)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"message": "Password updated successfully"}
