from typing import Callable, TypeVar, Optional
from typing_extensions import ParamSpec
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .tables import CategoryType

from ..errors import PruefstelleError


class CRUDError(PruefstelleError):
    user_message: str = "Something unexpected happened database-wise"


class IDError(CRUDError):
    """
    Foreign key constraint failed or the object referenced by a user-given ID is not as expected
    """

    user_message: str = "At least one given ID is not pointing to the expected kind of ressource, most likely due to a wrong UUID"


class NotUniqueError(CRUDError):
    """
    Unique constraint failed
    """

    user_message: str = "At least one given value is not unique, but was expected to be"


def raise_for_wrong_category(
    session: Session,
    expected: CategoryType,
    id: Optional[UUID],
    ignore_None=False,
):
    """
    Raises `IDError`, if `expected`  and persisted type of the category referenced by `id` don't match.

    If `ignore_None` is True and `id` is None, no error is raised.

    This is necessary, because a foreign key constraint isn't sufficient in the category case,
    since it's constrained to *any* category (Single Table Inheritance).
    """
    if not ignore_None and id is None:
        raise IDError()
    if ignore_None and id is None:
        return None

    CategoryModel = expected.get_model()
    category = session.get(CategoryModel, id)

    if category is None:
        raise IDError()


ReturnType = TypeVar("ReturnType")
ParamTypes = ParamSpec("ParamTypes")


def raise_for_constraint_error(
    func: Callable[ParamTypes, ReturnType]
) -> Callable[ParamTypes, ReturnType]:
    """
    Decorator, raising CRUDError, i.e.:
    - NotUniqueError, if the unique constraint failed
    - IDError, if the foreign key error constraint failed
    """

    def handler(*args: ParamTypes.args, **kwargs: ParamTypes.kwargs) -> ReturnType:
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            # cf. https://docs.sqlalchemy.org/en/14/core/exceptions.html#sqlalchemy.exc.IntegrityError
            # An IntegrityError is just a wrapper for a DB-API IntegrityError.
            # To differentiate between a foreign key error and other errors, the error needs parsing
            original_message = str(e.orig.args)
            is_foreign_key_error = (
                "foreign key" in original_message.lower()
                and "constraint" in original_message.lower()
            )
            if is_foreign_key_error:
                raise IDError()
            is_unique_constraint_error = (
                "unique" in original_message.lower()
                and "constraint" in original_message.lower()
            )
            if is_unique_constraint_error:
                raise NotUniqueError()

            raise

    return handler
