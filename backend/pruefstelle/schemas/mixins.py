from uuid import UUID
import datetime
import enum

from pydantic import BaseModel, constr, SecretStr


class Password(constr(min_length=1), SecretStr):
    pass


class Name(constr(min_length=1, max_length=255)):
    pass


class Date(str):
    pass


class Title(constr(min_length=1, max_length=255)):
    pass


class Content(constr(min_length=1, max_length=2000000)):
    pass


class Score(int, enum.Enum):
    BAD = 0
    OKAY = 1
    GOOD = 2


class Success(BaseModel):
    ok: bool


class WithDate(BaseModel):
    date: datetime.datetime


class WithCreator(BaseModel):
    creator_id: UUID


class WithTitle(BaseModel):
    title: Title


class WithTitleDate(WithDate, WithTitle):
    pass


class WithID(BaseModel):
    id: UUID


class IDRead(WithID):
    class Config:
        orm_mode = True


class IDTitleRead(WithID, WithTitle):
    class Config:
        orm_mode = True
