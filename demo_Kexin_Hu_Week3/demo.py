import os
from difflib import SequenceMatcher
from PIL import Image
from surya.texify import TexifyPredictor

image_folder = "math_formulas"

ground_truths = {
    "formula1.png": '<math display="block">\\mathbf{M}\\mathbf{x} = \\mathbf{x}</math>',
    "formula2.png": '<math display="block">\\mathbf{A}\\mathbf{x}^* = \\mathbf{x}^*</math>',
    "formula3.png": "<math>A_{ij} = 1</math>",
    "formula4.png": (
        '<math display="block">'
        "(\\mathbf{A} - \\sigma \\mathbf{I})^{-1} \\mathbf{x} = "
        "\\frac{1}{\\lambda - \\sigma} \\mathbf{x}"
        "</math>"
    ),
    "formula5.png": (
        '<math display="block">'
        "\\mathbf{x}_0 = \\alpha_1 \\mathbf{u}_1 + "
        "\\alpha_2 \\mathbf{u}_2 + \\cdots + "
        "\\alpha_n \\mathbf{u}_n"
        "</math>"
    ),
    "formula6.png": "<math>\\det(\\mathbf{A} - \\lambda \\mathbb{I}) = 0</math>",
    "formula7.png": "<math>\\int x^n \\, dx = \\frac{x^{n+1}}{n+1} + C</math>",
}

predictor = TexifyPredictor()


def extract_math(text):
    """
    Extracts only the LaTeX math expression from the recognized string.
    Strip out the unwanted parts (the "text=" prefix and the "confidence=..." suffix)
    """
    if text.startswith("text="):
        text = text[len("text=") :].strip()
    if "confidence=" in text:
        text = text.split("confidence=")[0].strip()
    if len(text) >= 2 and text[0] in ['"', "'"] and text[-1] in ['"', "'"]:
        text = text[1:-1]
    return text


def similarity(a, b):
    """Return the similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()


total = 0
total_similarity = 0.0

for filename, expected_formula in ground_truths.items():
    image_path = os.path.join(image_folder, filename)
    if not os.path.exists(image_path):
        print(f"File not found: {filename}, skipping.")
        continue

    image = Image.open(image_path)
    predictions = predictor([image])

    if predictions and len(predictions) > 0:
        recognized_formula = str(predictions[0])
    else:
        recognized_formula = ""

    cleaned_formula = extract_math(recognized_formula)

    sim_ratio = similarity(expected_formula, cleaned_formula)

    print(f"File: {filename}")
    print(f"Cleaned Recognized LaTeX: '{cleaned_formula}'")
    print(f"Expected LaTeX:           '{expected_formula}'")
    print(f"Similarity Ratio: {sim_ratio:.2f}\n")

    total += 1
    total_similarity += sim_ratio

avg_similarity = (total_similarity / total) * 100 if total > 0 else 0
print(f"Average Fuzzy LaTeX OCR Accuracy on {total} images: {avg_similarity:.2f}%")
