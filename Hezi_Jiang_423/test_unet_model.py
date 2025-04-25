# test_unet_model.py

import numpy as np
import torch
from unet_model import UNet, segment_symbols_unet
import pytest

def create_dummy_image():
    return np.ones((128, 128), dtype=np.uint8) * 255

def test_segment_symbols_unet_valid():
    model = UNet()
    img = create_dummy_image()
    symbols = segment_symbols_unet(img, model, threshold=0.5)
    assert isinstance(symbols, list)
    assert all(isinstance(sym, np.ndarray) for sym in symbols)

def test_segment_symbols_unet_invalid_input():
    model = UNet()
    with pytest.raises(ValueError):
        segment_symbols_unet(12345, model)
