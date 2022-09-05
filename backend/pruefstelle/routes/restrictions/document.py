from uuid import UUID
from ... import database


def has_document_update_access(
    document: database.Document, current_user_id: UUID
) -> bool:
    if (len(document.cases) == 0) and (document.creator_id == current_user_id):
        return True
    return False


def has_document_delete_access(
    document: database.Document, current_user_id: UUID
) -> bool:
    return has_document_update_access(document, current_user_id)
