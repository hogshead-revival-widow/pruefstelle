import enum
from itertools import islice
from typing import Optional, Literal
from uuid import UUID

from pydantic import BaseModel, conset
from .mixins import WithDate, WithID
from ..external.mining.schemas import TextWorkflow, ProcessingStatus


class Status(str, enum.Enum):
    # TO_BE_CONFIRMED: job was temporarily created and may still be deleted by the user,
    #  i.e. this status forbids any interaction with external services
    DRAFT = "DRAFT"
    # TO_BE_STARTED: job  has been created and should be handed over to the service
    TO_BE_STARTED = "TO_BE_STARTED"
    # STARTED: job has been handed over, but there is no return yet
    STARTED = "WAITING_FOR_RETURN"
    # ERROR: somethign has gone wrong, but the mining service didn't fail (-> use failed)
    # i.e. the api may not be reachable
    ERROR = "NON_API_ERROR"
    # RESULTS_IN_DB: job has finished and
    RESULTS_IN_DB = "RESULTS_IN_DB"
    # all following: return values from mining api
    NEW = "NEW"
    RUNNING = "RUNNING"
    PARTIALLY_COMPLETED = "PARTIALLY_COMPLETED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    def is_completed(self) -> bool:
        is_completed = ["COMPLETED", "RESULTS_IN_DB"]
        return self.name in is_completed

    def has_error(self) -> bool:
        has_error = ["FAILED", "ERROR"]
        return self.name in has_error

    @classmethod
    def get_processing_status(cls):
        sliced = islice(cls, 5, 10)
        return [(member.name, member.value) for member in sliced]


# making sure all names and values of ProcessingStatus are in Status
# as an Enum can't be subclassed
assert Status.get_processing_status() == ProcessingStatus.get_processing_status()


Service = TextWorkflow

AtLeastOneService = conset(Service, min_items=1)


class JobBase(WithDate, BaseModel):
    status: Status
    service: Service
    external_id: Optional[str]
    item_id: UUID


class JobCreate(BaseModel):
    service: Service
    status: Literal[Status.DRAFT, Status.TO_BE_STARTED]
    item_id: UUID


class JobUpdate(BaseModel):
    status: Optional[Literal[Status.DRAFT, Status.TO_BE_STARTED]]


class JobRead(WithID, JobBase):
    # results: List[Result]
    pass

    class Config:
        orm_mode = True
