from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter

from ..utils import raise_404_for_None
from ... import schemas
from ...database.config import ActiveSession
from ...database import crud

router = APIRouter()


@router.patch("/{text_id}", response_model=schemas.TextRead)
def update_text(
    text_id: UUID, update: schemas.TextUpdate, session: Session = ActiveSession
):
    text = crud.get_text(session, text_id)
    raise_404_for_None(text)
    update_text = crud.update_text(session, text, update)  # type: ignore
    return update_text


@router.delete("/{text_id}", response_model=schemas.CaseRead)
def delete_text(text_id: UUID, session: Session = ActiveSession):
    text = crud.get_text(session, text_id)
    raise_404_for_None(text)
    deleted_text = crud.delete_text(session, text)  # type: ignore
    return deleted_text
