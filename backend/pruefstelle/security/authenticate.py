from typing import Callable, Optional, Union, Tuple


from fastapi import Depends, HTTPException, Request
from pydantic import EmailStr
from jose import JWTError, jwt

from .token import cookie_sec, SECRET_KEY, ALGORITHM, TokenData
from ..database.config import SessionLocal
from .. import schemas
from ..schemas.user import pwd_context
from ..database.crud.user import get_user_by_email


UserReturn = Optional[Tuple[schemas.UserRead, str]]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(email: EmailStr) -> UserReturn:
    with SessionLocal() as session:
        user = get_user_by_email(session, email)

    if user is None:
        return None

    return schemas.UserRead.from_orm(user), str(user.password)


def authenticate_user(
    get_user: Callable[[EmailStr], UserReturn],
    email: EmailStr,
    password: str,
) -> Union[schemas.UserRead, bool]:
    email = EmailStr(email.lower())
    user = get_user(email)
    if user is None:
        return False
    user, db_password = user
    if verify_password(password, db_password) is False:
        return False
    return user


def get_current_user(
    token: str = Depends(cookie_sec), request: Request = None  # type: ignore
) -> schemas.UserRead:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: EmailStr = payload.get("sub")  # type: ignore
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    if token_data.email is None:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    user, _ = user
    return user


AuthenticatedUser = Depends(get_current_user)


async def get_current_admin_user(
    current_user: schemas.UserRead = Depends(get_current_user),
) -> schemas.UserRead:
    if not current_user.superuser:
        raise HTTPException(status_code=403, detail="Not an admin user")
    return current_user


AdminUser = Depends(get_current_admin_user)
