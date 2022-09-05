from uuid import UUID
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import EmailStr

from ... import schemas
from ... import database
from .shared import update_obj, delete_obj
from ..errors import raise_for_constraint_error


@raise_for_constraint_error
def create_user(
    session: Session, user: schemas.UserCreate, superuser=False
) -> database.User:
    data = user.dict()
    new_user = database.User(**data, superuser=superuser)  # type: ignore
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def get_user(session: Session, user_id: UUID) -> Optional[database.User]:
    user = session.get(database.User, user_id)
    return user


def get_user_by_email(session: Session, email: EmailStr) -> Optional[database.User]:
    statement = select(database.User).where(database.User.email == email)
    user = session.execute(statement).scalar_one_or_none()
    return user


def update_user_email(
    session: Session,
    user: database.User,
    email: EmailStr,
) -> Optional[database.User]:
    patch = {"email": email}
    return update_obj(session, user, patch)


def update_user_password(
    session: Session,
    user: database.User,
    password_hash: str,  # this has been hashed already by UserUpdate
) -> Optional[database.User]:
    patch = {"password": password_hash}
    return update_obj(session, user, patch)


def delete_user(session: Session, user: database.User) -> Optional[database.User]:
    return delete_obj(session, user)
