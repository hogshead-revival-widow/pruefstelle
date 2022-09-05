from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter

from ..utils import raise_404_for_None
from ... import schemas
from ...database.config import ActiveSession
from ...database import crud

router = APIRouter()


@router.post("", response_model=schemas.CategoryRead)
def create_category(category: schemas.CategoryCreate, session: Session = ActiveSession):

    new_category = crud.create_category(session, category)
    raise_404_for_None(new_category)
    return new_category


@router.patch("/{category_id}", response_model=schemas.CategoryRead)
def update_category(
    category_id: UUID, update: schemas.CategoryUpdate, session: Session = ActiveSession
):
    """
    Note:
    - `source_id ` is **ignored**, if `type` is other than `external_id`
    - you can't change the type (cf. `discriminator`) of the category
    """
    category = crud.get_category(session, category_id)
    raise_404_for_None(category)
    updated_category = crud.update_category(session, category, update)  # type: ignore
    return updated_category
