from uuid import UUID
from ... import database


def has_case_update_access(case: database.Case, current_user_id: UUID) -> bool:
    if (len(case.documents) == 0) and (case.creator_id == current_user_id):
        return True
    return False


def has_case_delete_access(case: database.Case, current_user_id: UUID) -> bool:
    return has_case_update_access(case, current_user_id)
