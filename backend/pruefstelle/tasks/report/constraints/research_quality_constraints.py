from typing import Optional, Tuple
from .... import schemas


def research_quality_constraint_needed_users(
    expected_value: int,
    points_result_information: schemas.Report,
) -> Tuple[Optional[schemas.Constraint], Optional[schemas.Constraint]]:

    constraint_name = "research_quality_constraint_needed_users"
    failed_item_constraint = None
    failed_option_constraint = None

    if points_result_information.item_results_min_unique_creators < expected_value:
        failed_item_constraint = schemas.Constraint(
            constraint_name=constraint_name,
            expected_value=expected_value,
            found_value=points_result_information.item_results_min_unique_creators,
        )

    if points_result_information.optioned_results_min_unique_creators < expected_value:
        failed_option_constraint = schemas.Constraint(
            constraint_name=constraint_name,
            expected_value=expected_value,
            found_value=points_result_information.optioned_results_min_unique_creators,
        )

    return failed_item_constraint, failed_option_constraint
