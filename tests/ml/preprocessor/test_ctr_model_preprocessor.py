import numpy as np
import polars as pl
import pytest
from ml.preprocessor.ctr_model_preprocessor import CTRModelPreprocessor
from scipy.sparse._csr import csr_matrix


@pytest.fixture
def sample_data():
    data = {
        "hour": [21011500, 21011501, 21011502, 21011503],
        "banner_pos": [1, 2, 3, 4],
        "site_id": ["AAA", "BBB", "CCC", "DDD"],
        "site_domain": ["site_A", "site_B", "site_C", "site_D"],
        "site_category": ["A", "B", "C", "D"],
        "app_id": ["111", "222", "333", "444"],
        "app_domain": ["app_A", "app_B", "app_C", "app_D"],
        "app_category": ["A", "B", "C", "D"],
        "device_id": ["device_1", "device_2", "device_3", "device_4"],
        "device_ip": ["192.0.2.1", "192.0.2.2", "192.0.2.3", "192.0.2.4"],
        "device_model": ["model_A", "model_B", "model_C", "model_D"],
        "device_type": [1, 2, 1, 2],
    }
    df = pl.DataFrame(data)
    return df


def test_run(sample_data):
    preprocessor = CTRModelPreprocessor()
    actual = preprocessor.run(sample_data)

    assert isinstance(actual, csr_matrix)
    assert actual.shape == (4, 262144)
    unique_values = np.unique(actual.toarray())
    assert len(unique_values) > 0 and len(unique_values) <= 262144


def test_feature():
    expected = [
        "hour",
        "banner_pos",
        "site_id",
        "site_domain",
        "site_category",
        "app_id",
        "app_domain",
        "app_category",
        "device_id",
        "device_ip",
        "device_model",
        "device_type",
    ]
    preprocessor = CTRModelPreprocessor()
    assert preprocessor.feature == expected
