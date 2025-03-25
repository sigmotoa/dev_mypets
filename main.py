from fastapi import FastAPI
from models import Pet

app = FastAPI()


@app.post("/pet")
async def create_pet(pet:Pet):
    return pet

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
