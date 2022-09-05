from uuid import UUID
from typing import Optional, List, Union

from sqlalchemy import select, insert, or_
from sqlalchemy.orm import Session
from sqlalchemy_utils import escape_like

from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.sqlalchemy_future import paginate

from ... import schemas
from ... import database
from ..errors import raise_for_constraint_error, raise_for_wrong_category
from .shared import update_obj, delete_obj, establish_link
from .user import get_user


@raise_for_constraint_error
def create_case(
    session: Session, case: schemas.CaseCreate, creator_id: UUID
) -> database.Case:
    """
    Create a new case.
    """
    case_data = case.dict(exclude_unset=True)
    profile_data = case.profile.dict(exclude_unset=True)
    case_data.pop("documents", None)
    case_data.pop("profile", None)
    new_case = database.Case(**case_data, creator_id=creator_id)  # type: ignore
    new_case.profile = database.Profile(**profile_data)  # type: ignore

    raise_for_wrong_category(
        session, expected=database.CategoryType.CaseCategory, id=case.category_id
    )

    session.add(new_case)
    session.flush()

    add_creator_watcher = insert(database.Case.watchers_link_model).values(
        case_id=new_case.id,
        user_id=creator_id,
    )
    session.execute(add_creator_watcher)

    links = [
        {"case_id": new_case.id, "document_id": document_id}
        for document_id in case.documents
    ]
    link_model = database.Case.document_link_model
    establish_link(session, link_model, links)

    session.commit()
    session.refresh(new_case)
    return new_case


def get_case(session: Session, case_id: UUID) -> Optional[database.Case]:
    case = session.get(database.Case, case_id)
    return case


def get_case_ids(
    session: Session, with_pagination=False
) -> Union[AbstractPage[UUID], List[UUID]]:

    statement = select(database.Case.id)

    if with_pagination:
        return paginate(session, statement)

    ids = session.execute(statement).scalars().all()
    return ids


def get_cases(
    session: Session, with_pagination=False
) -> Union[AbstractPage[database.Case], List[database.Case]]:
    statement = select(database.Case).order_by(database.Case.date.desc())
    if with_pagination:
        return paginate(session, statement)

    cases = session.execute(statement).scalars().all()
    return cases


def get_cases_by_watcher_id(
    session: Session, watcher_id: UUID, with_pagination=False
) -> Union[AbstractPage[database.Case], List[database.Case]]:
    statement = (
        select(database.Case)
        .join(database.Case.watchers_link_model)
        .where(database.Case.watchers_link_model.c.user_id == watcher_id)
        .order_by(database.Case.date.desc())
    )
    if with_pagination:
        return paginate(session, statement)

    cases = session.execute(statement).scalars().all()
    return cases


def search_cases(
    session: Session,
    title: Optional[str],
    category_name: Optional[str],
    with_pagination=False,
) -> Union[AbstractPage[UUID], List[UUID]]:

    statement = select(database.Case.id).order_by(database.Case.date.desc())

    conditions = list()
    if title is not None:
        conditions.append(database.Case.title.ilike(f"%{escape_like(title)}%"))

    if category_name is not None:
        statement = statement.join(database.Category)
        conditions.append(
            database.Category.name.ilike(f"%{escape_like(category_name)}%")
        )

    statement = statement.where(or_(*conditions))
    if with_pagination:
        return paginate(session, statement)

    cases = session.execute(statement).scalars().all()
    return cases


def get_case_item_ids(session: Session, case_id: UUID) -> List[UUID]:

    statement = select(database.Case.document_link_model.c.document_id).where(
        database.Case.document_link_model.c.case_id == case_id
    )
    document_ids = session.execute(statement).scalars().all()

    statement = select(database.Item.id).where(
        database.Item.document_id.in_(document_ids)
    )

    item_ids = session.execute(statement).scalars().all()

    return item_ids


def get_profile_from_case_id(
    session: Session, case_id: UUID
) -> Optional[database.Profile]:
    profile_id = session.execute(
        select(database.Case.profile_id).where(database.Case.id == case_id)
    ).scalar()
    profile = session.get(database.Profile, profile_id)
    return profile


def update_case(
    session: Session, case: database.Case, update: schemas.CaseUpdate
) -> database.Case:

    raise_for_wrong_category(
        session,
        database.CategoryType.CaseCategory,
        update.category_id,
        ignore_None=True,
    )
    patch = update.dict(exclude_unset=True)

    if "documents" in patch:
        links = [
            {"case_id": case.id, "document_id": document_id}
            for document_id in patch["documents"]
        ]
        link_model = database.Case.document_link_model
        establish_link(session, link_model, links)
        del patch["documents"]

    return update_obj(session, case, patch)


def delete_case(session: Session, case: database.Case) -> database.Case:
    return delete_obj(session, case)


def toggle_watch_case(
    session: Session, case_id: UUID, user_id: UUID
) -> Optional[database.Case]:
    case = get_case(session, case_id=case_id)
    if case is None:
        return None
    user = get_user(session, user_id=user_id)
    if user is None:
        return None

    if user in case.watchers:  # type: ignore
        return unwatch_case(session, case, user)
    return watch_case(session, case, user)


def watch_case(
    session: Session, case: database.Case, user: database.User
) -> Optional[database.Case]:
    case.watchers.append(user)
    session.add(case)
    session.commit()
    session.refresh(case)
    return case


def unwatch_case(
    session: Session, case: database.Case, user: database.User
) -> Optional[database.Case]:
    case.watchers.remove(user)
    session.add(case)
    session.commit()
    session.refresh(case)
    return case
