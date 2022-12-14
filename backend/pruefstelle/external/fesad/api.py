from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, PositiveInt, ValidationError

from ...config import settings
from ..base_api import Api
from .schemas import ImportableText, ImportableDocument


class DocumentImporter(Api):
    class Paths(BaseModel):
        """Paths to endpoints"""

        base_url: str = settings.TEXT_IMPORTER.BASE_URL  # type: ignore
        from_du_key = "/du/{du_key}/"

    def __init__(self):
        self.paths = DocumentImporter.Paths()
        super().__init__(base_url=self.paths.base_url)

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
    ) -> ImportableDocument:
        """Get texts, currently only importing from FESAD"""
        path = self.paths.from_du_key.format(du_key=du_key)
        url = self._path_to_url(path=path)
        response = self._get(url)
        data = response.json()["du"]
        texts = []
        try:
            if name is None:
                name = "unbekannt"

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
