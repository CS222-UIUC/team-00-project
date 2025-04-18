from fastapi import FastAPI
from pydantic import BaseModel
from model import get_latex  # local model
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request
class Prompt(BaseModel):
    text: str


# Post
@app.post("/latex")
def generate_latex(prompt: Prompt):
    latex = get_latex(prompt.text)
    return {"latex": latex}
