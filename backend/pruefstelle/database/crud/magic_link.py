from uuid import UUID
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import Session
import datetime

from ... import database
from ..errors import raise_for_constraint_error


@raise_for_constraint_error
def create_link_value(session: Session, user_id: UUID, hashed_value: str):
    new_link = database.MagicLink(user_id=user_id, value=hashed_value)  # type: ignore
    session.add(new_link)
    session.commit()


def delete_old_links(session: Session, expires_after_minutes: int):
    too_old = datetime.datetime.now() - datetime.timedelta(
        minutes=expires_after_minutes
    )
    statement = delete(database.MagicLink).where(
        database.MagicLink.date <= too_old.isoformat()
    )
    session.execute(statement)
    session.commit()


@raise_for_constraint_error
def get_link(session: Session, user_id: UUID) -> Optional[database.MagicLink]:
    statement = select(database.MagicLink).where(database.MagicLink.user_id == user_id)
    link = session.execute(statement).scalar_one_or_none()
    return link


@raise_for_constraint_error
def delete_link(session: Session, user_id: UUID):
    statement = delete(database.MagicLink).where(database.MagicLink.user_id == user_id)
    session.execute(statement)
    session.commit()
