import os
import cv2
import torch
import json
import sys

from classify_formula import connected_components, load_model, classify_symbols

MODEL_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "..", "..", "Final_Handwritting_Recognizer_Model"
    )
)
if MODEL_DIR not in sys.path:
    sys.path.insert(0, MODEL_DIR)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class_path = os.path.join(MODEL_DIR, "classes.json")
model_path = os.path.join(MODEL_DIR, "resnet_handwritten.pth")

with open(class_path, "r") as f:
    class_names = json.load(f)

_model = load_model(model_path, len(class_names), device)


def predict_latex(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not load image '{image_path}'")

    symbols = connected_components(img, min_area=10)
    if not symbols:
        return ""

    labels = classify_symbols(_model, device, class_names, symbols)
    return "".join(labels)


def wrap_latex(latex_body):
    return (
        r"""
\documentclass{article}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{bm}
\begin{document}
\[
"""
        + latex_body
        + r"""
\]
\end{document}
"""
    )
