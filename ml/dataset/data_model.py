from dataclasses import dataclass

import polars as pl
from scipy.sparse._csr import csr_matrix


@dataclass
class FeatureTarget:
    feature: csr_matrix
    target: pl.series.series.Series


@dataclass
class Dataset:
    train: FeatureTarget
    valid: FeatureTarget
    test: FeatureTarget
