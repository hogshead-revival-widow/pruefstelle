from typing import List, Optional, Dict
import enum
from uuid import UUID

from pydantic import BaseModel, PositiveInt, conset
from ...schemas.mixins import Content, Title
from ...schemas.document import DocumentCreate
from ...schemas.text import TextCreate

DUKey = PositiveInt

DUKeys = conset(DUKey, min_items=1)


class FESADTextCategory(str, enum.Enum):
    SPEAKER = "Sprecher:innentext"
    PR = "Pressetext"
    INTERNET = "Internettext"
    MODERATION = "Moderationstext"
    MANUSCRIPT = "Manuskript"
    WORD = "O-Ton"
    CONTENT = "Sachinhalt"

    @classmethod
    def to_list(cls) -> List[str]:
        return [item.value for item in cls]


class ImportableText(BaseModel):
    content: Content
    category: FESADTextCategory
    category_id: Optional[UUID] = None

    @classmethod
    def from_fesad(cls, text: Dict[str, str]) -> Optional["ImportableText"]:
        "Check if it makes sense to import a text and if so, make the category readable"
        if "content" not in text or "type" not in text:
            return None
        fesad_type: int = int(text["type"])
        if not cls._is_wanted(fesad_type):
            return None
        map_fesad_text_type_to_category = {
            1: FESADTextCategory.CONTENT,
            3: FESADTextCategory.WORD,
            6: FESADTextCategory.PR,
            7: FESADTextCategory.MANUSCRIPT,
            8: FESADTextCategory.MODERATION,
            9: FESADTextCategory.SPEAKER,
            10: FESADTextCategory.INTERNET,
        }

        category = map_fesad_text_type_to_category[fesad_type]
        content = Content(text["content"].strip())
        return cls(content=content, category=category)

    @staticmethod
    def _is_wanted(fesad_type: PositiveInt) -> bool:
        import_these_types = [1, 3, 6, 7, 8, 9, 10]
        return fesad_type in import_these_types

    def to_text_create(
        self, category_id: UUID, source_category_id: UUID, document_id: UUID
    ) -> TextCreate:
        return TextCreate(
            content=self.content,
            category_id=category_id,
            source_category_id=source_category_id,
            document_id=document_id,
            parents=set(),
        )


class ImportableDocument(BaseModel):
    name: str
    du_key: PositiveInt
    texts: List[ImportableText]
    category_id: Optional[UUID] = None

    def to_document_create(
        self, category_id: UUID, external_id_category_id: UUID
    ) -> DocumentCreate:
        return DocumentCreate(
            title=Title(self.name[:50]),
            category_id=category_id,
            external_id=str(self.du_key),
            external_id_category_id=external_id_category_id,
            cases=set(),
        )
