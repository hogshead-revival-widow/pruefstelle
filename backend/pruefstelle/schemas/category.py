from typing import Optional, Union, Literal
from typing_extensions import Annotated
from uuid import UUID
from pydantic import BaseModel, Field

from ..database import CategoryType
from .mixins import Name, WithID


class AnyCategory(BaseModel):
    discriminator: Literal[
        CategoryType.CaseCategory,
        CategoryType.DocumentCategory,
        CategoryType.SourceCategory,
        CategoryType.TextCategory,
    ]
    name: Name
    ndb_norm_id: Optional[int] = None


class ExternalIDCategory(BaseModel):
    discriminator: Literal[CategoryType.ExternalIDCategory]
    source_id: Optional[UUID] = None
    name: Name
    ndb_norm_id: Optional[int] = None


Category = Annotated[
    Union[AnyCategory, ExternalIDCategory], Field(discriminator="discriminator")
]

CategoryUpdate = Category
CategoryCreate = Category


class ChildCategoryRead(WithID):
    name: str
    discriminator: str
    ndb_norm_id: Optional[int] = None

    class Config:
        orm_mode = True


class CategoryRead(WithID):
    name: str
    source: Optional[ChildCategoryRead] = None
    discriminator: str
    ndb_norm_id: Optional[int] = None

    class Config:
        orm_mode = True
