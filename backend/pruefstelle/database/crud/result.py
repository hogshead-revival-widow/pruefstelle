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

    if isinstance(result.result, schemas.TopicCreate):
        keywords = data.pop("keywords", None)
        mappings = data.pop("mappings", None)
        new_result = ResultModel(**data)  # type: ignore
        if keywords is not None:
            new_result.keywords.extend(
                [
                    database.TopicKeyword(
                        mining_result_id=new_result.mining_result_id, **keyword
                    )  # type: ignore
                    for keyword in keywords
                ]
            )
        if mappings is not None:
            new_result.mappings.extend(
                [
                    database.TopicMapping(
                        mining_result_id=new_result.mining_result_id, **mapping
                    )  # type: ignore
                    for mapping in mappings
                ]
            )
    else:
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
