from uuid import UUID
from ... import database
from ... import schemas


def has_job_update_access(job: database.MiningJob, current_user_id: UUID) -> bool:
    if (job.creator_id == current_user_id) and (job.status == schemas.JobStatus.DRAFT):
        return True
    return False


def has_job_delete_access(job: database.MiningJob, current_user_id: UUID) -> bool:
    return has_job_update_access(job, current_user_id)
