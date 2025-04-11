import io
from io import BytesIO
from PIL import Image
from backend.server import app
from unittest.mock import patch


def test_compile_latex():
    client = app.test_client()
    tex_code = r"\documentclass{article}\begin{document}Test\end{document}"
    response = client.post("/compile", data={"code": tex_code})
    assert response.status_code == 200
    assert response.mimetype == "application/pdf"


def test_ocr_endpoint_with_no_file():
    client = app.test_client()
    response = client.post("/ocr", data={})
    assert response.status_code == 400
    assert b"No image uploaded" in response.data


def test_compile_fails(client):
    res = client.post("/compile", data={"code": "bad \\latex"})
    assert res.status_code == 500


def test_ocr_no_file(client):
    response = client.post("/ocr", data={})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_compile_invalid_latex(client):
    bad_code = r"\badcommand"
    response = client.post("/compile", data={"code": bad_code})
    assert response.status_code == 500
    assert b"Failed to compile LaTeX" in response.data


def test_ocr_image_success(client):
    img = Image.new("RGB", (100, 30), color=(255, 255, 255))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    response = client.post(
        "/ocr",
        data={"image": (img_bytes, "test.png")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert "latex" in response.json


def test_ocr_image_missing_file(client):
    response = client.post("/ocr", data={}, content_type="multipart/form-data")
    assert response.status_code == 400
    assert response.json["error"] == "No image uploaded"


@patch("backend.server.predict_latex", side_effect=Exception("mock error"))
def test_ocr_image_internal_error(mock_predict, client):
    data = {"image": (BytesIO(b"dummy image"), "test.png")}
    response = client.post("/ocr", data=data, content_type="multipart/form-data")
    assert response.status_code == 500
    assert "error" in response.json


def test_ocr_image_error(client):
    with patch("backend.server.predict_latex", side_effect=RuntimeError("Mock fail")):
        data = {"image": (BytesIO(b"fake image content"), "fake.png")}
        response = client.post("/ocr", data=data, content_type="multipart/form-data")
        assert response.status_code == 500
        assert "error" in response.json
