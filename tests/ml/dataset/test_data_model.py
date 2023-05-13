import numpy as np
import polars as pl
from scipy.sparse import csr_matrix

from ml.dataset.data_model import Dataset, FeatureTarget


def test_feature_target():
    feature = csr_matrix([[1, 2, 0], [3, 0, 4]])
    target = pl.Series([1, 2])

    feature_target = FeatureTarget(feature=feature, target=target)

    assert np.array_equal(feature_target.feature.toarray(), feature.toarray())
    assert np.array_equal(feature_target.target, target)


def test_dataset():
    feature_train = csr_matrix([[1, 2, 0], [3, 0, 4]])
    target_train = pl.Series([1, 2])
    train = FeatureTarget(feature_train, target_train)

    feature_valid = csr_matrix([[0, 5, 6], [0, 7, 8]])
    target_valid = pl.Series([3, 4])
    valid = FeatureTarget(feature_valid, target_valid)

    feature_test = csr_matrix([[9, 0, 10], [0, 11, 12]])
    target_test = pl.Series([5, 6])
    test = FeatureTarget(feature_test, target_test)

    dataset = Dataset(train=train, valid=valid, test=test)

    assert dataset.train == train
    assert dataset.valid == valid
    assert dataset.test == test
