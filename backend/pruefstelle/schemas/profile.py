from typing import Optional
from pydantic import BaseModel, NonNegativeInt, conint

from .mixins import WithID


class OneOrMoreInt(conint(ge=1)):
    pass


class FiftyOrMoreInt(conint(ge=50)):
    pass


class ProfileBase(BaseModel):
    # Order matters; the options are applied in this order
    keyword_only_top_n_relevance: NonNegativeInt = 0
    keyword_relevance_threshold: NonNegativeInt = 0
    keyword_confidence_threshold: NonNegativeInt = 0
    keyword_frequency_threshold: NonNegativeInt = 0
    research_quality_good_threshold: FiftyOrMoreInt = FiftyOrMoreInt(50)
    research_quality_constraint_needed_users: OneOrMoreInt = OneOrMoreInt(1)


class ProfileRead(WithID, ProfileBase):
    pass

    class Config:
        orm_mode = True


class ProfileCreate(BaseModel):
    keyword_relevance_threshold: Optional[NonNegativeInt] = 0
    keyword_confidence_threshold: Optional[NonNegativeInt] = 0
    keyword_frequency_threshold: Optional[NonNegativeInt] = 0
    keyword_only_top_n_relevance: Optional[NonNegativeInt] = 0
    research_quality_constraint_needed_users: Optional[OneOrMoreInt] = OneOrMoreInt(1)
    research_quality_good_threshold: Optional[FiftyOrMoreInt] = FiftyOrMoreInt(50)

    class Config:
        orm_mode = True


class ProfileUpdate(ProfileCreate):
    pass
