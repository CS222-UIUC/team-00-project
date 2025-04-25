# unet_model.py

import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
import numpy as np
from torchvision import transforms


class UNet(nn.Module):

    def __init__(self, in_channels=1, out_channels=1):
        super().__init__()

        def CBR(in_c, out_c):
            return nn.Sequential(
                nn.Conv2d(in_c, out_c, 3, padding=1),
                nn.BatchNorm2d(out_c),
                nn.ReLU(inplace=True),
            )

        self.enc1 = nn.Sequential(CBR(in_channels, 64), CBR(64, 64))
        self.enc2 = nn.Sequential(CBR(64, 128), CBR(128, 128))
        self.pool = nn.MaxPool2d(2, 2)
        self.dec1 = nn.Sequential(CBR(128, 64), CBR(64, 64))
        self.final = nn.Conv2d(64, out_channels, 1)

    def forward(self, x):
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        d1 = F.interpolate(e2, scale_factor=2)
        d1 = self.dec1(d1)
        out = self.final(d1)
        return torch.sigmoid(out)


def segment_symbols_unet(image_input, model, threshold=0.5, min_area=10):
    if isinstance(image_input, str):
        image = cv2.imread(image_input, cv2.IMREAD_GRAYSCALE)
    elif isinstance(image_input, np.ndarray):
        image = image_input
    else:
        raise ValueError("Unsupported input type")

    h, w = image.shape
    tensor = transforms.ToTensor()(image).unsqueeze(0)

    with torch.no_grad():
        pred_mask = model(tensor)[0, 0].numpy()

    binary_mask = (pred_mask > threshold).astype(np.uint8) * 255

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_mask)

    symbols = []
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if area >= min_area:
            symbols.append(image[y : y + h, x : x + w])

    return symbols
