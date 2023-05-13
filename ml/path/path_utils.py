from pathlib import Path

FILE_DIR = "files"


class PathRetrieve:
    def __init__(self, version: str, model_name: str):
        self.model_name = model_name
        self.s3_key_prefix = Path(f"{model_name}/{version}")
        self.output_dir = Path(f"{FILE_DIR}/{model_name}/{version}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def raw_data_path(self) -> str:
        return str(self.output_dir / "raw_data")

    @property
    def model_path(self) -> str:
        return str(self.output_dir / "model")

    @property
    def model_s3_key(self) -> str:
        return str(self.s3_key_prefix / "model")

    @property
    def dataset_path(self) -> str:
        return str(self.output_dir / "dataset")

    @property
    def dataset_s3_key(self) -> str:
        return str(self.s3_key_prefix / "dataset")
