import json
import os
import random
from typing import Dict, Union

import polars as pl
from fastapi import APIRouter
from ml.logger.logging_utils import get_logger
from predictor.request import AdRequest
from predictor.setup import get_model_preprocessor

logger = get_logger(__name__)

BUCKET = str(os.getenv("AWS_BUCKET"))
VERSION = str(os.getenv("VERSION"))

model_candidates = ["sgd_classifier_ctr_model", "sgd_classifier_ctr_optuna_model"]
model_preprocessor_list = [
    get_model_preprocessor(bucket=BUCKET, model_name=model_name, version=VERSION) for model_name in model_candidates
]


router = APIRouter()


@router.post("/predict")
def predict(ad_request: AdRequest) -> Dict[str, Union[float, str]]:
    logger.info(f"predict method call: {ad_request}")
    model_preprocessor = random.choice(model_preprocessor_list)

    df = pl.DataFrame(json.loads(ad_request.json()))
    preprocessed = model_preprocessor.preprocessor.run(df)
    pred = model_preprocessor.model.predict(preprocessed)
    logger.info(f"model: {model_preprocessor.model_name}, predict value: {pred}")
    return {"prediction": pred, "model": model_preprocessor.model_name}


@router.get("/healthcheck")
def healthcheck() -> Dict[str, str]:
    logger.info("helathcheck method call")
    return {"health": "ok"}
