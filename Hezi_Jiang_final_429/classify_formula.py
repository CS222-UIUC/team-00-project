import argparse
import json
import cv2
import torch
import torch.nn as nn
from torchvision import models, transforms


def connected_components(image_input, min_area=10):
    if isinstance(image_input, str):
        img = cv2.imread(image_input, cv2.IMREAD_GRAYSCALE)
    else:
        img = image_input.copy()
    _, binary = cv2.threshold(
        img, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary)

    symbols = []
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if area >= min_area and w < img.shape[1] and h < img.shape[0]:
            pad = 2
            sy = max(0, y - pad)
            ey = min(img.shape[0], y + h + pad)
            sx = max(0, x - pad)
            ex = min(img.shape[1], x + w + pad)

            symbol_img = img[sy:ey, sx:ex]
            symbols.append((x, symbol_img))

    symbols.sort(key=lambda item: item[0])
    return [img for (_, img) in symbols]


def build_model(num_classes, device):
    model = models.resnet18(pretrained=False)
    model.conv1 = nn.Conv2d(1, 64, kernel_size=7,
                            stride=2, padding=3, bias=False)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model = model.to(device)
    return model


def load_model(weights_path, num_classes, device):
    model = build_model(num_classes, device)
    state = torch.load(weights_path, map_location=device)
    model.load_state_dict(state)
    model.eval()
    return model


def preprocess_symbol(sym_img):
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
    ])
    return transform(sym_img)


def classify_symbols(model, device, class_names, symbols):
    results = []
    with torch.no_grad():
        for sym in symbols:
            inp = preprocess_symbol(sym).unsqueeze(0).to(device)
            logits = model(inp)
            pred = logits.argmax(dim=1).item()
            results.append(class_names[pred])
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Segment a formula and classify each symbol"
    )
    parser.add_argument('image', help="path to formula image")
    parser.add_argument('--model', default='CS222/resnet_handwritten.pth',
                        help="path to trained weights")
    parser.add_argument('--classes', default='CS222/classes.json',
                        help="path to classes.json")
    parser.add_argument('--min_area', type=int, default=10,
                        help="minimum CC area to keep")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    class_names = json.load(open(args.classes))

    model = load_model(args.model, len(class_names), device)

    symbols = connected_components(args.image, min_area=args.min_area)
    if not symbols:
        print("No symbols found.")
        return

    labels = classify_symbols(model, device, class_names, symbols)

    print("Recognized:", " ".join(labels))


if __name__ == "__main__":
    main()
