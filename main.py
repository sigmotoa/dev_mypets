from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.testing.plugin.plugin_base import engines
from starlette.responses import JSONResponse

import models
from models import *
from operations import *
from typing import List
from contextlib import asynccontextmanager
from database import Base
from db_connection import AsyncSessionLocal, get_db_session, get_engine
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from db_operations import *


@asynccontextmanager
async def lifespan(app:FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()
app = FastAPI(lifespan=lifespan)


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


@app.post("/dbpet", response_model=dict[str, int])
async def add_pet(pet: models.Pet, db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    pet_id=await create_pet(db_session,
                            pet.name,
                            pet.breed,
                            pet.birth,
                            pet.kind,
                            pet.female,)
    return {"Nueva mascota":pet_id}

