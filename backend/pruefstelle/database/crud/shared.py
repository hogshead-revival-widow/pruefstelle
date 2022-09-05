from typing import Dict, List, Optional, Type, TypeVar, Any, Callable
from uuid import UUID

from sqlalchemy import insert, Table
from sqlalchemy.orm import Session

from ..errors import raise_for_constraint_error


T = TypeVar("T")

Patch = Dict[str, Any]


def establish_link(session: Session, link_model: Table, links: List[Dict[str, UUID]]):
    for link in links:
        linker = insert(link_model).values(**link)
        session.execute(linker)


def get_obj(
    session: Session, obj: Type[T], id: UUID, fetched_obj: Optional[T] = None
) -> Optional[T]:
    if fetched_obj is None:
        db_obj = session.get(obj, id)
        if db_obj is None:
            return None
        return db_obj
    return fetched_obj


@raise_for_constraint_error
def update_obj(session: Session, db_obj: T, patch: Dict[str, Any]) -> T:
    """Update instance of `obj` according to `patch`."""

    if len(patch) == 0:
        return db_obj

    for attribute, value in patch.items():
        setattr(db_obj, attribute, value)

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def delete_obj(session: Session, db_obj: T) -> T:
    """
    Delete `db_obj`
    """
    session.delete(db_obj)
    session.commit()
    return db_obj
