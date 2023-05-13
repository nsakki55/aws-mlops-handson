import os
import pickle
import tempfile
from unittest.mock import MagicMock, patch

import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split

from ml.dataset.data_model import Dataset, FeatureTarget
from ml.model.sgd_classifier_ctr_model import SGDClassifierCTRModel


def test_grid_search():
    X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, random_state=42)
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)
    dataset = Dataset(train=FeatureTarget(X_train, y_train), valid=FeatureTarget(X_valid, y_valid), test=None)

    model = SGDClassifierCTRModel()
    best_alpha = model._grid_search(dataset)

    assert np.isin(best_alpha, [1e-5, 1e-4, 1e-3, 1e2, 1e-1])

    best_model = SGDClassifier(loss="log_loss", penalty="l2", random_state=42, alpha=best_alpha)
    best_model.fit(X_train, y_train)
    best_score = best_model.score(X_valid, y_valid)

    for alpha in [1e-5, 1e-4, 1e-3, 1e2, 1e-1]:
        if alpha != best_alpha:
            model = SGDClassifier(loss="log_loss", penalty="l2", random_state=42, alpha=alpha)
            model.fit(X_train, y_train)
            score = model.score(X_valid, y_valid)
            assert best_score <= score


@patch("ml.model.sgd_classifier_ctr_model.SGDClassifierCTRModel._grid_search")
@patch("sklearn.linear_model.SGDClassifier.score")
@patch("sklearn.linear_model.SGDClassifier.fit")
def test_train(mocked_train, mocked_score, mocked_grid_search):
    dataset = MagicMock()
    mocked_grid_search.return_value = 0.1

    model = SGDClassifierCTRModel()
    model.train(dataset)

    mocked_grid_search.assert_called_once_with(dataset=dataset)
    mocked_train.assert_called_once_with(dataset.train.feature, dataset.train.target)
    mocked_score.assert_called_once_with(dataset.test.feature, dataset.test.target)


@patch("ml.aws.controller.boto3")
def test_save(mocked_boto3):
    file_path = os.path.join(tempfile.mkdtemp(), "test_model.pkl")
    s3_bucket = "test_bucket"
    s3_key = "test_model.pkl"
    model = SGDClassifierCTRModel()
    model.save(s3_bucket=s3_bucket, s3_key=s3_key, file_path=file_path)
    assert os.path.exists(file_path)


def test_load():
    tmp_model = SGDClassifierCTRModel()
    file_path = os.path.join(tempfile.mkdtemp(), "tmp_model.pkl")
    pickle.dump(tmp_model, open(file_path, "wb"))

    model = SGDClassifierCTRModel()
    model.load(file_path)
    assert model.model is not None


def test_predict():
    model_mock = MagicMock()
    model_mock.predict_proba.return_value = [[0.2, 0.8]]
    input = MagicMock()

    model = SGDClassifierCTRModel()
    model.model = model_mock

    assert model.predict(input=input) == 0.8
    model_mock.predict_proba.assert_called_once_with(input)
