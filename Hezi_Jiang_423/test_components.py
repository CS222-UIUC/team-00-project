# connected components
import cv2
import numpy as np
from connected_components import connected_components


def create_test_image():
    img = np.ones((100, 200), dtype=np.uint8) * 255
    cv2.putText(img, "1+2", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,), 5, cv2.LINE_AA)
    return img


def test_connected_components_extraction():
    img = create_test_image()
    symbol_imgs = connected_components(img)

    assert isinstance(symbol_imgs, list)
    assert len(symbol_imgs) == 3
    for sym in symbol_imgs:
        assert isinstance(sym, np.ndarray)
        assert sym.size > 0
        assert sym.ndim == 2


def test_empty_image():
    img = np.zeros((100, 100), dtype=np.uint8)
    assert connected_components(img) == []
