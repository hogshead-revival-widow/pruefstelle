from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter

from ..utils import raise_404_for_None
from ... import schemas
from ...database.config import ActiveSession
from ...database import crud

router = APIRouter()


@router.patch("/{document_id}", response_model=schemas.DocumentRead)
def update_document(
    document_id: UUID, update: schemas.DocumentUpdate, session: Session = ActiveSession
):

    document = crud.get_case(session, document_id)
    raise_404_for_None(document)
    updated_case = crud.update_document(session, document, update)  # type: ignore
    return updated_case


@router.delete("/{document_id}", response_model=schemas.CaseRead)
def delete_document(document_id: UUID, session: Session = ActiveSession):
    document = crud.get_case(session, document_id)
    raise_404_for_None(document)
    deleted_document = crud.delete_document(session, document)  # type: ignore
    return deleted_document
