from typing import List, Dict, Set, Callable, Tuple
from uuid import UUID

from pydantic import BaseModel

from .... import schemas
from ....database import ResultType
from . import keyword_options


KeywordOptionFunction = Callable[[List[schemas.KeywordRead], int], Set[UUID]]


class Options(BaseModel):
    # e.g. List[(keyword_options.keyword_only_top_n_relevance, 10),...]
    keyword_options: List[Tuple[KeywordOptionFunction, int]]


def get_options(profile: schemas.ProfileRead) -> Options:

    profile_dict = profile.dict()
    keyword_prefix = "keyword_"
    kw_options = [
        (getattr(keyword_options, name), value)
        for name, value in profile_dict.items()
        if name.startswith(keyword_prefix)
    ]

    return Options(keyword_options=kw_options)


def apply_options(
    profile: schemas.ProfileRead,
    results_by_item_id: Dict[UUID, List[schemas.ResultRead]],
) -> Dict[UUID, List[schemas.ResultRead]]:

    # make sure not to mutate the original results
    optioned_results = dict(results_by_item_id)

    options = get_options(profile)
    results_to_drop = set()

    for item_id, item_results in optioned_results.items():

        results_to_drop_per_item = apply_options_per_item(options, item_results)
        results_to_drop = results_to_drop.union(results_to_drop_per_item)

    for item_id, results in optioned_results.items():
        to_keep = [result for result in results if result.id not in results_to_drop]
        optioned_results[item_id] = to_keep

    return optioned_results


def apply_options_per_item(
    options: Options, results: List[schemas.ResultRead]
) -> Set[UUID]:

    to_drop = set()
    if len(results) == 0:
        return to_drop
    to_drop = apply_keyword_options_per_item(options, results)
    return to_drop


def apply_keyword_options_per_item(
    options: Options, results: List[schemas.ResultRead]
) -> Set[UUID]:

    all_keywords = [
        result for result in results if result.discriminator == ResultType.Keyword
    ]

    to_drop = set()
    for option, value in options.keyword_options:
        option_wants_to_drop = option(all_keywords, value)
        to_drop = to_drop.union(option_wants_to_drop)

    return to_drop
