from typing import List
from sqlalchemy.orm import Session

from ... import database
from ... import schemas
from ...external.mining import TextOrder, ApiError
from .shared import mining_api, enforce_text_order_requirements


def order_text_mining_for_job(
    session: Session, job: database.MiningJob, commit_and_refresh: bool = True
) -> database.MiningJob:
    """Order text mining for `job`. Assumes requirements are fulfilled (cf. `enforce_text_order_requirements`)"""

    order = TextOrder(text=job.item.content)
    job.status = schemas.JobStatus.STARTED  # type: ignore
    try:
        receipt = mining_api.new_text_order(order=order, workflow=job.service)  # type: ignore
        job.external_id = str(receipt.order_id)  # type: ignore
    except ApiError as api_error:
        job.status = schemas.JobStatus.ERROR  # type: ignore
        print(api_error, job.id)
    session.add(job)

    if commit_and_refresh:
        session.commit()
        session.refresh(job)

    return job


def order_text_mining(
    session: Session, jobs: List[database.MiningJob]
) -> List[database.MiningJob]:
    """Order text mining for all `jobs`

    Raises:
    - `JobError` if any job is not a text job or is not set to be started (via `enforce_text_order_requirements`)
    """

    enforce_text_order_requirements(jobs)

    refreshed_jobs = list()
    for job in jobs:
        refreshed_job = order_text_mining_for_job(session, job)
        refreshed_jobs.append(refreshed_job)

    return refreshed_jobs
