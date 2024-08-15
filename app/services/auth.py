import os
from datetime import timedelta, datetime, UTC
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException

from ..schemas.auth import TokenPairSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "i9i3902849209323m009sfhs90dh")
ALGORITHM = "HS256"
USER_IDENTIFIER = "user_id"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_HOURS = 24 * 30


def create_jwt_token_pair(user_id: int) -> TokenPairSchema:
    """Создает пару токенов (рефреш + аксесс)"""

    access_token = _create_jwt_token(
        {USER_IDENTIFIER: user_id, "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = _create_jwt_token(
        {USER_IDENTIFIER: user_id, "type": "refresh"},
        timedelta(minutes=REFRESH_TOKEN_EXPIRE_HOURS)
    )
    return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)


def refresh_access_token(refresh_token: str) -> str:
    """Создать новый аксесс токен на основе рефреш токена"""
    payload = _get_token_payload(refresh_token, "refresh")

    return _create_jwt_token(
        {USER_IDENTIFIER: payload[USER_IDENTIFIER], "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def _create_jwt_token(data: dict, delta: timedelta):
    expires_delta = datetime.now(UTC) + delta
    data.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def _get_token_payload(token: str, token_type: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("type") != token_type:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload.get(USER_IDENTIFIER) is None:
        raise HTTPException(status_code=401, detail="Cloud not validate credentials")

    return payload
