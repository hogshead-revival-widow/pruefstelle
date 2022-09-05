from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter

from ..utils import raise_404_for_None
from ... import schemas
from ...database.config import ActiveSession
from ...database import crud

router = APIRouter()


@router.post("", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, session: Session = ActiveSession):
    try:
        new_user = crud.create_user(session, user)
    except crud.NotUniqueError:
        raise HTTPException(status_code=400, detail="Email address is already in use")
    return new_user


@router.patch("/{user_id}", response_model=schemas.UserRead)
def update_user(
    user_id: UUID, update: schemas.UserUpdate, session: Session = ActiveSession
):
    """
    Note:
    - `current_password` refers to your password
    """
    user = crud.get_user(session, user_id)
    raise_404_for_None(user)
    try:
        updated_user = crud.update_user_email(session, user, update)  # type: ignore
    except crud.NotUniqueError:
        raise HTTPException(status_code=400, detail="Email address is already in use")
    return updated_user
