from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter

from .. import schemas
from ..database.config import ActiveSession
from ..database import crud
from .utils import raise_404_for_None
from ..security import AuthenticatedUser


router = APIRouter()


@router.post("/{job_id}", response_model=schemas.ResultRead)  # type: ignore
def create_result(
    job_id: UUID,
    result: schemas.ResultCreate,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """Temp, to delete"""
    new_result = crud.create_result(session, job_id, result)

    return new_result


@router.get("/{result_id}", response_model=schemas.ResultRead)  # type: ignore
def read_result(
    result_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    result = crud.get_result(session, result_id)
    raise_404_for_None(result)
    return result


# @router.get("/{snapshot_id}", response_model=schemas.SnapshotRead)
# def read_research_quality_snapshot(snapshot_id: UUID, session: Session = ActiveSession):
#     snapshot = crud.get_snapshot(session, snapshot_id)
#     raise_404_for_None(snapshot)
#     return snapshot


@router.get("/list/{item_id}", response_model=List[schemas.ResultRead])
def list_results_for_item(
    item_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    results = crud.get_results_for_item(session, item_id)

    return results
