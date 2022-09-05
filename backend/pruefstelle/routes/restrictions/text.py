from uuid import UUID
from ... import database


def has_text_update_access(text: database.Text, current_user_id: UUID) -> bool:
    if (text.creator_id == current_user_id) and (len(text.document.cases) == 0):
        return True
    return False


def has_text_delete_access(text: database.Text, current_user_id: UUID) -> bool:
    return has_text_update_access(text, current_user_id)
