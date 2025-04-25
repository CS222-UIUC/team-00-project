# detect_symbols.py

import torch
import torchvision
from torchvision import transforms
from PIL import Image
import numpy as np


def detect_symbols_frcnn(image_input, confidence_threshold=0.5):
    if isinstance(image_input, str):
        image = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, np.ndarray):
        image = Image.fromarray(image_input).convert("RGB")
    elif isinstance(image_input, Image.Image):
        image = image_input.convert("RGB")
    else:
        raise ValueError("Unsupported image input type")

    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    img_tensor = transform(image)

    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()

    with torch.no_grad():
        predictions = model([img_tensor])[0]

    boxes = predictions['boxes']
    scores = predictions['scores']

    cropped = []
    for box, score in zip(boxes, scores):
        if score >= confidence_threshold:
            xmin, ymin, xmax, ymax = box.int().tolist()
            cropped_img = img_tensor[:, ymin:ymax, xmin:xmax]
            cropped_img = cropped_img.mul(255).byte().permute(1, 2, 0).numpy()
            cropped.append(cropped_img)

    return cropped
