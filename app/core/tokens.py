from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 15

def create_reset_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES),
        "type": "password_reset",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_reset_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "password_reset":
            return None
        return int(payload["sub"])
    except Exception:
        return None
