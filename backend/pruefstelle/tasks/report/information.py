from typing import List, Tuple, Dict
from uuid import UUID
from decimal import Decimal

import statistics

from ... import schemas
from ..errors import PointsError
from .constraints import apply_constraints


def get_min_unique_creators(item_results: List[schemas.ResultRead]) -> int:

    unique_creators = set(
        map(
            lambda result: len(
                set(map(lambda evaluation: evaluation.creator_id, result.evaluations))
            ),
            item_results,
        )
    )

    if len(unique_creators) == 0:
        return 0
    return min(unique_creators)


def get_all_evaluated(item_results: List[schemas.ResultRead]) -> bool:
    return all(len(result.evaluations) > 0 for result in item_results)


def calculate_points(medians: List[int], total: int) -> Decimal:
    """
    Calculate points (e.g. percentage of results evaluated as good / total results)

    Raise `PointError` if the amount of medians are not equal to `total`
    """

    if total != len(medians):
        raise PointsError(
            "Aborted point calculation, because of missing evaluation medians"
        )

    total_good = sum(medians)
    quotient = total_good / total
    points = quotient * 100
    points = Decimal(f"{points:.2f}")

    return points


def calculate_medians(results: List[schemas.ResultRead]) -> List[int]:
    """
    Calculate median evaluation per result.

    Raises `PointError` if not all items have been evaluated
    """

    if any(len(result.evaluations) == 0 for result in results):
        raise PointsError("Can't calculate median for results without evaluations")

    medians = list()
    for result in results:
        median = statistics.median(
            map(lambda evaluation: int(evaluation.is_good), result.evaluations)
        )
        medians.append(median)
    return medians


def get_report_information(
    profile: schemas.ProfileRead,
    item_id: UUID,
    item_results: List[schemas.ResultRead],
    optioned_results: List[schemas.ResultRead],
) -> Tuple[int, schemas.Report]:

    profile_id = profile.id
    results_included_in_point_calculation = {result.id for result in optioned_results}
    total = len(results_included_in_point_calculation)

    item_results_total = len(item_results)
    item_results_all_evaluated = get_all_evaluated(item_results)
    item_results_min_unique_creators = get_min_unique_creators(item_results)

    optioned_results_total = len(optioned_results)
    optioned_results_all_evaluated = get_all_evaluated(optioned_results)
    optioned_results_min_unique_creators = get_min_unique_creators(optioned_results)
    optioned_results_by_id = [result.id for result in optioned_results]

    item_results_ignored_by_option = item_results_total - optioned_results_total

    item_results_failed_constraints = list()
    optioned_results_failed_constraints = list()

    pointinformation_without_checked_constraints = schemas.Report(
        item_id=item_id,
        profile_id=profile_id,
        item_results=item_results,
        item_results_total=item_results_total,
        item_results_min_unique_creators=item_results_min_unique_creators,
        item_results_all_evaluated=item_results_all_evaluated,
        optioned_results_min_unique_creators=optioned_results_min_unique_creators,
        optioned_results_all_evaluated=optioned_results_all_evaluated,
        optioned_results_total=optioned_results_total,
        optioned_results_by_id=optioned_results_by_id,
        item_results_ignored_by_option=item_results_ignored_by_option,
        item_results_failed_constraints=item_results_failed_constraints,
        optioned_results_failed_constraints=optioned_results_failed_constraints,
    )

    pointinformation_with_checked_constraints = apply_constraints(
        profile, pointinformation_without_checked_constraints
    )

    return total, pointinformation_with_checked_constraints


def make_report(
    profile: schemas.ProfileRead,
    item_id: UUID,
    # results before options have been applied
    item_results: List[schemas.ResultRead],
    # results after options have been applied
    optioned_results: List[schemas.ResultRead],
) -> schemas.ReportWithPoints:

    total, result_information = get_report_information(
        profile,
        item_id,
        item_results,
        optioned_results,
    )
    points = Decimal(0)
    item_results_calculation_conditions_met = (
        total > 0 and result_information.item_results_all_evaluated
    )
    optioned_results_calculation_conditions_met = (
        total > 0 and result_information.optioned_results_all_evaluated
    )

    if optioned_results_calculation_conditions_met:
        medians = calculate_medians(results=optioned_results)
        points = calculate_points(medians, total)

    return schemas.ReportWithPoints(
        points=points,
        item_results_calculation_conditions_met=item_results_calculation_conditions_met,
        optioned_results_calculation_conditions_met=optioned_results_calculation_conditions_met,
        **result_information.dict(),
    )


def collect_reports(
    profile: schemas.ProfileRead,
    results_by_item_id: Dict[UUID, List[schemas.ResultRead]],
    optioned_results_by_item_id: Dict[UUID, List[schemas.ResultRead]],
) -> List[schemas.ReportWithPoints]:

    reports = list()

    for item_id, optioned_results in optioned_results_by_item_id.items():
        item_results = results_by_item_id[item_id]

        item_reports = make_report(
            profile=profile,
            item_id=item_id,
            item_results=item_results,
            optioned_results=optioned_results,
        )

        reports.append(item_reports)

    return reports
