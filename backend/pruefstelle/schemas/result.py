from uuid import UUID
from typing import Union, Literal, List
from typing_extensions import Annotated
import enum
from decimal import Decimal

from pydantic import BaseModel, Field, validator

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


class TopicKeywordBase(BaseModel):
    keyword: str
    confidence: Decimal

    class Config:
        orm_mode = True


class TopicMappingBase(BaseModel):
    link: str = Field(alias="id")  # https://normdb.ivz.../vokabel/...
    terms: str
    score: Decimal

    @validator("terms", pre=True)
    def join(cls, v):
        if isinstance(v, list):
            return ", ".join(v)
        return v

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class TopicBase(BaseModel):
    given_topic_id: str = Field(alias="id")  # "123"
    confidence: Decimal
    keywords: List[TopicKeywordBase] = Field(alias="topic_keywords")
    mappings: List[TopicMappingBase] = Field(alias="topic_mappings")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class ResultBase(WithDate, WithID):
    item_id: UUID
    evaluations: List["EvaluationRead"]

    class Config:
        orm_mode = True


# making sure not to populate Topic and TopicMapping by alias
class TopicMappingRead(BaseModel):
    link: str
    terms: str
    score: Decimal

    class Config:
        orm_mode = True


class TopicRead(ResultBase):
    discriminator: Literal[ResultType.Topic]
    given_topic_id: str
    confidence: Decimal
    keywords: List[TopicKeywordBase]
    mappings: List[TopicMappingRead]

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
    Union[TopicRead, KeywordRead, NamedEntityRead], Field(discriminator="discriminator")
]


class ResultCreateBase(BaseModel):
    item_id: UUID


class NamedEntityCreate(NamedEntityBase, ResultCreateBase):
    discriminator: Literal[ResultType.NamedEntity]


class KeywordCreate(KeywordBase, ResultCreateBase):
    discriminator: Literal[ResultType.Keyword]


class TopicCreate(TopicBase, ResultCreateBase):
    discriminator: Literal[ResultType.Topic]


class ResultCreate(BaseModel):
    result: Union[KeywordCreate, NamedEntityCreate, TopicCreate] = Field(
        discriminator="discriminator"
    )

    @classmethod
    def from_result_base(
        cls,
        any_base_result: Union[TopicBase, KeywordBase, NamedEntityBase],
        item_id: UUID,
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

        if isinstance(any_base_result, TopicBase):
            result = TopicCreate(
                discriminator=ResultType.Topic,
                item_id=item_id,
                **any_base_result.dict()
            )

        if result is None:
            raise NotImplementedError()

        return ResultCreate(result=result)
