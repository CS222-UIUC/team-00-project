from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
import json
import cv2
import numpy as np
from classify_formula import connected_components, load_model, classify_symbols

app = FastAPI()

# Allow frontend from any domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model on startup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class_path = "./classes.json"
model_path = "./resnet_handwritten.pth"

with open(class_path) as f:
    class_names = json.load(f)

model = load_model(model_path, len(class_names), device)


@app.post("/classify")
async def classify_formula(image: UploadFile = File(...)):
    try:
        # Read image from the request
        contents = await image.read()
        np_img = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_GRAYSCALE)

        # Segment and classify
        symbols = connected_components(img, min_area=10)
        if not symbols:
            return JSONResponse(
                {"result": [], "error": "No symbols found."}, status_code=200
            )

        labels = classify_symbols(model, device, class_names, symbols)

        return {"result": labels}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
