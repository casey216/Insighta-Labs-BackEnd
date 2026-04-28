import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError

from app.core.settings import settings


ALGORITHM = "HS256"


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=3)
    }

    return jwt.encode(
        claims=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_refresh_token() -> tuple[str, str]:
    raw = secrets.token_urlsafe(32)
    hashed = hashlib.sha256(raw.encode()).hexdigest()
    return raw, hashed


def verify_access_token(token: str | None) -> tuple[dict | None, str | None]:
    if not token:
        return None, "Token Missing"

    try:
        return jwt.decode(
            token=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[ALGORITHM],
        ), None
    except ExpiredSignatureError:
        return None, "Signature Expired"
    except JWTError:
        return None, "Invalid Token"
