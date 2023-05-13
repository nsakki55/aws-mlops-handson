from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
@patch("predictor.setup.get_model_preprocessor")
def test_client(mocked_get_model_preprocessor):
    from predictor.routers import router

    return TestClient(router)


def test_healthcheck(test_client):
    response = test_client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"health": "ok"}


def test_predict(test_client):
    data = (
        '{"hour": "05","banner_pos": "1","site_id": "site123","site_domain": "example.com",'
        '"site_category": "news","app_id": "app123","app_domain": "example.com",'
        '"app_category": "education","device_id": "device123","device_ip": "192.168.0.1",'
        '"device_model": "Samsung Galaxy S21","device_type": "1"}'
    )

    response = test_client.post("/predict", data=data)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "model" in response.json()
