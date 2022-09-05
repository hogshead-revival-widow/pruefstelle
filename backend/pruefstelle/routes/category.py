from uuid import UUID
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter

from .utils import raise_404_for_None
from .. import schemas
from ..database.config import ActiveSession
from ..database import crud
from ..security import AuthenticatedUser

router = APIRouter()


@router.get("/{category_id}", response_model=schemas.CategoryRead)
def read_category(
    category_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    category = crud.get_category(session, category_id)
    raise_404_for_None(category)
    return category


@router.get("/list/{category_type}", response_model=List[schemas.CategoryRead])
def list_categories(
    category_type: schemas.CategoryType,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    categories = crud.get_categories(session, category_type)
    return categories
