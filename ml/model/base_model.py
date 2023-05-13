from abc import ABC, abstractmethod

from ml.dataset.data_model import Dataset
from scipy.sparse._csr import csr_matrix


class BaseModel(ABC):
    @abstractmethod
    def train(self, dataset: Dataset) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self, s3_bucket: str, s3_key: str, file_path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def load(self, file_path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def predict(self, input: csr_matrix) -> float:
        raise NotImplementedError
