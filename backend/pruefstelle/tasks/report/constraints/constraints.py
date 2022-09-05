from typing import List, Callable, Tuple, Optional

from .... import schemas
from . import research_quality_constraints


ConstraintFunction = Callable[
    [int, schemas.Report],
    Tuple[Optional[schemas.Constraint], Optional[schemas.Constraint]],
]


def get_constraints(
    profile: schemas.ProfileRead,
) -> List[Tuple[ConstraintFunction, int]]:

    profile_dict = profile.dict()
    research_quality_constraints_prefix = "research_quality_constraint_"
    rq_constraints = [
        (
            getattr(research_quality_constraints, name),
            expected_value,
        )
        for name, expected_value in profile_dict.items()
        if name.startswith(research_quality_constraints_prefix)
    ]

    return rq_constraints


def apply_constraints(
    profile: schemas.ProfileRead,
    points_result_information: schemas.Report,
) -> schemas.Report:

    constraints = get_constraints(profile)

    for constraint, expected_value in constraints:
        failed_item_constraint, failed_option_constraint = constraint(
            expected_value, points_result_information
        )
        if failed_item_constraint is not None:
            points_result_information.item_results_failed_constraints.append(
                failed_item_constraint
            )
        if failed_option_constraint is not None:
            points_result_information.optioned_results_failed_constraints.append(
                failed_option_constraint
            )

    return points_result_information
