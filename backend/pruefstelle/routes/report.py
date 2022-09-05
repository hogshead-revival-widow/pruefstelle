from uuid import UUID
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Query

from .utils import raise_404_for_None

from .. import schemas
from ..database import crud
from ..database.config import ActiveSession
from ..tasks.report import assemble_report_with_points, PointsError
from ..security import AuthenticatedUser


router = APIRouter()


@router.get("/case/{case_id}", response_model=List[schemas.ReportWithPoints])
def read_case_report(
    case_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """Points for all items (e.g.texts)  of a case"""

    try:
        reports_with_points = assemble_report_with_points(
            session,
            level=schemas.Level.CASE,
            level_id=case_id,
            case_id=case_id,
        )
    except PointsError as e:
        raise HTTPException(status_code=400, detail=e.name)

    return reports_with_points


@router.get(
    "/case/{case_id}/document/{document_id}",
    response_model=List[schemas.ReportWithPoints],
)
def read_document_report(
    document_id: UUID,
    case_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """Points for all items (e.g.texts)  of a document"""
    try:
        reports_with_points = assemble_report_with_points(
            session,
            level=schemas.Level.DOCUMENT,
            level_id=document_id,
            case_id=case_id,
        )
    except PointsError as e:
        raise HTTPException(status_code=400, detail=e.name)

    raise_404_for_None(reports_with_points)
    return reports_with_points


@router.get("/case/{case_id}/item/{item_id}", response_model=schemas.ReportWithPoints)
def read_item_report(
    item_id: UUID,
    case_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """Points for item (e.g. a text)"""
    try:
        report_with_point = assemble_report_with_points(
            session,
            level=schemas.Level.ITEM,
            level_id=item_id,
            case_id=case_id,
        )[0]
    except PointsError as e:
        raise HTTPException(status_code=400, detail=e.name)
    raise_404_for_None(report_with_point)
    return report_with_point


@router.get("/profile/{profile_id}", response_model=schemas.ProfileRead)
def read_profile(
    profile_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):

    profile = crud.get_profile(session, profile_id)
    raise_404_for_None(profile)
    return profile


@router.patch("/profile/{profile_id}", response_model=schemas.ProfileRead)
def update_profile(
    profile_id: UUID,
    update: schemas.ProfileUpdate,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):

    profile = crud.get_profile(session, profile_id)
    raise_404_for_None(profile)
    profile = crud.update_profile(session, profile, update)  # type: ignore
    return profile


@router.get("/profile/{case_id}/case", response_model=schemas.ProfileRead)
def read_profile_from_case(
    case_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    profile = crud.get_profile_from_case_id(session, case_id)
    raise_404_for_None(profile)
    return profile


@router.patch("/case/profile/{case_id}", response_model=schemas.ProfileRead)
def update_profile_from_case(
    case_id: UUID,
    update: schemas.ProfileUpdate,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):

    profile = crud.get_profile(session, case_id)
    raise_404_for_None(profile)
    profile = crud.update_profile(session, profile, update)  # type: ignore
    return profile
