from typing import List, Literal

from .schemas import TranscribedWord, TranscriptLimit


def find_limit(
    direction: Literal["start", "end"],
    transcript: List[TranscribedWord],
    value: float,
    safetySecs=1,
):

    search = (item for item in transcript if item.time - safetySecs >= value)

    def key(x):
        return abs(x.time + x.duration - value)

    if direction == "end":
        search = (
            item
            for item in transcript
            if item.time + item.duration + safetySecs <= value
        )
    try:
        foundWord = min(search, key=key)
    except ValueError:  # generator may be empty
        search = (item for item in transcript)
        foundWord = min(search, key=key)

    limit = transcript.index(foundWord)

    if direction == "end":
        limit += 1

    return limit


def get_transcript_id(data):
    if data is None or "contents" not in data or len(data["contents"]) == 0:
        return None
    key_type = 5
    identifier = next(
        (
            int(content["content"].strip())
            for content in data["contents"]
            if "type" in content
            and "content" in content
            and content["type"] == key_type
            and len(content["content"].strip()) > 0
        ),
        None,
    )
    return identifier


def ms_to_sec(ms: int):
    return ms / 1000.0


def cut(transcript: List[TranscribedWord], transcriptMetadata: TranscriptLimit):
    needsFullTranscript = (
        transcriptMetadata.end is None and transcriptMetadata.start == float(0)
    )
    if needsFullTranscript:
        return transcript

    start = find_limit("start", transcript, transcriptMetadata.start)
    if transcriptMetadata.end is None:
        return transcript[start:]

    end = find_limit("end", transcript, transcriptMetadata.end)
    return transcript[start:end]
