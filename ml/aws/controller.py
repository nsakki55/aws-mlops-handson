import boto3
from ml.logger.logging_utils import get_logger

logger = get_logger(__name__)


def upload_to_s3(s3_bucket: str, s3_key: str, file_path: str) -> None:
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3_bucket)

    logger.info(f"Start uploading model file: {s3_key}, file_path: {file_path}")
    bucket.upload_file(Key=s3_key, Filename=file_path)
    logger.info(f"Completely uploaded model file: {s3_key}, file_path: {file_path}")


def download_from_s3(s3_bucket: str, s3_key: str, file_path: str) -> None:
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3_bucket)

    logger.info(f"Start downloading model file: {s3_key}, file_path: {file_path}")
    bucket.download_file(Key=s3_key, Filename=file_path)
    logger.info(f"Completely downloaded model file: {s3_key}, file_path: {file_path}")
