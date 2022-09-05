from uuid import UUID
from typing import Union, Literal
from typing_extensions import Annotated


from pydantic import BaseModel, validator, Field

from ..database import Evaluation
from .mixins import WithID, Score, WithCreator, WithDate


class ScoredEvaluationCreate(BaseModel):
    discriminator: Literal[Evaluation.discriminatorType.ScoredEvaluation]
    value: Score


class CorrectnessEvaluationCreate(BaseModel):
    discriminator: Literal[Evaluation.discriminatorType.CorrectnessEvaluation]
    value: bool


EvaluationCreate = Annotated[
    Union[ScoredEvaluationCreate, CorrectnessEvaluationCreate],
    Field(discriminator="discriminator"),
]

EvaluationUpdate = EvaluationCreate


class EvaluationRead(WithID, WithCreator, WithDate):
    mining_result_id: UUID
    value: int
    discriminator: Evaluation.discriminatorType
    is_good: bool = False

    @validator("is_good", pre=True, always=True)
    def set_is_good(cls, v, *, values, **kwargs):
        attr_discriminator = values["discriminator"]
        attr_value: int = values["value"]
        if attr_discriminator == Evaluation.discriminatorType.ScoredEvaluation:
            return attr_value > Score.BAD
        if attr_discriminator == Evaluation.discriminatorType.CorrectnessEvaluation:
            return attr_value > 0
        raise NotImplementedError

    class Config:
        orm_mode = True
