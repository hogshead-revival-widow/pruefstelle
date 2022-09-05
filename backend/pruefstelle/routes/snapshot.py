from uuid import UUID
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter

from .. import schemas
from ..database.config import ActiveSession
from ..database import crud
from .utils import raise_404_for_None
from ..security import AuthenticatedUser

router = APIRouter()


@router.post("/{item_id}/{case_id}", response_model=schemas.SnapshotRead)
def create_snapshot(
    item_id: UUID,
    case_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    new_snapshot = crud.create_snapshot(session, item_id, case_id)
    raise_404_for_None(new_snapshot)
    return new_snapshot


@router.get("/{snapshot_id}", response_model=schemas.SnapshotRead)
def read_research_quality_snapshot(
    snapshot_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    snapshot = crud.get_snapshot(session, snapshot_id)
    raise_404_for_None(snapshot)
    return snapshot


@router.get("/list/{item_id}", response_model=List[schemas.SnapshotRead])
def list_snapshots_for_item(
    item_id: UUID,
    session: Session = ActiveSession,
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """List snapshots for item, newest first"""
    snapshots = crud.get_snapshots_for_item(session, item_id)
    return snapshots
