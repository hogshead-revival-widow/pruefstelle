from pydantic import EmailStr
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm


from .. import schemas
from ..security import (
    authenticate_user,
    get_user,
    COOKIE_NAME,
    set_cookie,
)
from .utils import raise_401_for_violation


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
