from unittest.mock import MagicMock, patch

from ml.model.base_model import BaseModel
from ml.preprocessor.base_preprocessor import BasePreprocessor
from predictor.setup import ModelPreprocessor, get_model_preprocessor


@patch("predictor.setup.MODELS.retrieve")
@patch("predictor.setup.download_from_s3")
@patch("predictor.setup.PathRetrieve")
def test_setup(mocked_path_retrieve, mocked_download_from_s3, mocked_retrieve):
    bucket = "test-bucket"
    model_name = "test-model"
    version = "v1"

    mocked_model = MagicMock(spec=BaseModel)
    mock_preprocessor = MagicMock(spec=BasePreprocessor)

    mocked_model_info = MagicMock()
    mocked_path_retrieve.return_value = MagicMock()
    mocked_download_from_s3.return_value = None
    mocked_retrieve.return_value = mocked_model_info
    mocked_model_info.model.return_value = mocked_model
    mocked_model_info.preprocessor.return_value = mock_preprocessor

    result = get_model_preprocessor(bucket=bucket, model_name=model_name, version=version)

    mocked_path_retrieve.assert_called_once_with(version=version, model_name=model_name)
    mocked_download_from_s3.assert_called_once_with(
        s3_bucket=bucket,
        s3_key=mocked_path_retrieve.return_value.model_s3_key,
        file_path=mocked_path_retrieve.return_value.model_path,
    )
    mocked_retrieve.assert_called_once_with(model_name)
    expected_result = ModelPreprocessor(
        model_name=model_name,
        model=mocked_model,
        preprocessor=mock_preprocessor,
    )
    assert result == expected_result
