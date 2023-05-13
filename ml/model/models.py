from dataclasses import dataclass
from enum import Enum
from typing import Type

from ml.model import BaseModel, SGDClassifierCTRModel, SGDClassifierCTROptunaModel
from ml.preprocessor import BasePreprocessor, CTRModelPreprocessor


@dataclass(frozen=True)
class Model(object):
    name: str
    model: Type[BaseModel]
    preprocessor: Type[BasePreprocessor]


class MODELS(Enum):
    sgd_classifier_ctr_model = Model(
        name="sgd_classifier_ctr_model",
        model=SGDClassifierCTRModel,
        preprocessor=CTRModelPreprocessor,
    )
    sgd_classifier_ctr_optuna_model = Model(
        name="sgd_classifier_ctr_optuna_model",
        model=SGDClassifierCTROptunaModel,
        preprocessor=CTRModelPreprocessor,
    )

    @staticmethod
    def retrieve(name: str) -> Model:
        for model in [v.value for v in MODELS.__members__.values()]:
            if model.name == name:
                return model
        raise ValueError(f"{name} is not implemented.")
