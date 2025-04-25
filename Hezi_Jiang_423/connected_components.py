import cv2


def connected_components(image_input, min_area=10):
    """
    Given an image of a handwritten formula, extract and return individual symbol images.

    Args:
        image_input: str (file path) or np.ndarray (image loaded already)
        min_area: minimum area to filter out small noise
    Returns:
        List of np.ndarray: each is a cropped image of a symbol
    """
    if isinstance(image_input, str):
        img = cv2.imread(image_input, cv2.IMREAD_GRAYSCALE)
    else:
        img = image_input.copy()

    _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary)

    symbols = []
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if area >= min_area and w < img.shape[1] and h < img.shape[0]:
            symbol_img = binary[y:y+h, x:x+w]
            symbols.append((x, symbol_img))

    symbols.sort(key=lambda item: item[0])
    return [img for (_, img) in symbols]
