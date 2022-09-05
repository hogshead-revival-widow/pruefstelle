from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter

from ..utils import raise_404_for_None
from ... import schemas
from ...database.config import ActiveSession
from ...database import crud

router = APIRouter()


@router.patch("/{case_id}", response_model=schemas.CaseRead)
def update_case(
    case_id: UUID, update: schemas.CaseUpdate, session: Session = ActiveSession
):
    case = crud.get_case(session, case_id)
    raise_404_for_None(case)
    updated_case = crud.update_case(session, case, update)  # type: ignore
    return updated_case


@router.delete("/{case_id}", response_model=schemas.CaseRead)
def delete_case(case_id: UUID, session: Session = ActiveSession):
    case = crud.get_case(session, case_id)
    raise_404_for_None(case)
    deleted_case = crud.delete_case(session, case)  # type: ignore
    return deleted_case
