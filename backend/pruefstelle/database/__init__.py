from typing import Union

from .tables import (
    User,
    Case,
    Profile,
    Document,
    CaseDocumentLink,
    Category,
    CaseCategory,
    DocumentCategory,
    SourceCategory,
    ExternalIDCategory,
    CategoryType,
    Text,
    MiningJob,
    MiningResult,
    Keyword,
    NamedEntity,
    Evaluation,
    ScoredEvaluation,
    CorrectnessEvaluation,
    ResearchQualitySnapshot,
    ResultType,
    Item,
    TextCategory,
    ItemType,
    MagicLink,
)

AnyResult = Union[Keyword, NamedEntity]


AnyCategory = Union[
    Category,
    CaseCategory,
    DocumentCategory,
    SourceCategory,
    ExternalIDCategory,
]

from .errors import NotUniqueError, IDError, CRUDError
