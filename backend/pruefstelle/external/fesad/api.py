from typing import List
from urllib import parse


from pydantic import BaseModel, PositiveInt, ValidationError

from ...config import settings
from ..base_api import Api
from .schemas import (
    ImportableText,
    ImportableDocument,
    Preview,
    TranscribedWord,
    TranscriptLimit,
    Container,
)

from ...tasks.fesad.schemas import DocumentInformation

from .transcript import cut, ms_to_sec, get_transcript_id


class DocumentImporter(Api):
    class Paths(BaseModel):
        """Paths to endpoints"""

        base_url: str = settings.TEXT_IMPORTER.BASE_URL  # type: ignore
        mpeg7_url: str = settings.TEXT_IMPORTER.MPEG7_URL  # type: ignore
        du = "/du/{du_key}"
        preview = "/du/{du_key}/preview"
        containers = "/du/{du_key}/containers"
        transcript = "/mpeg7/words?url={url}"

    def __init__(self):
        self.paths = DocumentImporter.Paths()
        super().__init__(base_url=self.paths.base_url)

    @Api.ErrorHandling.on_response_error
    def _getPreview(self, identifier: PositiveInt):
        path = self.paths.preview.format(du_key=identifier)
        url = self._path_to_url(path=path)
        response = self._get(url)
        data = response.json()
        return Preview(**data)

    @Api.ErrorHandling.on_response_error
    def _getContainer(self, identifier: PositiveInt, parent_identifier: PositiveInt):
        path = self.paths.containers.format(du_key=parent_identifier)
        url = self._path_to_url(path=path)
        response = self._get(url)
        data = response.json()
        duContainer = next(
            (
                Container(**container)
                for container in data
                if container["key"]["childKey"] == identifier
                and container["key"]["parentKey"] == parent_identifier
            ),
            None,
        )
        if duContainer is None:
            return None
        return duContainer

    @Api.ErrorHandling.on_response_error
    def _get_raw_trancsript(self, previewURL: str):
        previewURL = parse.quote(previewURL)
        path = self.paths.transcript.format(url=previewURL)
        url = self._path_to_url(path=path, base_url=self.paths.mpeg7_url)
        response = self._get(url)
        data = response.json()
        return [TranscribedWord(**word) for word in data]

    @Api.ErrorHandling.on_response_error
    def get_transcript(self, data, parentData=None):
        identifier = get_transcript_id(data)
        if identifier is None:
            return None
        parent_identifier = get_transcript_id(parentData)
        if parent_identifier is None:
            parent_identifier = identifier
        print(f"using id: {identifier}, parent: {parent_identifier}")

        preview = self._getPreview(parent_identifier)
        hasTranscript = (
            len(preview.miningResultLinks) > 0
            and "AUDIOTRANS" in preview.miningResultLinks[0].miningMethod
            and len(preview.miningResultLinks[0].url) > 0
        )
        if not hasTranscript:
            return None

        tcOffset = preview.absDuStartTc - preview.absVideoStartTC
        start = ms_to_sec(tcOffset)
        end = None
        previewURL = preview.miningResultLinks[0].url

        if identifier == parent_identifier:
            limit = TranscriptLimit(start=start, end=None)
        else:
            container = self._getContainer(identifier, parent_identifier)
            if container is None:
                limit = TranscriptLimit(start=start, end=end)
            else:
                start = ms_to_sec(container.startTimecode.timecode + tcOffset)
                end = start + ms_to_sec(container.durationNum)
                limit = TranscriptLimit(start=start, end=end)

        transcript = cut(self._get_raw_trancsript(previewURL), limit)
        content = " ".join((word.name for word in transcript))
        return ImportableText.from_vms({"content": content, "type": "-1"})

    @Api.ErrorHandling.on_response_error
    def get_texts(self, identifier: PositiveInt) -> List[ImportableText]:
        """Get texts, currently only importing from FESAD"""
        path = self.paths.du.format(du_key=identifier)
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
    def _get_du_info(self, identifier: PositiveInt):
        path = self.paths.du.format(du_key=identifier)
        url = self._path_to_url(path=path)
        response = self._get(url)
        data = response.json()["du"]
        return data

    @Api.ErrorHandling.on_response_error
    def get_document(
        self,
        info: DocumentInformation,
        # name: Optional[str] = None,
        # category_id: Optional[UUID] = None,
        # parent_du_key: Optional[PositiveInt] = None,
    ) -> ImportableDocument:
        """Get texts, currently only importing from FESAD"""
        data = self._get_du_info(info.du_key)
        texts = []
        name = info.name
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

            # get transcript
            parent_data = None
            if info.parent_du_key is not None:
                parent_data = self._get_du_info(info.parent_du_key)
            transcript = self.get_transcript(data, parent_data)
            if transcript is not None:
                texts.append(transcript)

        except KeyError as e:
            # As the direct FESAD import is a temporary workaround
            # We re-raise a KeyError as a ValidationError
            # as this is handled by `on_response_error``
            raise ValidationError([[e]], ImportableText)

        return ImportableDocument(
            name=name, du_key=info.du_key, texts=texts, category_id=info.category_id  # type: ignore
        )
