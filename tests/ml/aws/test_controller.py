from unittest.mock import MagicMock, patch

from ml.aws.controller import download_from_s3, upload_to_s3


@patch("ml.aws.controller.boto3")
def test_upload_to_s3(mocked_boto3):
    s3_bucket = "test_bucket"
    s3_key = "test_key"
    file_path = "test_file_pat"

    mocked_bucket = MagicMock()
    mocked_resource = MagicMock()
    mocked_resource.Bucket.return_value = mocked_bucket
    mocked_boto3.resource.return_value = mocked_resource

    upload_to_s3(s3_bucket, s3_key, file_path)
    mocked_bucket.upload_file.assert_called_once_with(Key=s3_key, Filename=file_path)


@patch("ml.aws.controller.boto3")
def test_download_from_s3(mocked_boto3):
    s3_bucket = "test_bucket"
    s3_key = "test_key"
    file_path = "test_file_pat"

    mocked_bucket = MagicMock()
    mocked_resource = MagicMock()
    mocked_resource.Bucket.return_value = mocked_bucket
    mocked_boto3.resource.return_value = mocked_resource

    download_from_s3(s3_bucket, s3_key, file_path)
    mocked_bucket.download_file.assert_called_once_with(Key=s3_key, Filename=file_path)
