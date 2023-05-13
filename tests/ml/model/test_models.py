import pytest
from ml.model import SGDClassifierCTRModel, SGDClassifierCTROptunaModel
from ml.model.models import MODELS
from ml.preprocessor import CTRModelPreprocessor

params = {
    "sgd_classifier_ctr_model": ("sgd_classifier_ctr_model", SGDClassifierCTRModel, CTRModelPreprocessor),
    "sgd_classifier_ctr_optuna_model": ("sgd_classifier_ctr_optuna_model", SGDClassifierCTROptunaModel, CTRModelPreprocessor),
}


@pytest.mark.parametrize(
    "model_name, expected_model_class, expected_preprocessor_class", list(params.values()), ids=list(params.keys())
)
def test_retrieve_valid(model_name, expected_model_class, expected_preprocessor_class):
    retrieved_model = MODELS.retrieve(model_name)
    assert retrieved_model.name == model_name


def test_all_models_are_tested():
    assert list(params.keys()) == [model.name for model in MODELS]


def test_retrieve_invalid():
    invalid_model_name = "not_implemented_model"
    with pytest.raises(ValueError):
        MODELS.retrieve(invalid_model_name)
