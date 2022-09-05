from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter

from .utils import raise_404_for_None
from .. import schemas
from ..database.config import ActiveSession
from .. import database
from ..database import crud
from . import restrictions
from .shared import enforce_restriction_and_get
from ..security import AuthenticatedUser

router = APIRouter()


@router.post("", response_model=schemas.DocumentRead)
def create_document(
    document: schemas.DocumentCreate,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    new_document = crud.create_document(session, document, creator_id=current_user.id)
    return new_document


@router.get("/mining_result/{mining_result_id}", response_model=schemas.DocumentRead)
def read_document_from_mining_result(
    mining_result_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    document = crud.get_document_from_mining_result(session, mining_result_id)
    raise_404_for_None(document)
    return document


@router.get("/{document_id}", response_model=schemas.DocumentRead)
def read_document(
    document_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    document = crud.get_document(session, document_id)
    raise_404_for_None(document)
    return document


@router.patch("/{document_id}", response_model=schemas.DocumentRead)
def update_document(
    document_id: UUID,
    update: schemas.DocumentUpdate,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """
    Note:
    - You can only update a document if
        - it was created by you and
        - it has no cases attached yet
    """
    restriction = restrictions.has_document_update_access
    document = enforce_restriction_and_get(
        session, database.Document, document_id, restriction, current_user.id
    )

    document = crud.update_document(session, document, update)
    return document


@router.delete("/{document_id}", response_model=schemas.DocumentRead)
def delete_document(
    document_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """
    Beware:
    - This will also delete any items (e.g. texts) attached to this document

    Note:
    - You can only delete a document if
        - it was created by you and
        - it has no cases attached yet
    """
    restriction = restrictions.has_document_delete_access
    document = enforce_restriction_and_get(
        session, database.Document, document_id, restriction, current_user.id
    )

    # load the document fully before it or its depending items are deleted
    # otherwise lazy loading may fail
    deleted_document = schemas.DocumentRead.from_orm(document)
    crud.delete_document(session, document)
    return deleted_document
