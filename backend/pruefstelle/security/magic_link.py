import secrets
from uuid import UUID
from datetime import timedelta
from typing import Optional

from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, ValidationError
from jose import JWTError, jwt
from passlib.context import CryptContext

from .token import create_access_token, SECRET_KEY, ALGORITHM
from ..database import crud
from .. import database


EXPIRES_AFTER_MINUTES = 15
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class MagicLink(BaseModel):
    value: str
    email: EmailStr


def create_link_token(session: Session, user_id: UUID, email: EmailStr) -> str:
    value = create_link_value()
    store_link_value(session, user_id, value)
    data = dict(value=value, email=email)
    expires = timedelta(minutes=EXPIRES_AFTER_MINUTES)
    return create_access_token(data, expires_delta=expires)


def create_link_value() -> str:
    """Create magic link secret (86 characters)"""
    return secrets.token_urlsafe(64)


def store_link_value(session: Session, user_id: UUID, value: str):
    crud.delete_link(session, user_id)
    hashed_value = pwd_context.hash(value)
    crud.create_link_value(session, user_id, hashed_value)


def verify_link_value(value: str, hashed: str) -> bool:
    return pwd_context.verify(value, hashed)


def authenticate_link_value(session: Session, user_id: UUID, value: str) -> bool:
    crud.delete_old_links(session, expires_after_minutes=EXPIRES_AFTER_MINUTES)
    hashed = crud.get_link(session, user_id)
    if hashed is None:
        return False
    crud.delete_link(session, user_id)
    return verify_link_value(value, str(hashed.value))


def authenticate_by_link(session: Session, token: str) -> Optional[database.User]:
    try:
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        value: str = payload.get("value")  # type: ignore
        email: EmailStr = payload.get("email")  # type: ignore
        token_data = MagicLink(value=value, email=email)
    except (JWTError, ValidationError):
        return None
    if token_data.value is None or token_data.email is None:
        return None
    user = crud.get_user_by_email(session, token_data.email)
    if user is None:
        return None
    authenticated = authenticate_link_value(session, user_id=user.id, value=token_data.value)  # type: ignore
    if authenticated is False:
        return None
    return user
