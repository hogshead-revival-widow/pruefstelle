from datetime import datetime, timedelta
from typing import Optional

from fastapi import Response
from pydantic import BaseModel, EmailStr
from fastapi.security import APIKeyCookie
from jose import jwt


from ..config import settings
from .. import schemas

SECRET_KEY = settings.security.secret_key  # type: ignore
ALGORITHM = settings.security.algorithm  # type: ignore
TOKEN_EXPIRES = settings.security.access_token_expires_seconds  # type: ignore
COOKIE_NAME = "jwt"
COOKIE_EXPIRES = TOKEN_EXPIRES

cookie_sec = APIKeyCookie(name=COOKIE_NAME)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[EmailStr]


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRES)  # type: ignore
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore
    return encoded_jwt


async def set_cookie(response: Response, user: schemas.UserRead):
    access_token = create_access_token(data={"sub": user.email})

    response.set_cookie(
        COOKIE_NAME,
        access_token,
        max_age=COOKIE_EXPIRES,
        expires=COOKIE_EXPIRES,
        httponly=True,
        # secure=True,
        samesite="lax",
    )
