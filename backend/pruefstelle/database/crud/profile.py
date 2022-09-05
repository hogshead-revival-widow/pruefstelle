from uuid import UUID
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ... import schemas
from ... import database
from .shared import update_obj, delete_obj


def create_profile(
    session: Session, profile: schemas.ProfileCreate
) -> database.Profile:
    data = profile.dict(exclude_unset=True)
    new_profile = database.Profile(**data)  # type: ignore
    session.add(new_profile)
    session.commit()
    session.refresh(new_profile)
    return new_profile


def get_profile(session: Session, profile_id: UUID) -> Optional[database.Profile]:
    return session.get(database.Profile, profile_id)


def get_profile_from_case(
    session: Session, case_id: UUID
) -> Optional[database.Profile]:
    statement = select(database.Case).where(database.Case.id == case_id)
    result = session.execute(statement).scalar_one_or_none()
    if result is None:
        return None
    return result.profile


def update_profile(
    session: Session, profile: database.Profile, update: schemas.ProfileUpdate
) -> database.Profile:

    patch = update.dict(exclude_unset=True)
    return update_obj(session, profile, patch)


def delete_profile(session: Session, profile: database.Profile) -> database.Profile:
    return delete_obj(session, profile)
