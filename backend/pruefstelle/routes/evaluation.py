from uuid import UUID
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter

from .. import schemas
from ..database.config import ActiveSession
from .. import database
from ..database import crud
from .utils import raise_404_for_None
from .shared import enforce_restriction_and_get
from . import restrictions
from ..security import AuthenticatedUser

router = APIRouter()


@router.post("/mining_result/{mining_result_id}", response_model=schemas.EvaluationRead)
def create_evaluation(
    mining_result_id: UUID,
    evaluation: schemas.EvaluationCreate,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    new_evaluation = crud.create_evaluation(
        session, mining_result_id, evaluation, creator_id=current_user.id
    )
    return new_evaluation


@router.get(
    "/mining_result/{mining_result_id}", response_model=List[schemas.EvaluationRead]
)
def read_item_evaluations(
    mining_result_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    evaluations = crud.get_evaluations(session, mining_result_id)
    return evaluations


@router.get("/{evaluation_id}", response_model=schemas.EvaluationRead)
def read_evaluation(
    evaluation_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    evaluation = crud.get_evaluation(session, evaluation_id)
    raise_404_for_None(evaluation)
    return evaluation


@router.patch("/{evaluation_id}", response_model=schemas.EvaluationRead)
def update_evaluation(
    evaluation_id: UUID,
    update: schemas.EvaluationUpdate,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """
    You can only update an evaluation, if it was created by you
    """

    restriction = restrictions.has_evaluation_update_access
    evaluation = enforce_restriction_and_get(
        session, database.Evaluation, evaluation_id, restriction, current_user.id
    )
    updated_evaluation = crud.update_evaluation(session, evaluation, update)
    return updated_evaluation


@router.delete("/{evaluation_id}", response_model=schemas.EvaluationRead)
def delete_evaluation(
    evaluation_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """
    You can only delete an evaluation, if it was created by you
    """
    restriction = restrictions.has_evaluation_delete_access
    evaluation = enforce_restriction_and_get(
        session, database.Evaluation, evaluation_id, restriction, current_user.id
    )
    deleted_evaluation = crud.delete_evaluation(session, evaluation)
    return deleted_evaluation
