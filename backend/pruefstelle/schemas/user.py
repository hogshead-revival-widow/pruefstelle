from typing import Optional

from pydantic import BaseModel, EmailStr, validator
from passlib.context import CryptContext

from .mixins import WithID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashedPassword(str):
    """Takes a plain text password and hashes it."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Accepts a plain text password and returns a hashed password."""
        if not isinstance(v, str):
            raise TypeError("string required")

        hashed_password = pwd_context.hash(v)
        return cls(hashed_password)


class UserBase(BaseModel):
    email: EmailStr
    superuser: bool

    @validator("email", pre=True)
    def email_to_lower(cls, v):
        if isinstance(v, (str, EmailStr)):
            return v.lower()
        return v


class UserRead(WithID, UserBase):
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: "HashedPassword"

    @validator("email", pre=True)
    def email_to_lower(cls, v):
        if isinstance(v, (str, EmailStr)):
            return v.lower()
        return v


class UserUpdate(BaseModel):
    current_password: str
    email: Optional[EmailStr]
    new_password: Optional[HashedPassword]

    @validator("email", pre=True)
    def email_to_lower(cls, v):
        if isinstance(v, (str, EmailStr)):
            return v.lower()
        return v
