from fastapi import FastAPI
from fastapi import HTTPException
from starlette.responses import JSONResponse
from models import Pet,PetResponse,PetWithId
from operations import *
from typing import List

app = FastAPI()


#pets:List[Pet]=[]
'''@app.post("/pet", response_model=Pet)
async def create_pet(pet:Pet):
    #pets.append(pet)
    return pet
'''

@app.get("/allpets", response_model=list[PetWithId])
async def show_all_pets():
    pets=read_all_pets()
    return pets

    '''return [
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
    ]'''


@app.get("/pet/{pet_id}", response_model=PetWithId)
async def show_pet(pet_id:int):
    pet= read_one_pet(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet doesnt found")
    return pet

##Adding a pet into the database
@app.post("/pet", response_model=PetWithId)
def add_pet(pet:Pet):
    return new_pet(pet)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request,exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message":"Carambas, algo fallo"
        },
    )


@app.get("/error")
async def raise_exception():
    raise HTTPException(status_code=400)