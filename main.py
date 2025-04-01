from fastapi import FastAPI
from fastapi import HTTPException
from starlette.responses import JSONResponse
from models import *
from operations import *
from typing import List

app = FastAPI()


#pets:List[Pet]=[]
'''@app.post("/pet", response_model=Pet)
async def create_pet(pet:Pet):
    #pets.append(pet)
    return pet
'''

#show all pets
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


#show one pet
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


#modify one pet by ID
@app.put("/pet/{pet_id}", response_model=PetWithId)
def update_pet(pet_id:int, pet_update:UpdatedPet):
    modified=modify_pet(
        pet_id,pet_update.model_dump(exclude_unset=True),
    )
    if not modified:
        raise HTTPException(status_code=404, detail="Pet not modified")

    return modified

#Delete one pet by the ID
@app.delete("/pet/{pet_id}", response_model=Pet)
def delete_one_pet(pet_id:int):
    removed_pet=remove_pet(pet_id)
    if not removed_pet:
        raise HTTPException(
            status_code=404, detail="Pet not deleted"
        )
    return removed_pet

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
            "message":"Carambas, algo fallo",
            "detail":exc.detail,
            "path":request.url.path
        },
    )


@app.get("/error")
async def raise_exception():
    raise HTTPException(status_code=400)