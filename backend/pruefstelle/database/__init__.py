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
    Topic,
    TopicKeyword,
    TopicMapping,
)

AnyResult = Union[Keyword, NamedEntity, Topic]


AnyCategory = Union[
    Category,
    CaseCategory,
    DocumentCategory,
    SourceCategory,
    ExternalIDCategory,
]

from .errors import NotUniqueError, IDError, CRUDError
