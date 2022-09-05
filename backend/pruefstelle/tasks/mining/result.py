from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from .shared import mining_api, enforce_text_order_requirements
from ... import schemas
from ... import database
from ...database import crud
from ...external.errors import ApiRequestError


def is_same(that: schemas.ResultCreate, other: database.AnyResult) -> bool:
    if other.discriminator != that.result.discriminator:
        return False
    return that.result.is_same(other)  # type: ignore


def is_known(that: schemas.ResultCreate, others: List[database.AnyResult]) -> bool:
    return any(is_same(that, other) for other in others)


def write_text_results_to_db(
    session: Session, job: database.MiningJob, new_results: List[schemas.ResultCreate]
) -> List[database.AnyResult]:

    saved_results: List[database.AnyResult] = job.results
    created_items = [crud.create_result(session, job.id, result_to_add) for result_to_add in new_results if not is_known(result_to_add, saved_results)]  # type: ignore
    job.status = schemas.JobStatus.RESULTS_IN_DB  # type: ignore
    session.add(job)
    session.commit()
    if len(created_items) == 0:
        return created_items

    return created_items


def get_text_results(
    session: Session, job: database.MiningJob
) -> List[schemas.ResultCreate]:

    try:
        results_from_api = mining_api.get_text_result(
            order_id=UUID(job.external_id), workflow=job.service  # type: ignore
        )
    except ApiRequestError as error:
        job.status = schemas.JobStatus.ERROR  # type: ignore
        session.add(job)
        session.commit()
        print(error)
        return list()

    item_id = job.item_id
    results = [
        schemas.ResultCreate.from_result_base(
            returned_result,
            item_id,  # type: ignore
        )
        for returned_result in results_from_api.get_items()
    ]
    session.add(job)
    session.commit()
    return results


def get_and_save_result(
    session: Session, job: database.MiningJob
) -> List[database.AnyResult]:

    is_completed = [schemas.JobStatus.COMPLETED]
    enforce_text_order_requirements([job], allowed_status=is_completed)

    new_results = get_text_results(session, job)
    db_results = write_text_results_to_db(session, job, new_results=new_results)
    return db_results
