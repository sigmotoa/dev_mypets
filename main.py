from fastapi import FastAPI
from models import Pet,PetResponse

app = FastAPI()


@app.post("/pet")
async def create_pet(pet:Pet):
    return pet


@app.get("/allpets", response_model=list[PetResponse])
async def show_all_pets():
    return [
        {
            "id":1,
            "name":"chispas",
            "kind":"cat"
        },
        {
            "id":2,
            "name":"pascal",
            "kind":"cat"
        },
        {
            "id":3,
            "name":"elefante",
            "kind":"dog"
        }
    ]
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
