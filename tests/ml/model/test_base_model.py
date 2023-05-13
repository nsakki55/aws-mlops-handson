from unittest.mock import MagicMock

import pytest
from scipy.sparse._csr import csr_matrix

from ml.dataset.data_model import Dataset
from ml.model.base_model import BaseModel


class ModelImplement(BaseModel):
    def train(self, dataset: Dataset) -> None:
        raise NotImplementedError

    def save(self, s3_bucket: str, s3_key: str, file_path: str) -> str:
        raise NotImplementedError

    def load(self, file_path: str) -> None:
        raise NotImplementedError

    def predict(self, input: csr_matrix) -> float:
        raise NotImplementedError


def test_train():
    model = ModelImplement()
    dataset = MagicMock()
    with pytest.raises(NotImplementedError):
        model.train(dataset)


def test_save():
    model = ModelImplement()
    s3_bucket = "test_bucket"
    s3_key = "test_model"
    file_path = "test_file_path"
    with pytest.raises(NotImplementedError):
        model.save(s3_bucket, s3_key, file_path)


def test_load():
    model = ModelImplement()
    file_path = "test_file_path"
    with pytest.raises(NotImplementedError):
        model.load(file_path)


def test_predict():
    model = ModelImplement()
    input_data = csr_matrix([1, 2, 3])
    with pytest.raises(NotImplementedError):
        model.predict(input_data)
