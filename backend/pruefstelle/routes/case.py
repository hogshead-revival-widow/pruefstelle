from uuid import UUID
from typing import Optional

from sqlalchemy.orm import Session
from fastapi import APIRouter, Query
from fastapi_pagination import Page
from pydantic import ConstrainedStr

from .utils import raise_404_for_None
from .. import schemas
from ..database.config import ActiveSession
from ..security import AuthenticatedUser
from .. import database
from ..database import crud
from . import restrictions
from .shared import enforce_restriction_and_get


router = APIRouter()


@router.post("", response_model=schemas.CaseRead)
def create_case(
    case: schemas.CaseCreate,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    new_case = crud.create_case(session, case, creator_id=current_user.id)
    return new_case


@router.get("", response_model=Page[schemas.CaseRead])
def list_cases(
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    cases = crud.get_cases(session, with_pagination=True)
    return cases


class ConStr(ConstrainedStr):
    min_length = 3


@router.get("/search", response_model=Page[UUID])
def search_cases(
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
    title: Optional[ConStr] = Query(default=None),
    category_name: Optional[ConStr] = Query(default=None),
):
    """Search for a case that has a matching category name or title."""
    cases = crud.search_cases(
        session, title=title, category_name=category_name, with_pagination=True
    )
    return cases


@router.get("/{case_id}", response_model=schemas.CaseRead)
def read_case(
    case_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    case = crud.get_case(session, case_id)
    raise_404_for_None(case)
    return case


@router.patch("/{case_id}", response_model=schemas.CaseRead)
def update_case(
    case_id: UUID,
    update: schemas.CaseUpdate,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """
    Note:
    - You can only update a case if
        - it was created by you and
        - it has no documents attached yet
    """
    restriction = restrictions.has_case_update_access
    case = enforce_restriction_and_get(
        session, database.Case, case_id, restriction, current_user.id
    )
    case = crud.update_case(session, case, update)
    return case


@router.delete("/{case_id}", response_model=schemas.CaseRead)
def delete_case(
    case_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """
    Note:
    - You can only delete a case if
         - it was created by you and
        - it has no documents attached yet
    """

    restriction = restrictions.has_case_delete_access
    case = enforce_restriction_and_get(
        session, database.Case, case_id, restriction, current_user.id
    )
    deleted_case = crud.delete_case(session, case)

    return deleted_case
