from uuid import UUID
from typing import Optional, List, Union

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.sqlalchemy_future import paginate

from ... import schemas
from ... import database
from .shared import delete_obj, update_obj
from ..errors import raise_for_constraint_error


@raise_for_constraint_error
def create_evaluation(
    session: Session,
    mining_result_id: UUID,
    evaluation: schemas.EvaluationCreate,
    creator_id: UUID,
) -> Optional[database.Evaluation]:

    data = evaluation.dict(exclude_unset=True, exclude={"discriminator"})
    EvaluationModel = evaluation.discriminator.get_model()

    new_evaluation = EvaluationModel(
        **data, mining_result_id=mining_result_id, creator_id=creator_id
    )
    session.add(new_evaluation)
    session.commit()
    session.refresh(new_evaluation)
    return new_evaluation


def get_evaluation(
    session: Session, evaluation_id: UUID
) -> Optional[database.Evaluation]:
    evaluation = session.get(database.Evaluation, evaluation_id)
    return evaluation


def update_evaluation(
    session: Session, evaluation: database.Evaluation, update: schemas.EvaluationUpdate
) -> database.Evaluation:

    patch = update.dict(exclude_unset=True)
    del patch["discriminator"]
    patch["value"] = int(patch["value"])

    return update_obj(session, evaluation, patch)


def delete_evaluation(
    session: Session, evaluation: database.Evaluation
) -> database.Evaluation:
    return delete_obj(session, evaluation)


def get_evaluations(
    session: Session, mining_result_id: UUID
) -> List[database.Evaluation]:
    statement = select(database.Evaluation).where(
        database.Evaluation.mining_result_id == mining_result_id
    )
    evaluations = session.execute(statement).scalars().all()
    return evaluations


@raise_for_constraint_error
def get_evaluations_by_creator_id(
    session: Session, creator_id: UUID, with_pagination=False
) -> Union[AbstractPage, List[database.Evaluation]]:
    statement = select(database.Evaluation).where(
        database.Evaluation.creator_id == creator_id
    )
    if with_pagination:
        return paginate(session, statement)

    evaluations = session.execute(statement).scalars().all()
    return evaluations


@raise_for_constraint_error
def get_evaluations_by_creator_id_and_case_id(
    session: Session, creator_id: UUID, case_id: UUID, with_pagination=False
) -> Union[AbstractPage, List[database.Evaluation]]:

    statement = (
        select(database.Evaluation)
        .join(database.MiningResult)
        .join(database.Item)
        .join(database.Document)
        .join(database.Case, onclause=database.Document.cases)
        .where(
            database.Case.id == case_id, database.Evaluation.creator_id == creator_id
        )
    )

    if with_pagination:
        return paginate(session, statement)
    evaluations = session.execute(statement).scalars().all()

    return evaluations


@raise_for_constraint_error
def get_evaluations_by_creator_id_and_document_id(
    session: Session, creator_id: UUID, document_id: UUID, with_pagination=False
) -> Union[AbstractPage, List[database.Evaluation]]:

    statement = (
        select(database.Evaluation)
        .join(database.MiningResult)
        .join(database.Item)
        .where(
            database.Item.document_id == document_id,
            database.Evaluation.creator_id == creator_id,
        )
    )

    if with_pagination:
        return paginate(session, statement)
    evaluations = session.execute(statement).scalars().all()
    return evaluations


@raise_for_constraint_error
def get_evaluations_by_creator_id_and_text_id(
    session: Session, creator_id: UUID, text_id: UUID, with_pagination=False
) -> Union[AbstractPage, List[database.Evaluation]]:

    # Hole alle Evaluationen, die
    # mit ihrer mining_result_id auf
    # mining_results zeigen, die mit ihrer item_id
    # auf das document verweisen
    statement = (
        select(database.Evaluation)
        .where(database.Evaluation.creator_id == creator_id)
        .join(database.MiningResult)
        .join(database.Text)
        .where(database.Text.item_id == text_id)
    )
    if with_pagination:
        return paginate(session, statement)
    evaluations = session.execute(statement).scalars().all()
    return evaluations
