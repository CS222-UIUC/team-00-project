import os
import pytest
from backend.ocr import predict_latex, wrap_latex
from unittest.mock import patch


def test_predict_latex_dummy():
    dummy_path = "tests/assets/formula_sample.png"
    assert os.path.exists(
        dummy_path
    ), "Make sure tests/assets/formula_sample.png exists"
    latex = predict_latex(dummy_path)
    assert isinstance(latex, str)
    assert len(latex) > 0


def test_wrap_latex_basic():
    body = r"\alpha + \beta = \gamma"
    wrapped = wrap_latex(body)
    assert r"\documentclass{article}" in wrapped
    assert body in wrapped
    assert r"\end{document}" in wrapped


def test_predict_latex_invalid_path():
    with pytest.raises(ValueError):
        predict_latex("nonexistent_file.png")


@patch("backend.ocr.connected_components", return_value=[])
def test_predict_latex_no_symbols(mock_cc):
    # If segmentation finds no symbols, predict_latex should return empty string
    dummy_path = "tests/assets/formula_sample.png"
    result = predict_latex(dummy_path)
    assert result == ""
