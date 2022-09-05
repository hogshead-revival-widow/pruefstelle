from uuid import UUID
from typing import Optional, Set
from pydantic import BaseModel

from .mixins import Content
from .item import TextRead  # noqa: F401


class TextCreate(BaseModel):
    content: Content
    document_id: UUID
    source_category_id: UUID
    category_id: UUID
    parents: Set[UUID]


class TextUpdate(BaseModel):
    source_category_id: Optional[UUID]
    category_id: Optional[UUID]
    document_id: Optional[UUID]
