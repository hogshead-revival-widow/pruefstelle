from ...database.config import SessionLocal
from ...database import crud
from ... import schemas
from ...external.mining.schemas import ProcessingStatus
from ...external.errors import ApiRequestError
from .shared import mining_api
from .result import get_and_save_result


def update_status():
    """Update status of mining jobs that have neither completed nor failed.

    Note:
        * This needs to run seperatedly from the main app (cf. `run_repeating`)
        * Thus, (top-level) exception handling is expected there"""

    with SessionLocal() as session:

        wanted_status = [
            schemas.JobStatus.STARTED,
            schemas.JobStatus.NEW,
            schemas.JobStatus.RUNNING,
            schemas.JobStatus.COMPLETED
            # schemas.JobStatus.PARTIALLY_COMPLETED,
        ]
        unfinished_jobs = crud.get_jobs_by_status(session, status=wanted_status)

        if len(unfinished_jobs) == 0:
            return None

        for job in unfinished_jobs:
            try:
                status = mining_api.get_status(order_id=job.external_id)  # type: ignore

                is_still_running = (
                    status.processing_status == ProcessingStatus.NEW
                    or status.processing_status == ProcessingStatus.RUNNING
                )
                is_finished_successfully = (
                    status.processing_status == ProcessingStatus.COMPLETED
                )
            except ApiRequestError as error:
                if error.response.status_code == 404:
                    job.status = schemas.JobStatus.ERROR  # type: ignore
                    session.add(job)
                    session.commit()
                    continue
                raise error

            if is_still_running:
                continue

            if not is_finished_successfully:
                # Any other status means there has been an error
                job.status = schemas.JobStatus.ERROR  # type: ignore
                session.add(job)
                session.commit()
                continue

            job.status = status.processing_status  # type: ignore
            session.add(job)
            session.commit()
            session.refresh(job)

            if is_finished_successfully:
                get_and_save_result(session, job)
