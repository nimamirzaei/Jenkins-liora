from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "We Love Liora, and we did it. We built a CI/CD Pipeline!"}