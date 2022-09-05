from uuid import UUID
from typing import List, Annotated, Union, Literal, Set

from pydantic import BaseModel, Field

from .category import CategoryRead
from .mixins import WithDate, Content, WithTitle
from .snapshot import SnapshotReadWithoutProfile
from .result import ResultRead
from .job import JobRead


class ItemBase(WithDate):
    document_id: UUID
    source_category: CategoryRead
    parents: Set[UUID]
    mining_results: List[ResultRead]
    mining_jobs: List[JobRead]
    research_quality_snapshots: List[SnapshotReadWithoutProfile]

    class Config:
        orm_mode = True


class TextRead(ItemBase, WithTitle):
    content: Content
    category: CategoryRead
    discriminator: Literal["text"]
    item_id: UUID = Field(alias="id")

    class Config:
        orm_mode = True


class AnyItemRead(ItemBase):
    id: UUID
    discriminator: Literal["item"]

    class Config:
        orm_mode = True


# Right now, the only table inheriting from Item is Text
# And because doesnt support a discriminator union with only one type
# AnyItemRead is used as a placeholder
ItemRead = Annotated[Union[TextRead, AnyItemRead], Field(discriminator="discriminator")]
