from typing import List, Set, Optional

from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, Query, HTTPException


from .. import schemas
from ..database.config import ActiveSession
from ..tasks import read_collection, import_documents
from ..tasks.errors import DUNotFoundError, MissingNeeededCategoryError

from ..security import AuthenticatedUser


router = APIRouter()


@router.post(
    "/fesad/excel_collection",
    response_model=List[schemas.DocumentRead],
)
async def import_documents_with_texts_from_fesad_excel_collection(
    *,
    session: Session = ActiveSession,
    excel_collection: UploadFile,
    services: Optional[Set[schemas.Service]] = Query(default=None),
    current_user: schemas.UserRead = AuthenticatedUser,
):
    """Import an excel collection as provided by FESAD to the database and return the created documents.

    Note:
    * `services` is applied to **all** imported texts
    * One `Job` (with status `DRAFT`) for every `service`is created.
    * `DRAFT` means that it is excluded from being run
        * [cf. here](/docs#/Mining%20Job/start_job_api_job__job_id__start_patch) to start the job
    * If you want to use the created documents in a case, you'll need to create one separately and attach the returned documents there.


    """
    FESADXlsMimeType = "application/vnd.ms-excel"

    if services is None:
        services = set()

    if excel_collection.content_type != FESADXlsMimeType:
        detail = f"Please upload a XLS file, file type '{excel_collection.content_type}' is not supported"
        raise HTTPException(400, detail=detail)

    try:
        document_informations = read_collection(excel_collection)
    except (ValueError, KeyError):
        detail = "Couldn't read excel collection file"
        raise HTTPException(status_code=400, detail=detail)
    if len(document_informations) == 0:
        return []

    try:
        imported_documents = import_documents(
            session, document_informations, current_user, services
        )
    except (MissingNeeededCategoryError, DUNotFoundError) as e:
        raise HTTPException(status_code=400, detail=e.name)

    return imported_documents
