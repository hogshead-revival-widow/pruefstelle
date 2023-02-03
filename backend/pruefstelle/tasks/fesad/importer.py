from typing import List, Set, Optional, Tuple


from sqlalchemy.orm import Session

from ...database import crud
from ... import schemas
from ... import database


from ...external.fesad import DocumentImporter, ImportableDocument
from ...external.fesad.schemas import FESADTextCategory
from ...external.errors import ApiError


from ..errors import DUNotFoundError, MissingNeeededCategoryError
from .schemas import DocumentInformation

importer = DocumentImporter()

NeededCategories = Tuple[
    database.DocumentCategory,
    database.SourceCategory,
    database.ExternalIDCategory,
    List[database.TextCategory],
]


def get_needed_categories(session: Session) -> NeededCategories:

    category_type = schemas.CategoryType.DocumentCategory
    name = "Sonstiges"
    document_category: Optional[database.DocumentCategory] = crud.get_category_by_name(
        session, name, category_type
    )  # type: ignore
    if document_category is None:
        raise MissingNeeededCategoryError(f"Needed category `{name}` not found")

    category_type = schemas.CategoryType.SourceCategory
    name = "FESAD"
    source_category: Optional[database.SourceCategory] = crud.get_category_by_name(
        session, name, category_type
    )  # type: ignore
    if source_category is None:
        raise MissingNeeededCategoryError(f"Needed category `{name}` not found")

    category_type = schemas.CategoryType.ExternalIDCategory
    name = "DU-Key"
    external_id_category: Optional[
        database.ExternalIDCategory
    ] = crud.get_category_by_name(
        session, name, category_type
    )  # type: ignore
    if external_id_category is None:
        raise MissingNeeededCategoryError(f"Needed category `{name}` not found")

    fesad_text_categories = FESADTextCategory.to_list()
    text_categories: List[database.TextCategory] = crud.get_categories_by_name(
        session, fesad_text_categories, schemas.CategoryType.TextCategory
    )  # type: ignore
    if len(text_categories) != len(fesad_text_categories):
        missing = len(fesad_text_categories) - len(text_categories)
        raise MissingNeeededCategoryError(f"{missing} needed text categories not found")

    return document_category, source_category, external_id_category, text_categories


def get_documents(
    document_informations: List[DocumentInformation],
) -> List[ImportableDocument]:
    importable_documents = list()
    for document_information in document_informations:
        try:
            importable_document = importer.get_document(info=document_information)
            if importable_document is not None:
                importable_documents.append(importable_document)
        except ApiError:
            failed_du_key = document_information.du_key
            error = f"Didn't find at least one DU. Failed with DU-Key: {failed_du_key}"
            raise DUNotFoundError(error)
    return importable_documents


def import_documents(
    session: Session,
    document_informations: List[DocumentInformation],
    current_user: schemas.UserRead,
    services: Set[schemas.Service],
) -> List[schemas.DocumentRead]:
    """
    Import document (based on `document_information`) from FESAD to database.

    Raises:
    - `MissingNeeededCategoryError` if a needed category is not found (in `get_needed_categories`)
    - `DUNotFoundError` if there was any APIError while requesting a DU's information from FESAD (in `get_documents`)
    """

    importable_documents = get_documents(document_informations)
    if len(importable_documents) == 0:
        return importable_documents  # type: ignore

    (
        document_category,
        source_category,
        external_id_category,
        text_categories,
    ) = get_needed_categories(session)
    text_category_by_name = {
        str(category.name): category for category in text_categories
    }

    imported_documents = list()
    for importable_document in importable_documents:
        category_id = document_category.id
        if importable_document.category_id is not None:
            category = importable_document.category_id
        new_document = importable_document.to_document_create(
            category_id, external_id_category.id  # type: ignore
        )
        new_document = crud.create_document(
            session, new_document, current_user.id, commit_and_refresh=False
        )
        imported_documents.append(new_document)

        session.flush()
        for importable_text in importable_document.texts:
            category = text_category_by_name[importable_text.category]
            new_text = importable_text.to_text_create(
                category.id, source_category.id, new_document.id  # type: ignore
            )
            new_text = crud.create_text(
                session, new_text, creator_id=current_user.id, commit_and_refresh=False
            )

            session.flush()

            for service in services:
                job = schemas.JobCreate(
                    service=service, status=schemas.JobStatus.DRAFT, item_id=new_text.id  # type: ignore
                )
                crud.create_job(session, job, current_user.id, commit_and_refresh=False)

    session.commit()

    for document in imported_documents:
        session.refresh(document)

    return imported_documents
