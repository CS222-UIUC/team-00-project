from fastapi import FastAPI
from pydantic import BaseModel
from model import get_latex  # local model


app = FastAPI()


# Request
class Prompt(BaseModel):
    text: str


# Post
@app.post("/latex")
def generate_latex(prompt: Prompt):
    latex = get_latex(prompt.text)
    return {"latex": latex}
