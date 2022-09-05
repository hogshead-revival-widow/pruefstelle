from uuid import UUID
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from ... import schemas
from ... import database
from ... import tasks

from .profile import create_profile, get_profile_from_case
from ..errors import raise_for_constraint_error


@raise_for_constraint_error
def create_snapshot(
    session: Session, item_id: UUID, case_id: UUID
) -> Optional[database.ResearchQualitySnapshot]:

    profile = get_profile_from_case(session, case_id)
    if profile is None:
        return None

    points = tasks.report.assemble_report_with_points(
        session, level=schemas.Level.ITEM, level_id=item_id, case_id=case_id
    )
    if len(points) != 1:
        return None
    points = points[0].points

    profile_snapshot = schemas.ProfileCreate.from_orm(profile)
    profile_snapshot = create_profile(session, profile_snapshot)

    new_snapshot = database.ResearchQualitySnapshot(points=points, item_id=item_id, profile_id=profile.id)  # type: ignore

    session.add(new_snapshot)
    session.commit()
    session.refresh(new_snapshot)
    return new_snapshot


def get_snapshot(
    session: Session, snapshot_id: UUID
) -> Optional[database.ResearchQualitySnapshot]:
    snapshot = session.get(database.ResearchQualitySnapshot, snapshot_id)
    return snapshot


@raise_for_constraint_error
def get_snapshots_for_item(
    session: Session, item_id: UUID
) -> List[database.ResearchQualitySnapshot]:
    statement = (
        select(database.ResearchQualitySnapshot)
        .where(database.ResearchQualitySnapshot.item_id == item_id)
        .order_by(database.ResearchQualitySnapshot.date.desc())
    )
    snapshots = session.execute(statement).scalars().all()
    return snapshots
