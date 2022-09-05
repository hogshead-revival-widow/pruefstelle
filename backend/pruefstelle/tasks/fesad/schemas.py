from typing import Optional
from uuid import UUID
from pydantic import PositiveInt, BaseModel


class DocumentInformation(BaseModel):
    du_key: PositiveInt
    name: Optional[str] = None
    category_id: Optional[UUID] = None
    # todo: subject_area
