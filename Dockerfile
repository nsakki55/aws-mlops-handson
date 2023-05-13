FROM python:3.9.0-slim as ml

ENV PROJECT_DIR app
ENV AWS_DEFAULT_REGION ap-northeast-1
WORKDIR /${PROJECT_DIR}

RUN pip install --upgrade pip && pip install poetry=="1.4.2"
COPY pyproject.toml poetry.lock /
RUN poetry export -f requirements.txt > requirements.txt && pip install -r requirements.txt
COPY ./ml /${PROJECT_DIR}/ml

CMD ["python", "-m", "ml.main"]

FROM ml as predictor

COPY ./predictor /${PROJECT_DIR}/predictor

CMD ["uvicorn", "predictor.app:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
