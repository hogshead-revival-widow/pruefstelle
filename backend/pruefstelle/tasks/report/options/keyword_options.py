"""
Apply one option per function and return a set of IDs to be
excluded from further processing (i.e. ignored in point calculation).

Cf. tasks.points.options:get_options / schemas.ProfileRead
for order of option application.
"""

from typing import List, Set
from uuid import UUID

from .... import schemas


def keyword_only_top_n_relevance(
    keywords: List[schemas.KeywordRead], value: int
) -> Set[UUID]:
    total = len(keywords)
    n = value

    if (total <= n) or (n == 0):
        return set()

    top_n_keywords_by_id = map(
        lambda x: x.id, sorted(keywords, key=lambda x: x.relevance, reverse=True)[:n]
    )

    to_drop = {
        keyword.id for keyword in keywords if keyword.id not in top_n_keywords_by_id
    }

    return to_drop


def keyword_relevance_threshold(
    keywords: List[schemas.KeywordRead], value: int
) -> Set[UUID]:
    if value == 0:
        return set()
    return set(map(lambda x: x.id, filter(lambda x: x.relevance < value, keywords)))


def keyword_confidence_threshold(
    keywords: List[schemas.KeywordRead], value: int
) -> Set[UUID]:
    if value == 0:
        return set()
    return set(map(lambda x: x.id, filter(lambda x: x.confidence < value, keywords)))


def keyword_frequency_threshold(
    keywords: List[schemas.KeywordRead], value: int
) -> Set[UUID]:
    if value == 0:
        return set()
    return set(map(lambda x: x.id, filter(lambda x: x.frequency < value, keywords)))
