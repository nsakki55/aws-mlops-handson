import os
import pickle
import tempfile
from unittest.mock import MagicMock, patch

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from ml.dataset.data_model import Dataset, FeatureTarget
from ml.model.sgd_classifier_ctr_optuna_model import SGDClassifierCTROptunaModel


def test_grid_search():
    X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, random_state=42)
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)
    dataset = Dataset(train=FeatureTarget(X_train, y_train), valid=FeatureTarget(X_valid, y_valid), test=None)

    model = SGDClassifierCTROptunaModel()
    best_alpha = model._optuna_search(dataset)

    assert 0 <= best_alpha <= 0.1
    assert isinstance(best_alpha, float)


@patch("ml.model.sgd_classifier_ctr_optuna_model.SGDClassifierCTROptunaModel._optuna_search")
@patch("sklearn.linear_model.SGDClassifier.score")
@patch("sklearn.linear_model.SGDClassifier.fit")
def test_train(mocked_train, mocked_score, mocked_optuna_search):
    dataset = MagicMock()
    mocked_optuna_search.return_value = 0.1

    model = SGDClassifierCTROptunaModel()
    model.train(dataset)

    mocked_optuna_search.assert_called_once_with(dataset=dataset)
    mocked_train.assert_called_once_with(dataset.train.feature, dataset.train.target)
    mocked_score.assert_called_once_with(dataset.test.feature, dataset.test.target)


@patch("ml.aws.controller.boto3")
def test_save(mocked_boto3):
    file_path = os.path.join(tempfile.mkdtemp(), "test_model.pkl")
    s3_bucket = "test_bucket"
    s3_key = "test_model.pkl"
    model = SGDClassifierCTROptunaModel()
    model.save(s3_bucket=s3_bucket, s3_key=s3_key, file_path=file_path)
    assert os.path.exists(file_path)


def test_load():
    tmp_model = SGDClassifierCTROptunaModel()
    file_path = os.path.join(tempfile.mkdtemp(), "tmp_model.pkl")
    pickle.dump(tmp_model, open(file_path, "wb"))

    model = SGDClassifierCTROptunaModel()
    model.load(file_path)
    assert model.model is not None


def test_predict():
    model_mock = MagicMock()
    model_mock.predict_proba.return_value = [[0.2, 0.8]]
    input = MagicMock()

    model = SGDClassifierCTROptunaModel()
    model.model = model_mock

    assert model.predict(input=input) == 0.8
    model_mock.predict_proba.assert_called_once_with(input)
