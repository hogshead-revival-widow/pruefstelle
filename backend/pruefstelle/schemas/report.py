from decimal import Decimal
from typing import List

from uuid import UUID
import enum
from pydantic import BaseModel, NonNegativeInt

from .result import ResultRead


class Level(str, enum.Enum):
    ITEM = "item"
    DOCUMENT = "document"
    CASE = "case"


class Constraint(BaseModel):
    constraint_name: str
    expected_value: int
    found_value: int

    class Config:
        orm_mode = True


class Points(BaseModel):
    # research quality points
    points: Decimal
    # true if all calculation pre-conditions (very item has been evaluated at least once and there is at least one item) have been met
    item_results_calculation_conditions_met: bool
    # see above, but regarding only optioned results; points are only generated if this equals True
    optioned_results_calculation_conditions_met: bool

    class Config:
        orm_mode = True


class Report(BaseModel):
    item_id: UUID
    profile_id: UUID
    # _all_ results
    item_results: List[ResultRead]
    # amount of all results
    item_results_total: NonNegativeInt
    # Minimmal unique evaluation creators for all fundamental items (e.g. keywords) for item
    # i.e.: If there is any evaluation with only one unique creator, `min_unique_creators` is `1`
    item_results_min_unique_creators: NonNegativeInt
    #  see above
    optioned_results_min_unique_creators: NonNegativeInt
    # True, if _all_ results have been evaluated at least once
    item_results_all_evaluated: bool
    # True, if _all_ optioned results have been evaluated at least once
    optioned_results_all_evaluated: bool
    # amount of results that an option asked to ignore in point calculation
    optioned_results_total: NonNegativeInt
    # id of results included in points calculation
    optioned_results_by_id: List[UUID]
    # ignored results
    item_results_ignored_by_option: NonNegativeInt
    # e.g. <research_quality_constraint_needed_users>
    item_results_failed_constraints: List[Constraint]
    optioned_results_failed_constraints: List[Constraint]

    class Config:
        orm_mode = True


class ReportWithPoints(Report, Points):
    class Config:
        orm_mode = True
