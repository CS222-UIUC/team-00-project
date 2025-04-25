# faster rnn
import numpy as np
from detect_symbols import detect_symbols_frcnn
import pytest


def create_dummy_image():
    img = np.ones((200, 200, 3), dtype=np.uint8) * 255
    return img


def test_detect_symbols_empty_image():
    img = create_dummy_image()
    symbols = detect_symbols_frcnn(img, confidence_threshold=0.9)
    assert isinstance(symbols, list)
    assert all(isinstance(s, np.ndarray) for s in symbols)


def test_detect_symbols_real_image():
    symbols = detect_symbols_frcnn("test.jpg", confidence_threshold=0.1)
    assert isinstance(symbols, list)
    assert all(isinstance(s, np.ndarray) for s in symbols)


def test_invalid_input_type():
    with pytest.raises(ValueError):
        detect_symbols_frcnn(12345)
