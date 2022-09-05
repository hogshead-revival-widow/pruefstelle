from uuid import UUID
from typing import Optional, List, Union

from sqlalchemy.orm import Session
from sqlalchemy import select


from ... import schemas
from ... import database
from .shared import establish_link
from ..errors import raise_for_constraint_error


@raise_for_constraint_error
def create_result(
    session: Session,
    job_id: UUID,
    result: schemas.ResultCreate,
    commit_and_refresh=True,
) -> database.AnyResult:
    data = result.result.dict(exclude_unset=True)
    ResultModel: database.AnyResult = result.result.discriminator.get_model()

    new_result = ResultModel(**data)  # type: ignore

    session.add(new_result)
    session.flush()

    links = [{"mining_result_id": new_result.id, "mining_job_id": job_id}]
    link_model = ResultModel.mining_job_mining_result_link_model
    establish_link(session, link_model, links)

    if commit_and_refresh:
        session.commit()
        session.refresh(new_result)

    return new_result


def get_result(session, result_id) -> Optional[database.AnyResult]:
    result = session.get(database.MiningResult, result_id)
    return result


def get_results_for_item(
    session: Session, item_id: Union[UUID, List[UUID]]
) -> List[database.AnyResult]:

    if isinstance(item_id, UUID):
        item_id = [item_id]

    item_ids = tuple(item_id)

    statement = select(database.MiningResult).filter(
        database.MiningResult.item_id.in_(item_ids)
    )

    result = session.execute(statement).scalars().all()
    return result
