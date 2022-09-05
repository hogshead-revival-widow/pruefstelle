from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, BackgroundTasks


from .utils import raise_404_for_None
from .. import schemas
from ..database.config import ActiveSession
from ..database import crud
from .. import tasks
from .. import database
from . import restrictions
from .shared import enforce_restriction_and_get
from ..security import AuthenticatedUser


router = APIRouter()


@router.post("", response_model=schemas.TextRead)
def create_text(
    text: schemas.TextCreate,
    services: schemas.AtLeastOneService,
    background_tasks: BackgroundTasks,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """
    Create a text and a job for every service specified and start the jobs.
    Note:
        - You need to create a document before adding a text.
        - You need to trigger the job to start, it is created as a draft
    """
    new_text = crud.create_text(session, text, current_user.id)
    new_text, new_jobs = crud.create_jobs_for_text(
        session, new_text, services, current_user.id, as_draft=True
    )
    background_tasks.add_task(tasks.order_text_mining, session, new_jobs)

    return new_text


@router.get("/{text_id}", response_model=schemas.TextRead)
def read_text(
    text_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    text = crud.get_text(session, text_id)
    raise_404_for_None(text)
    return text


@router.patch("/{text_id}", response_model=schemas.TextRead)
def update_text(
    text_id: UUID,
    update: schemas.TextUpdate,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """
    Note:
    - You can only update a text, if
        - it was created by you and
        - the document it is attached to is not used in any case
    """
    text = enforce_restriction_and_get(
        session,
        database.Text,
        text_id,
        restrictions.has_text_update_access,
        current_user.id,
    )
    update_text = crud.update_text(session, text, update)
    return update_text


@router.delete("/{text_id}", response_model=schemas.TextRead)
def delete_text(
    text_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """
    Note:
    - You can only delete a text, if
         - it was created by you and
         - the document it is attached to is not used in any case
    """
    restriction = restrictions.has_text_delete_access
    text = enforce_restriction_and_get(
        session, database.Text, text_id, restriction, current_user.id
    )
    deleted_text = crud.delete_text(session, text)
    return deleted_text
