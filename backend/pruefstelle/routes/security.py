from pydantic import EmailStr
from fastapi import APIRouter, Depends, Response, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from .. import schemas
from ..database import crud
from ..database.config import ActiveSession

from ..security import (
    authenticate_user,
    get_user,
    COOKIE_NAME,
    set_cookie,
)

from ..security import magic_link

from .utils import raise_401_for_violation, raise_404_for_None
from ..tasks import send_magic_link

router = APIRouter()


@router.post("/logout")
def logout(response: Response):
    """Delete Cookie"""
    response.delete_cookie(COOKIE_NAME)
    return {"ok": True}


@router.post("/login", response_model=schemas.UserRead)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Get access cookie

    Note: Your email is your `username`
    """
    user = authenticate_user(get_user, EmailStr(form_data.username), form_data.password)
    is_authenticated = user is not False
    raise_401_for_violation(is_authenticated, detail="Invalid user or password")
    response.delete_cookie(COOKIE_NAME)
    await set_cookie(response, user)  # type: ignore

    return user


@router.post("/login_by_link", response_model=schemas.UserRead)
async def login_by_link(
    response: Response, token: str, session: Session = ActiveSession
):
    """Get access cookie by magic link"""

    user = magic_link.authenticate_by_link(session, token)
    authenticated = user is not None
    raise_401_for_violation(authenticated)
    response.delete_cookie(COOKIE_NAME)
    await set_cookie(response, user)  # type: ignore
    return user


@router.post("/send_login_link")
async def send_login_link(
    email: EmailStr, background_tasks: BackgroundTasks, session: Session = ActiveSession
):
    """Send login link to email"""
    user = crud.get_user_by_email(session, email)
    raise_404_for_None(user)
    token = magic_link.create_link_token(session, user_id=user.id, email=email)  # type: ignore
    background_tasks.add_task(send_magic_link, email, token)
    return {"ok": True}
