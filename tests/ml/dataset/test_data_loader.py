import os
import pickle
import tempfile
from unittest.mock import MagicMock, patch

import polars as pl

from ml.dataset.data_loader import DataLoader
from ml.dataset.data_model import Dataset, FeatureTarget
from ml.logger.logging_utils import get_logger

logger = get_logger(__name__)
TARGET = "click"
S3_BUCKET = "test-bucket"
S3_KEY = "test-key"


@patch("ml.aws.controller.boto3")
def test_load(mocked_boto3):
    data = pl.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": ["A", "B", "C"],
            "col3": [0.1, 0.2, 0.3],
        }
    )
    file_path = os.path.join(tempfile.mkdtemp(), "tmp_data.csv")
    data.write_csv(file_path)

    dataloader = DataLoader(s3_bucket=S3_BUCKET)
    loaded_data = dataloader.load(s3_key=S3_KEY, file_path=file_path)

    assert isinstance(loaded_data, pl.DataFrame)
    assert loaded_data.shape == data.shape


def test_train_test_split():
    data = pl.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "col2": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
            "col3": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            TARGET: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        }
    )

    preprocessor = MagicMock()
    preprocessor.run.side_effect = lambda x: x
    preprocessor.feature = ["col1", "col2", "col3"]

    dataloader = DataLoader(s3_bucket=S3_BUCKET)
    dataset = dataloader.train_test_split(raw_data=data, preprocessor=preprocessor)

    assert isinstance(dataset, Dataset)
    assert isinstance(dataset.train, FeatureTarget)
    assert isinstance(dataset.valid, FeatureTarget)
    assert isinstance(dataset.test, FeatureTarget)

    assert dataset.train.feature.shape[0] + dataset.valid.feature.shape[0] + dataset.test.feature.shape[0] == data.shape[0]


@patch("ml.aws.controller.boto3")
def test_save(mocked_boto3):
    data = pl.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "col2": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
            "col3": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            TARGET: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        }
    )

    preprocessor = MagicMock()
    preprocessor.run.side_effect = lambda x: x
    preprocessor.feature = ["col1", "col2", "col3"]

    dataloader = DataLoader(s3_bucket=S3_BUCKET)
    dataset = dataloader.train_test_split(raw_data=data, preprocessor=preprocessor)

    file_path = os.path.join(tempfile.mkdtemp(), "test_dataset.pkl")
    dataloader.save(dataset=dataset, s3_key=S3_KEY, file_path=file_path)

    assert os.path.exists(file_path)

    loaded_data = pickle.load(open(file_path, "rb"))
    assert isinstance(loaded_data, Dataset)
    assert isinstance(loaded_data.train, FeatureTarget)
    assert isinstance(loaded_data.valid, FeatureTarget)
    assert isinstance(loaded_data.test, FeatureTarget)

    assert loaded_data.train.feature.shape == dataset.train.feature.shape
    assert loaded_data.valid.feature.shape == dataset.valid.feature.shape
    assert loaded_data.test.feature.shape == dataset.test.feature.shape
