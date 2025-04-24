from PIL import Image
from surya.texify import TexifyPredictor
import re

predictor = TexifyPredictor()


def predict_latex(image_path):
    try:
        image = Image.open(image_path)
    except Exception as e:
        raise ValueError(f"Failed to load image: {e}")
    if image is None:
        raise ValueError("Image is None — could not be loaded")

    prediction = predictor([image])
    if prediction and len(prediction) > 0:
        return extract_latex(str(prediction[0]))
    return ""


def extract_latex(text):
    if text.startswith("text="):
        text = text[len("text="):].strip()
    if "confidence=" in text:
        text = text.split("confidence=")[0].strip()
    if len(text) >= 2 and text[0] in ['"', "'"] and text[-1] in ['"', "'"]:
        text = text[1:-1]
    if text.startswith("<math"):
        text = re.sub(r"<math[^>]*>", "", text)
        text = text.replace("</math>", "")
    return text.strip()


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
