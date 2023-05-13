import shutil

import pytest

from ml.path.path_utils import FILE_DIR, PathRetrieve


@pytest.fixture
def path_retrieve():
    test_version = "test_version"
    model_name = "test_model"
    yield PathRetrieve(test_version, model_name)
    shutil.rmtree(f"{FILE_DIR}/{model_name}/{test_version}")


def test_raw_data_path(path_retrieve):
    expected_path = f"{FILE_DIR}/test_model/test_version/raw_data"
    assert path_retrieve.raw_data_path == expected_path


def test_model_path(path_retrieve):
    expected_path = f"{FILE_DIR}/test_model/test_version/model"
    assert path_retrieve.model_path == expected_path


def test_model_s3_key(path_retrieve):
    expected_key = "test_model/test_version/model"
    assert path_retrieve.model_s3_key == expected_key


def test_dataset_path(path_retrieve):
    expected_path = f"{FILE_DIR}/test_model/test_version/dataset"
    assert path_retrieve.dataset_path == expected_path


def test_dataset_s3_key(path_retrieve):
    expected_key = "test_model/test_version/dataset"
    assert path_retrieve.dataset_s3_key == expected_key
