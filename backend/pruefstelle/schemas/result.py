from uuid import UUID
from typing import Union, Literal, List
from typing_extensions import Annotated
import enum
from decimal import Decimal

from pydantic import BaseModel, Field

from ..database import ResultType, Keyword, NamedEntity
from .mixins import WithDate, WithID


from .evaluation import EvaluationRead


class NamedEntityType(str, enum.Enum):
    PERSON = "PERSON"
    LOCATION = "LOCATION"
    ORGANIZATION = "ORGANIZATION"


class KeywordBase(BaseModel):
    keyword: str
    relevance: Decimal
    frequency: int
    confidence: Decimal

    def is_same(self, other: Keyword) -> bool:
        return self.keyword == other.keyword


class NamedEntityBase(BaseModel):
    type: NamedEntityType
    label: str
    begin: int
    end: int

    def is_same(self, other: NamedEntity) -> bool:
        return (self.label == other.label) and (self.type == other.type)


class ResultBase(WithDate, WithID):
    item_id: UUID
    evaluations: List["EvaluationRead"]

    class Config:
        orm_mode = True


class NamedEntityRead(NamedEntityBase, ResultBase):
    discriminator: Literal[ResultType.NamedEntity]

    class Config:
        orm_mode = True


class KeywordRead(KeywordBase, ResultBase):
    discriminator: Literal[ResultType.Keyword]

    class Config:
        orm_mode = True


ResultRead = Annotated[
    Union[KeywordRead, NamedEntityRead], Field(discriminator="discriminator")
]


""" only temp """


class ResultCreateBase(BaseModel):
    item_id: UUID


class NamedEntityCreate(NamedEntityBase, ResultCreateBase):
    discriminator: Literal[ResultType.NamedEntity]


class KeywordCreate(KeywordBase, ResultCreateBase):
    discriminator: Literal[ResultType.Keyword]


class ResultCreate(BaseModel):
    result: Union[KeywordCreate, NamedEntityCreate] = Field(
        discriminator="discriminator"
    )

    @classmethod
    def from_result_base(
        cls, any_base_result: Union[KeywordBase, NamedEntityBase], item_id: UUID
    ):

        result = None

        if isinstance(any_base_result, KeywordBase):
            result = KeywordCreate(
                discriminator=ResultType.Keyword,
                item_id=item_id,
                **any_base_result.dict()
            )
        if isinstance(any_base_result, NamedEntityBase):
            result = NamedEntityCreate(
                discriminator=ResultType.NamedEntity,
                item_id=item_id,
                **any_base_result.dict()
            )

        if result is None:
            raise NotImplementedError()

        return ResultCreate(result=result)
