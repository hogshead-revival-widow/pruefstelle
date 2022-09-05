import uuid
import datetime

from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import (
    declarative_mixin,
    declared_attr,
    has_inherited_table,
    relationship,
)
from sqlalchemy_utils import UUIDType

from .utils import camel_to_snake


@declarative_mixin
class WithTablename:
    @declared_attr
    def __tablename__(cls):
        if has_inherited_table(cls):  # type: ignore
            return None
        return camel_to_snake(cls.__name__)  # type: ignore


@declarative_mixin
class WithID:
    id = Column(
        UUIDType(binary=False),
        primary_key=True,
        index=True,
        nullable=False,
        default=uuid.uuid4,
    )


@declarative_mixin
class WithTitle:
    title = Column(String(255), nullable=False)


@declarative_mixin
class WithDate:
    date = Column(
        DateTime,
        default=datetime.datetime.now,
        nullable=False,
        onupdate=datetime.datetime.now,
    )


@declarative_mixin
class WithCreator:
    @declared_attr
    def creator(cls):
        return relationship("User", uselist=False)

    @declared_attr
    def creator_id(cls):
        return Column(ForeignKey("user.id"), nullable=False)


@declarative_mixin
class WithIDTitleDateCreator(WithID, WithTitle, WithDate, WithCreator):
    pass
