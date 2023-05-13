from dataclasses import dataclass

from ml.aws.controller import download_from_s3
from ml.logger.logging_utils import get_logger
from ml.model.base_model import BaseModel
from ml.model.models import MODELS
from ml.path.path_utils import PathRetrieve
from ml.preprocessor.base_preprocessor import BasePreprocessor

logger = get_logger(__name__)


@dataclass
class ModelPreprocessor:
    model_name: str
    model: BaseModel
    preprocessor: BasePreprocessor


def get_model_preprocessor(bucket: str, model_name: str, version: str) -> ModelPreprocessor:
    logger.info(f"api setup: bucket {bucket}, model_name: {model_name}, version: {version}")
    path_retrieve = PathRetrieve(version=version, model_name=model_name)
    download_from_s3(
        s3_bucket=bucket,
        s3_key=path_retrieve.model_s3_key,
        file_path=path_retrieve.model_path,
    )

    model_info = MODELS.retrieve(model_name)
    model = model_info.model()
    model.load(path_retrieve.model_path)
    preprocessor = model_info.preprocessor()

    return ModelPreprocessor(model_name=model_name, model=model, preprocessor=preprocessor)
