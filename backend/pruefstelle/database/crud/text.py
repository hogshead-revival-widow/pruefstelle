from typing import Optional, List
from uuid import UUID

from sqlalchemy import insert
from sqlalchemy.orm import Session

from ... import schemas
from ... import database
from ..errors import raise_for_constraint_error, raise_for_wrong_category
from .shared import update_obj, delete_obj


@raise_for_constraint_error
def create_text(
    session: Session,
    text: schemas.TextCreate,
    creator_id: UUID,
    commit_and_refresh=True,
) -> database.Text:

    data = text.dict(exclude_unset=True)
    parents: List[UUID] = data.get("parents", list())
    data.pop("parents", None)

    raise_for_wrong_category(
        session,
        expected=database.CategoryType.SourceCategory,
        id=data["source_category_id"],
    )
    raise_for_wrong_category(
        session,
        expected=database.CategoryType.TextCategory,
        id=data["category_id"],
    )

    new_text = database.Text(**data, creator_id=creator_id)  # type: ignore
    session.add(new_text)

    if len(parents) > 0:
        session.flush()
        for parent in parents:
            statement = insert(database.Text.item_link_model).values(
                parent_item_id=parent,
                child_item_id=new_text.item_id,
            )
            session.execute(statement)

    if commit_and_refresh:
        session.commit()
        session.refresh(new_text)

    return new_text


def get_text(session: Session, text_id: UUID) -> Optional[database.Text]:
    return session.get(database.Text, text_id)


def update_text(
    session: Session, text: database.Text, update: schemas.TextUpdate
) -> database.Text:

    patch = update.dict(exclude_unset=True)

    if "category_id" in patch:
        id = patch["category_id"]
        raise_for_wrong_category(
            session, database.CategoryType.TextCategory, id, ignore_None=True
        )
    if "source_id" in patch:
        id = patch["source_id"]
        raise_for_wrong_category(
            session, database.CategoryType.SourceCategory, id, ignore_None=True
        )

    return update_obj(session, text, patch)


def delete_text(session: Session, text: database.Text) -> database.Text:
    return delete_obj(session, text)
