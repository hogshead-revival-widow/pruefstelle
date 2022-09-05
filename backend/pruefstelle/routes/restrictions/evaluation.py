from uuid import UUID
from ... import database


def has_evaluation_update_access(
    evaluation: database.Evaluation, current_user_id: UUID
) -> bool:
    if evaluation.creator_id == current_user_id:
        return True
    return False


def has_evaluation_delete_access(
    evaluation: database.Evaluation, current_user_id: UUID
) -> bool:
    return has_evaluation_update_access(evaluation, current_user_id)
