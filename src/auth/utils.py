import uuid
from datetime import datetime, timedelta, timezone

import jwt
from passlib import context
from fastapi import HTTPException, status   

from src.config import settings

ACCESS_TOKEN_EXPIRY_SECONDS = 60 * 60 # 1 hour
_password_context = context.CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return _password_context.hash(password)

 
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password."""
    return _password_context.verify(plain_password, hashed_password)


def create_access_token(claims: dict, expiry: timedelta = None, refresh_token: bool = False) -> str:
    payload = {
        "user": claims,
        "exp": datetime.now(timezone.utc) + (expiry or timedelta(minutes=ACCESS_TOKEN_EXPIRY_SECONDS)),
        "jti": str(uuid.uuid4()),
        "refresh_token": refresh_token
    }
    token = jwt.encode(
        payload, settings.JWT_SECRET, settings.JWT_ALGORITHM
    )
    return token


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError as jwe:
        print(f"Token has expired: {jwe}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError as jwe:
        print(f"Invalid token : {jwe}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")