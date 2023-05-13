import argparse
import os

from ml.dataset.data_loader import DataLoader
from ml.logger.logging_utils import get_logger
from ml.model.models import MODELS
from ml.path.path_utils import PathRetrieve

logger = get_logger(__name__)
raw_data_s3_key = "train_data"


def load_options() -> argparse.Namespace:
    description = """
    Train ML Pipeline runtime arguments
    """
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-b", "--bucket", type=str, default=os.getenv("AWS_BUCKET", "mlops-handson"))
    parser.add_argument("-v", "--version", type=str, default=os.getenv("VERSION", "2023-05-11"))
    parser.add_argument("-m", "--model_name", type=str, default=os.getenv("MODEL", "sgd_classifier_ctr_model"))

    return parser.parse_args()


def main() -> None:
    args = load_options()
    logger.info(f"Started ML Pipeline. model_name: {args.model_name}")
    path_retrieve = PathRetrieve(version=args.version, model_name=args.model_name)
    model_info = MODELS.retrieve(args.model_name)

    model = model_info.model()
    preprocessor = model_info.preprocessor()
    data_loader = DataLoader(args.bucket)

    raw_data = data_loader.load(s3_key=raw_data_s3_key, file_path=path_retrieve.raw_data_path)
    dataset = data_loader.train_test_split(raw_data=raw_data, preprocessor=preprocessor)
    data_loader.save(dataset=dataset, s3_key=path_retrieve.dataset_s3_key, file_path=path_retrieve.dataset_path)

    model.train(dataset=dataset)
    model.save(s3_bucket=args.bucket, s3_key=path_retrieve.model_s3_key, file_path=path_retrieve.model_path)
    logger.info(f"Finished ML Pipeline. model_name: {args.model_name}")


if __name__ == "__main__":
    main()
