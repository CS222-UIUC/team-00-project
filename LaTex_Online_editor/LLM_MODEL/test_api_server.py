from fastapi.testclient import TestClient
from api_server import app

client = TestClient(app)


def test_latex_endpoint_success():
    response = client.post("/latex", json={"text": "the integral of x squared"})
    assert response.status_code == 200
    assert "latex" in response.json()
    assert isinstance(response.json()["latex"], str)
    assert len(response.json()["latex"]) > 0


def test_latex_endpoint_empty_input():
    response = client.post("/latex", json={"text": ""})
    assert response.status_code == 200
    assert "latex" in response.json()
    assert isinstance(response.json()["latex"], str)


def test_latex_endpoint_invalid_json():
    response = client.post("/latex", data="this is not json")
    assert response.status_code == 422  # FastAPI validation error


def test_latex_endpoint_long_input():
    long_text = "the integral of " + "x squared plus ".join(["x"] * 100)
    response = client.post("/latex", json={"text": long_text})
    assert response.status_code == 200
    assert "latex" in response.json()
    assert isinstance(response.json()["latex"], str)


def test_latex_endpoint_missing_text_field():
    response = client.post("/latex", json={"wrong_field": "value"})
    assert response.status_code == 422  # Required field `text` is missing
