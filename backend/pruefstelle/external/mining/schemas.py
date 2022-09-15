import enum
from typing import List, Union
from uuid import UUID

from pydantic import BaseModel, AnyHttpUrl

from ...schemas.result import KeywordBase, NamedEntityBase, TopicBase
from ...schemas.mixins import Content


"""
Simple Models
"""


class Immutable(BaseModel):
    class Config:
        allow_mutation = False


class TextWorkflow(str, enum.Enum):
    KEYWORD_EXTRACTION = "keyword-extraction"
    NAMED_ENTITY_RECOGNITION = "named-entity-recognition"
    # NAMED_ENTITY_LINKING = "named-entity-linking"
    TOPIC = "topic-modeling"

    @classmethod
    def to_list(cls) -> List[str]:
        return [text_workflow for text_workflow in cls]


class Language(str, enum.Enum):
    DE = "de"
    EN = "en"


class ProcessingStatus(str, enum.Enum):
    NEW = "NEW"
    RUNNING = "RUNNING"
    PARTIALLY_COMPLETED = "PARTIALLY_COMPLETED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    @classmethod
    def get_processing_status(cls):
        return [(member.name, member.value) for member in cls]


MiningResult = Union["ResultKeywords", "ResultNamedEntities"]

"""
Complex Models
"""


class TextOrder(Immutable):
    """Represents a mining job that can be sent to the mining platform."""

    text: Content


class TextOrderParams(Immutable):
    """Query Parameter for a new mining job with text"""

    language: Language = Language.DE


class OrderReceipt(Immutable):
    """Receipt for a mining job. `order_id` identifies the job."""

    order_id: UUID
    orders_url: AnyHttpUrl


class OrderStatus(Immutable):
    """Receipt for a mining job. `order_id` identifies the job."""

    order_id: UUID
    # The external_id is a value set by the MiningApi
    external_id: str
    processing_status: ProcessingStatus


class ResultBase(Immutable):
    order_id: UUID


class ResultKeywords(ResultBase):
    """Mined keywords"""

    keywords: List[KeywordBase]

    def get_items(self):
        return self.keywords


class ResultNamedEntities(ResultBase):
    """Mined entities"""

    named_entities: List[NamedEntityBase]

    def get_items(self):
        return self.named_entities


class ResultTopics(ResultBase):
    """Mined entities"""

    topics: List[TopicBase]

    def get_items(self):
        return self.topics
