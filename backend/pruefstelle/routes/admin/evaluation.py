from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter

from ..utils import raise_404_for_None
from ... import schemas
from ...database.config import ActiveSession
from ...database import crud

router = APIRouter()


@router.delete("/{evaluation_id}", response_model=schemas.EvaluationRead)
def delete_evaluation(evaluation_id: UUID, session: Session = ActiveSession):
    evaluation = crud.get_evaluation(session, evaluation_id)
    raise_404_for_None(evaluation)
    deleted_evaluation = crud.delete_evaluation(session, evaluation)  # type: ignore
    return deleted_evaluation
