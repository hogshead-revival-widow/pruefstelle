from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, BackgroundTasks

from .. import schemas
from ..database.config import ActiveSession
from .. import database
from ..database import crud
from .utils import raise_404_for_None
from . import restrictions
from .shared import enforce_restriction_and_get
from ..security import AuthenticatedUser
from ..tasks import order_text_mining

router = APIRouter()


# @router.post("", response_model=schemas.JobRead)
# def create_job(
#     job: schemas.JobCreate,
#     session: Session = ActiveSession,
#     current_user: schemas.UserRead = AuthenticatedUser,
# ):
#     new_job = crud.create_job(session, job, current_user.id)
#     return new_job


@router.get("/{job_id}", response_model=schemas.JobRead)
def read_job(
    job_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    job = crud.get_job(session, job_id)
    raise_404_for_None(job)
    return job


@router.patch("/{job_id}/start", response_model=schemas.JobRead)
def start_job(
    job_id: UUID,
    background_tasks: BackgroundTasks,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """
    Set a job, i.e. a job draft, to start.

    Note:
    - You can only update a job, if
        - it was created by you and
        - it is a draft
    """
    restriction = restrictions.has_job_update_access
    job = enforce_restriction_and_get(
        session, database.MiningJob, job_id, restriction, current_user.id
    )
    update = schemas.JobUpdate(status=schemas.JobStatus.TO_BE_STARTED)
    updated_job = crud.update_job(session, job, update)

    background_tasks.add_task(order_text_mining, session, [updated_job])

    return updated_job


@router.delete("/{job_id}", response_model=schemas.JobRead)
def delete_job(
    job_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """
    Note:
    - You can only delete a job, if
        - it was created by you and
        - it is a draft
    """
    restriction = restrictions.has_job_delete_access
    job = enforce_restriction_and_get(
        session, database.MiningJob, job_id, restriction, current_user.id
    )
    deleted_job = crud.delete_job(session, job)
    return deleted_job
