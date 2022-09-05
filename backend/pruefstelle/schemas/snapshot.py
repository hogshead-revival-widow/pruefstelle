from uuid import UUID
from decimal import Decimal


from .mixins import WithID, WithDate
from .profile import ProfileRead


class SnapshotBase(WithDate):
    points: Decimal
    item_id: UUID


class SnapshotRead(WithID, SnapshotBase):
    profile: ProfileRead

    class Config:
        orm_mode = True


class SnapshotReadWithoutProfile(WithID, SnapshotBase):
    class Config:
        orm_mode = True
