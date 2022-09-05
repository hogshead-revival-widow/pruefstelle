from typing import Optional, List, Set
from uuid import UUID
from pydantic import BaseModel

from .category import CategoryRead
from .mixins import WithID, WithTitleDate, Title, IDTitleRead
from .item import ItemRead


class DocumentBase(WithTitleDate, BaseModel):
    category: CategoryRead
    external_id: Optional[str]
    external_id_category: Optional[CategoryRead]
    items: List[ItemRead]


class DocumentRead(WithID, DocumentBase):
    cases: List[IDTitleRead]

    class Config:
        orm_mode = True


class DocumentReadWithoutCases(WithID, DocumentBase):
    class Config:
        orm_mode = True


class DocumentCreate(BaseModel):
    title: Title
    category_id: UUID
    external_id: Optional[str]
    external_id_category_id: Optional[UUID]
    cases: Set[UUID]


class DocumentUpdate(BaseModel):
    title: Optional[Title]
    category_id: Optional[UUID]
    external_id: Optional[str]
    external_id_category_id: Optional[UUID]
