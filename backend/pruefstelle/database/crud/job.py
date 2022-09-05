from uuid import UUID
from typing import Optional, List, Set, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from ... import schemas
from ... import database
from ..errors import raise_for_constraint_error
from .shared import delete_obj, update_obj


@raise_for_constraint_error
def create_job(
    session: Session, job: schemas.JobCreate, creator_id: UUID, commit_and_refresh=True
) -> database.MiningJob:

    data = job.dict(exclude_unset=True)
    new_job = database.MiningJob(**data, creator_id=creator_id)  # type: ignore

    session.add(new_job)

    if commit_and_refresh:
        session.commit()
        session.refresh(new_job)

    return new_job


def create_jobs_for_text(
    session: Session,
    text: database.Text,
    services: Set[schemas.Service],
    creator_id: UUID,
    commit_and_refresh: bool = True,
    as_draft: bool = False,
) -> Tuple[database.Text, List[database.MiningJob]]:

    new_jobs = list()
    status = schemas.JobStatus.TO_BE_STARTED
    if as_draft:
        status = schemas.JobStatus.DRAFT
    for service in services:
        job = schemas.JobCreate(
            service=service, status=status, item_id=text.id  # type: ignore
        )
        new_job = create_job(session, job, creator_id)
        new_jobs.append(new_job)

    if commit_and_refresh:
        session.commit()
        for job in new_jobs:
            session.refresh(job)
    return text, new_jobs


def update_job(
    session: Session, job: database.MiningJob, update: schemas.JobUpdate
) -> database.MiningJob:
    patch = update.dict(exclude_unset=True)
    return update_obj(session, job, patch)


def delete_job(session: Session, job: database.MiningJob) -> database.MiningJob:
    return delete_obj(session, job)


def get_job(session: Session, job_id: UUID) -> Optional[database.MiningJob]:
    job = session.get(database.MiningJob, job_id)
    return job


def get_jobs_by_status(
    session: Session, status: List[schemas.JobStatus]
) -> List[database.MiningJob]:

    statement = select(database.MiningJob).where(database.MiningJob.status.in_(status))
    jobs = session.execute(statement).scalars().all()
    return jobs
