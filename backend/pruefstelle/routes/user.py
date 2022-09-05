from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Response
from fastapi_pagination import Page


from .. import schemas
from ..database.config import ActiveSession
from .utils import raise_404_for_None, raise_401_for_violation
from ..database import crud
from ..security import AuthenticatedUser, set_cookie
from ..security.authenticate import verify_password

router = APIRouter()


@router.get("/self", response_model=schemas.UserRead)
def read_self(
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    return current_user


@router.get("/self/cases", response_model=Page[schemas.CaseRead])
def read_self_cases(
    session: Session = ActiveSession, current_user: schemas.UserRead = AuthenticatedUser
):
    evaluations = crud.get_cases_by_watcher_id(
        session, watcher_id=current_user.id, with_pagination=True
    )
    return evaluations


@router.get("/self/evaluations", response_model=Page[schemas.EvaluationRead])
def read_self_evaluations(
    session: Session = ActiveSession, current_user: schemas.UserRead = AuthenticatedUser
):
    evaluations = crud.get_evaluations_by_creator_id(
        session, creator_id=current_user.id, with_pagination=True
    )
    return evaluations


@router.get(
    "/self/evaluations/case/{case_id}",
    response_model=Page[schemas.EvaluationRead],
)
def read_self_evaluations_for_case(
    case_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    evaluations = crud.get_evaluations_by_creator_id_and_case_id(
        session,
        creator_id=current_user.id,
        case_id=case_id,
        with_pagination=True,
    )

    return evaluations


@router.get(
    "/self/evaluations/document/{document_id}",
    response_model=Page[schemas.EvaluationRead],
)
def read_self_evaluations_for_document(
    document_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    evaluations = crud.get_evaluations_by_creator_id_and_document_id(
        session,
        creator_id=current_user.id,
        document_id=document_id,
        with_pagination=True,
    )

    return evaluations


@router.get(
    "/self/evaluations/text/{text_id}", response_model=Page[schemas.EvaluationRead]
)
def read_self_evaluations_for_text(
    text_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    evaluations = crud.get_evaluations_by_creator_id_and_text_id(
        session, creator_id=current_user.id, text_id=text_id, with_pagination=True
    )

    return evaluations


@router.patch("/self", response_model=schemas.UserRead)
async def update_self(
    update: schemas.UserUpdate,
    response: Response,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    user = crud.get_user(session, current_user.id)
    raise_404_for_None(user)
    raise_401_for_violation(verify_password(update.current_password, user.password))  # type: ignore
    patch = update.dict(exclude_unset=True)
    if "email" in patch:
        user = crud.update_user_email(session, user, email=patch["email"])  # type: ignore
    if "new_password" in patch:
        user = crud.update_user_password(session, user, password_hash=patch["new_password"])  # type: ignore

    user = schemas.UserRead.from_orm(user)
    await set_cookie(response, user)  # type: ignore
    return user


@router.post("/self/watch/{case_id}", response_model=schemas.CaseRead)
def toggle_watch_case(
    case_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """ "Stop watching a case, if you watch it. Start watching it, if you don't."""
    case = crud.toggle_watch_case(session, case_id, current_user.id)
    raise_404_for_None(case)
    return case
