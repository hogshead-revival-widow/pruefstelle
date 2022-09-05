from typing import Optional, List, Set
from uuid import UUID
from pydantic import BaseModel

from .category import CategoryRead
from .profile import (
    ProfileRead,
    ProfileCreate,
)
from .document import DocumentReadWithoutCases
from .mixins import WithID, WithTitleDate, Title, IDRead


class CaseBase(WithTitleDate, BaseModel):
    pass


class CaseRead(WithID, CaseBase):
    original_case_id: Optional[UUID]
    category: CategoryRead
    profile: ProfileRead
    watchers: List[IDRead]
    documents: List[DocumentReadWithoutCases]

    class Config:
        orm_mode = True


class CaseCreate(BaseModel):
    title: Title
    category_id: UUID
    original_case_id: Optional[UUID] = None
    profile: ProfileCreate
    documents: Set[UUID]


class CaseUpdate(BaseModel):
    title: Title
    original_case_id: Optional[UUID]
    category_id: Optional[UUID]
    documents: Set[UUID]
