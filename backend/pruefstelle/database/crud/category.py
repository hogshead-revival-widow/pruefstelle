from uuid import UUID
from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy import select, func

from ... import schemas
from ... import database
from .shared import delete_obj, update_obj
from ..errors import raise_for_constraint_error, raise_for_wrong_category


@raise_for_constraint_error
def create_category(
    session: Session, category: schemas.CategoryCreate
) -> Optional[database.AnyCategory]:

    data = category.dict(exclude_unset=True)
    CategoryModel = schemas.CategoryType(category.discriminator).get_model()

    data.pop("discriminator", None)

    if "source_id" in data:
        raise_for_wrong_category(
            session,
            expected=schemas.CategoryType.SourceCategory,
            id=data["source_id"],
            ignore_None=True,
        )

    new_category = CategoryModel(**data)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category


def get_category_by_name(
    session: Session, name: str, discriminator: database.CategoryType
) -> Optional[database.AnyCategory]:
    ThisCategory = discriminator.get_model()
    statement = select(ThisCategory).where(
        func.lower(ThisCategory.name) == func.lower(name)
    )
    category = session.execute(statement).scalar()
    return category


def get_categories_by_name(
    session: Session, names: List[str], discriminator: database.CategoryType
) -> List[database.AnyCategory]:
    ThisCategory = discriminator.get_model()

    statement = select(ThisCategory).where(ThisCategory.name.in_(names))
    categories = session.execute(statement).scalars().all()
    return categories


def get_category(session: Session, category_id: UUID) -> Optional[database.AnyCategory]:
    category = session.get(database.Category, category_id)
    return category


def update_category(
    session: Session, category: database.AnyCategory, update: schemas.CategoryUpdate
) -> Optional[database.AnyCategory]:

    patch = update.dict(exclude_unset=True)
    del patch["discriminator"]

    if (
        "source_id" in patch
        and update.discriminator != database.CategoryType.ExternalIDCategory
    ):
        del patch["source_id"]

    return update_obj(session, category, patch)


def delete_category(
    session: Session, category: database.AnyCategory
) -> database.AnyCategory:
    return delete_obj(session, category)


def get_categories(
    session: Session, category_type: schemas.CategoryType
) -> List[database.AnyCategory]:
    statement = select(category_type.get_model())
    result = session.execute(statement).scalars().all()
    return result
