from abc import ABC, abstractmethod
from typing import List

import polars as pl
from scipy.sparse._csr import csr_matrix


class BasePreprocessor(ABC):
    @property
    @abstractmethod
    def feature(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def run(self, data: pl.dataframe.frame.DataFrame) -> csr_matrix:
        raise NotImplementedError
