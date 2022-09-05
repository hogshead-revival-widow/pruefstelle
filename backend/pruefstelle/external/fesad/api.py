from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, PositiveInt, ValidationError

from ...config import settings
from ..base_api import Api
from .schemas import ImportableText, ImportableDocument


class Paths(BaseModel):
    """Paths to endpoints"""

    base_url: str
    from_du_key: str  # with format variable {du_key}


class DocumentImporter(Api):
    def __init__(
        self,
        paths: Paths = settings.TEXT_IMPORTER.PATHS,
        base_url: str = settings.TEXT_IMPORTER.BASE_URL,
        url_scheme: Literal["http", "https"] = settings.TEXT_IMPORTER.URL_SCHEME,
    ):
        self.paths = paths
        super().__init__(base_url=base_url, url_scheme=url_scheme)

    @Api.ErrorHandling.on_response_error
    def get_texts(self, identifier: PositiveInt) -> List[ImportableText]:
        """Get texts, currently only importing from FESAD"""
        path = self.paths.from_du_key.format(du_key=identifier)
        url = self._path_to_url(path=path)
        response = self._get(url)
        data = response.json()
        texts = []
        try:
            if "contents" in data:
                texts = [ImportableText.from_fesad(text) for text in data["contents"]]
                texts = [text for text in texts if text is not None]
        except KeyError as e:
            # As the direct FESAD import is a temporary workaround
            # We re-raise a KeyError as a ValidationError
            # as this is handled by `on_response_error``
            raise ValidationError([[e]], ImportableText)

        return texts

    @Api.ErrorHandling.on_response_error
    def get_document(
        self,
        du_key: PositiveInt,
        name: Optional[str] = None,
        category_id: Optional[UUID] = None,
    ) -> Optional[ImportableDocument]:
        """Get texts, currently only importing from FESAD"""
        path = self.paths.from_du_key.format(du_key=du_key)
        url = self._path_to_url(path=path)
        response = self._get(url)
        data = response.json()
        texts = []

        try:
            if "du" not in data:
                return None
            data = data["du"]

            if name is None:
                name = settings.STRINGS.TEXT_IMPORT_DEFAULT_TITLE

                titles = list()
                # we are only interested in the first two title parts
                if "titles" in data:
                    for title in data["titles"][:2]:

                        title = str(title["title"]).strip()
                        if len(title) > 0:
                            titles.append(title)

                if ("titles" not in data) or (len(titles) == 0) and ("label" in data):
                    # no title? get title from label if set
                    label = str(data["label"]).strip()
                    if len(label) > 0:
                        titles.append(str(label))

                if len(titles) > 0:
                    name = ": ".join(titles)

            # get texts
            if "contents" in data:
                texts = [ImportableText.from_fesad(text) for text in data["contents"]]
                # removing results from ImportableText.from_fesad if none
                texts = [text for text in texts if text is not None]
        except KeyError as e:
            # As the direct FESAD import is a temporary workaround
            # We re-raise a KeyError as a ValidationError
            # as this is handled by `on_response_error``
            raise ValidationError([[e]], ImportableText)

        return ImportableDocument(
            name=name, du_key=du_key, texts=texts, category_id=category_id  # type: ignore
        )
