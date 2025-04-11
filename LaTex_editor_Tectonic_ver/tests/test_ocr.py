import os
import pytest
from backend.ocr import predict_latex
from backend.ocr import wrap_latex
from backend.ocr import extract_latex
from unittest.mock import patch


def test_predict_latex_dummy():
    dummy_path = "tests/assets/formula_sample.png"
    assert os.path.exists(dummy_path)
    latex = predict_latex(dummy_path)
    assert isinstance(latex, str)
    assert len(latex) > 0


def test_wrap_latex_basic():
    body = r"\alpha + \beta = \gamma"
    wrapped = wrap_latex(body)
    assert r"\begin{document}" in wrapped
    assert body in wrapped
    assert r"\end{document}" in wrapped


def test_predict_latex_invalid_path():
    with pytest.raises(ValueError, match="Failed to load image:"):
        predict_latex("nonexistent_file.png")


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("text=\\alpha + \\beta = \\gamma confidence=0.99", r"\alpha + \beta = \gamma"),
        (
            "text=\\int x^n \\, dx = \\frac{x^{n+1}}{n+1} + C confidence=0.85",
            r"\int x^n \, dx = \frac{x^{n+1}}{n+1} + C",
        ),
        ("<math display='block'>\\sum_{i=1}^n i</math>", r"\sum_{i=1}^n i"),
    ],
)
def test_extract_latex_variants(raw, expected):
    assert extract_latex(raw) == expected


@patch("backend.ocr.Image.open", return_value=None)
def test_predict_latex_none_image(mock_open):
    with pytest.raises(ValueError, match="Image is None"):
        predict_latex("dummy_path.png")


@patch("backend.ocr.predictor")
def test_predict_latex_empty_prediction(mock_predictor):
    mock_predictor.return_value = []
    result = predict_latex("tests/assets/formula_sample.png")
    assert result == ""
