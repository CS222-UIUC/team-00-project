import sys
import torch
import numpy as np
import cv2


from CS222.classify_formula import (
    main,
    connected_components,
    preprocess_symbol,
    build_model,
    load_model,
    classify_symbols,
)


def test_main_no_symbols(monkeypatch, tmp_path, capsys):
    blank = np.full((50, 50), 255, dtype=np.uint8)
    img_path = tmp_path / "blank.png"
    cv2.imwrite(str(img_path), blank)
    monkeypatch.setattr(sys, "argv", ["clf", str(img_path)])
    main()
    out = capsys.readouterr().out
    assert "No symbols found." in out


def test_connected_components_empty(tmp_path):
    blank = np.full((50, 50), 255, dtype=np.uint8)
    path = tmp_path / "b.png"
    cv2.imwrite(str(path), blank)
    assert connected_components(str(path)) == []


def test_connected_components_simple(tmp_path):
    img = np.full((100, 100), 255, dtype=np.uint8)
    cv2.rectangle(img, (10, 10), (30, 30), 0, -1)
    path = tmp_path / "s.png"
    cv2.imwrite(str(path), img)
    comps = connected_components(str(path), min_area=5)
    assert len(comps) == 1
    h, w = comps[0].shape
    assert 18 < h <= 25 and 18 < w <= 25


def test_preprocess_symbol_shape():
    dummy = np.zeros((50, 50), dtype=np.uint8)
    t = preprocess_symbol(dummy)
    assert isinstance(t, torch.Tensor)
    assert t.shape == (1, 28, 28)


def test_build_and_load_model(tmp_path):
    m1 = build_model(num_classes=3, device="cpu")
    path = tmp_path / "w.pth"
    torch.save(m1.state_dict(), str(path))
    m2 = load_model(str(path), num_classes=3, device="cpu")
    assert isinstance(m2, torch.nn.Module)


class DummyModel(torch.nn.Module):

    def __init__(self):
        super().__init__()

    def forward(self, x):
        b = x.size(0)
        out = torch.zeros(b, 2)
        out[:, 1] = 1.0
        return out


def test_classify_symbols_dummy():
    sym = np.zeros((28, 28), dtype=np.uint8)
    labels = classify_symbols(DummyModel(), "cpu", ["zero", "one"], [sym])
    assert labels == ["one"]
