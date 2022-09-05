from typing import List

from ... import database
from ... import schemas
from ...external.mining import MiningApi
from ...external.mining.schemas import TextWorkflow
from ..errors import JobError


# may raise ApiError
mining_api = MiningApi()


def enforce_text_order_requirements(
    jobs: List[database.MiningJob],
    allowed_status: List[schemas.JobStatus] = [schemas.JobStatus.TO_BE_STARTED],
):
    """Raises `JobError` if any job is not a text job or is not set to be started"""
    are_to_be_started = (job.status in allowed_status for job in jobs)
    if not all(are_to_be_started):
        all_status = [job.status for job in jobs]
        raise JobError(
            f"At least one job doesn't have the expected status `{allowed_status}` (found status: {all_status}) "
        )

    all_text_workflows = TextWorkflow.to_list()
    are_text_services = (
        job.service in all_text_workflows for job in jobs  # type: ignore
    )  #
    if not all(are_text_services):
        raise JobError("At least one job is not asking for a text service")

    are_texts = (job.item.discriminator == database.ItemType.Text for job in jobs)
    if not all(are_texts):
        raise JobError("At least one job isn't pointing to a text")
