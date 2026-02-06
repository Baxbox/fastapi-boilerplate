from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models.user import User
from app.core.tokens import create_reset_token, verify_reset_token
from app.core.security import hash_password
from app.services.email_service import send_password_reset_email

def request_password_reset(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return  # Always silent

    token = create_reset_token(user.id)
    reset_link = f"https://yourapp.com/reset-password?token={token}"
    send_password_reset_email(user.email, reset_link)

def reset_password(token: str, new_password: str, db: Session) -> bool:
    user_id = verify_reset_token(token)
    if not user_id:
        return False

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False

    user.hashed_password = hash_password(new_password)
    db.commit()
    return True

def login_user(email: str, password: str, db: Session) -> str:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    return access_token