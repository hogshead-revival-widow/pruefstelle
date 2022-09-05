from typing import Optional, List
from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from ... import schemas
from ... import database
from ..errors import raise_for_constraint_error, raise_for_wrong_category
from .shared import delete_obj, update_obj


@raise_for_constraint_error
def create_document(
    session: Session,
    document: schemas.DocumentCreate,
    creator_id: UUID,
    commit_and_refresh=True,
) -> database.Document:

    document_data = document.dict(exclude_unset=True)
    document_data.pop("cases")
    new_document = database.Document(**document_data, creator_id=creator_id)  # type: ignore

    raise_for_wrong_category(
        session,
        expected=database.CategoryType.DocumentCategory,
        id=document.category_id,
    )
    raise_for_wrong_category(
        session,
        expected=database.CategoryType.ExternalIDCategory,
        id=document.external_id_category_id,
        ignore_None=True,
    )

    session.add(new_document)

    if len(document.cases) > 0:
        session.flush()
        for case_id in document.cases:
            statement = insert(database.Document.case_link_model).values(
                document_id=new_document.id,
                case_id=case_id,
            )
            session.execute(statement)

    if commit_and_refresh:
        session.commit()
        session.refresh(new_document)

    return new_document


def get_document(session: Session, document_id: UUID) -> Optional[database.Document]:
    document = session.get(database.Document, document_id)
    return document


def get_document_from_mining_result(
    session: Session, mining_result_id: UUID
) -> Optional[database.Document]:
    statement = (
        select(database.Document)
        .join(database.Item)
        .join(database.MiningResult)
        .where(database.MiningResult.id == mining_result_id)
    )
    document = session.execute(statement).scalar()
    return document


def get_document_item_ids(session: Session, document_id: UUID) -> List[UUID]:

    statement = select(database.Item.id).where(database.Item.document_id == document_id)
    item_ids = session.execute(statement).scalars().all()
    return item_ids


def update_document(
    session: Session, document: database.Document, update: schemas.DocumentUpdate
) -> database.Document:

    patch = update.dict(exclude_unset=True)

    if "category_id" in patch:
        id = patch["category_id"]
        raise_for_wrong_category(
            session, database.CategoryType.DocumentCategory, id, ignore_None=True
        )
    if "external_id_category_id" in patch:
        id = patch["external_id_category_id"]
        raise_for_wrong_category(
            session, database.CategoryType.ExternalIDCategory, id, ignore_None=True
        )

    return update_obj(session, document, patch)


def delete_document(session: Session, document: database.Document) -> database.Document:
    deleted = delete_obj(session, document)
    return deleted
