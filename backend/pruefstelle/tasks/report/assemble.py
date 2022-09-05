from typing import List, Dict
from uuid import UUID


from sqlalchemy.orm import Session
from pydantic import parse_obj_as

from ..errors import PointsError
from .information import collect_reports
from ...database import crud
from ... import schemas
from .options import apply_options


def get_results(
    session: Session, item_ids: List[UUID]
) -> Dict[UUID, List[schemas.ResultRead]]:

    all_results = crud.get_results_for_item(session, item_ids)
    result_dict = dict()
    for result in all_results:
        result = parse_obj_as(schemas.ResultRead, result)
        result_dict.setdefault(result.item_id, list()).append(result)  # type: ignore

    # include items that have no results
    items_with_results = result_dict.keys()
    items_without_results = (
        item_id for item_id in item_ids if item_id not in items_with_results
    )
    for item_id in items_without_results:
        result_dict[item_id] = list()

    return result_dict


def get_item_ids(session: Session, level: schemas.Level, level_id: UUID) -> List[UUID]:
    item_ids = list()
    if level == schemas.Level.ITEM:
        item_ids = [level_id]
    if level == schemas.Level.CASE:
        item_ids = crud.get_case_item_ids(session, level_id)
    if level == schemas.Level.DOCUMENT:
        item_ids = crud.get_document_item_ids(session, level_id)
    if len(item_ids) == 0:
        raise PointsError("Items not found")
    return item_ids


def get_profile(session: Session, case_id) -> schemas.ProfileRead:
    profile = crud.get_profile_from_case_id(session, case_id)
    if profile is None:
        raise PointsError("Profile not found")

    profile = schemas.ProfileRead.from_orm(profile)

    return profile


def assemble_report_with_points(
    session: Session,
    level: schemas.Level,
    level_id: UUID,
    case_id: UUID,
) -> List[schemas.ReportWithPoints]:
    """
    Assemble report

    Raises `PointError` if:
    - no items have been found (via `get_items_id`)
    - no profile has been found (via `get_profile`)
    """

    item_ids = get_item_ids(session, level, level_id)
    profile = get_profile(session, case_id)
    results_by_item_id = get_results(session, item_ids)

    optioned_results_by_item_id = apply_options(profile, results_by_item_id)

    reports = collect_reports(profile, results_by_item_id, optioned_results_by_item_id)

    return reports
