from uuid import UUID
from typing import TypeVar, Callable, Type, Optional
from sqlalchemy.orm import Session
from .utils import raise_404_for_None, raise_401_for_violation


T = TypeVar("T")


def _get_item(session: Session, item_kind: Type[T], item_id: UUID) -> T:
    item = session.get(item_kind, item_id)
    raise_404_for_None(item)
    return item


def _enforce(
    item: T, enforce: Callable[[T, UUID], bool], current_user_id: UUID
) -> None:
    restriction = enforce(item, current_user_id)
    raise_401_for_violation(restriction)


def enforce_restriction_and_get(
    session: Session,
    item_kind: Type[T],
    item_id: UUID,
    enforce: Callable[[T, UUID], bool],
    current_user_id: UUID,
) -> T:
    """
    May raise:
    - 404: if item identified by `item_id` is not found
    - 401: if `check` returns `False`
    """
    item = _get_item(session, item_kind, item_id)
    _enforce(item, enforce, current_user_id)
    return item
