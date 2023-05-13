import polars as pl
import pytest

from ml.preprocessor.base_preprocessor import BasePreprocessor


class PreprocessorImplement(BasePreprocessor):
    def feature(self):
        raise NotImplementedError

    def run(self, data: pl.dataframe.frame.DataFrame):
        raise NotImplementedError


def test_feature():
    preprocessor = PreprocessorImplement()
    with pytest.raises(NotImplementedError):
        preprocessor.feature()


def test_run():
    preprocessor = PreprocessorImplement()
    data = pl.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    with pytest.raises(NotImplementedError):
        preprocessor.run(data)
