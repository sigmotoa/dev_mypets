from datetime import datetime

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy import Boolean

#SQLMODEL
from fastapi import UploadFile, File, Form, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlmodel import Session
from typing import List, Optional

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

#Importar modelos SQLMODEL
from sqlmodel_conn import get_session, init_db
from sqlmodel_db import PetSQL
import sqlmodel_ops as crud
from sqlmodel_ops import get_pet
from utils.file_utils import save_upload_file
from utils.terms import *
from utils import file_utils

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/pet_images", StaticFiles(directory="pet_images"), name="pet_images")

##Pets with IMAGE
@app.post("/pets", response_model=PetSQL, tags=["SQLMODEL"])
async def create_pet_img(
        name: str = Form(...),
    breed: Optional[str] = Form(None),
    birth: Optional[int] = Form(None),
    kind: Optional[Kind] = Form(None),
    genre: Optional[Genre] = Form(None),
    image: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session)
):

    pet_data=PetSQL(
        name=name,
        breed=breed,
        birth=birth,
        kind=kind,
        genre=genre,

    )
    pet = await crud.create_pet_sql(session, pet_data)

    if image:
        try:
            image_path = await save_upload_file(image, pet.id, pet.name)
            pet.image_path = image_path
            session.add(pet)
            await session.commit()
            await session.refresh(pet)
        except ValueError as e:
            return JSONResponse(
                status_code=201,
                content={
                    "id":pet.id,
                    "warning":str(e),
                    **pet.dict(exclude={"id"})
                }
            )
    return pet


@app.get("/pets/{pet_id}", response_model=PetSQL, tags=["SQLMODEL"])
async def read_pet_img(pet_id:int, session:Session = Depends(get_session)):
    pet = await crud.get_pet(session=session, pet_id=pet_id)
    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Mascota con img no encontrada"
        )
    return pet


@app.get("/pets", response_model=list[PetSQL], tags=["SQLMODEL"])
async def read_pets_img(session:Session = Depends(get_session)):
    pets = await crud.get_all_pets(session=session)
    return pets


''' 
@asynccontextmanager
async def lifespan(app:FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()
app = FastAPI(lifespan=lifespan)

'''
#pets:List[Pet]=[]
@app.post("/pet", response_model=Pet)
async def create_pet(pet:Pet):
    #pets.append(pet)
    return pet


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
async def add_pet_db(pet: models.Pet, db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    pet_id=await db_create_pet(db_session,
                               pet.name,
                               pet.breed,
                               pet.birth,
                               pet.kind,
                               pet.female, )
    return {"Nueva mascota":pet_id}


@app.get("/dbpet/{pet_id}", response_model=PetWithId)
async def one_pet_db(pet_id:int, db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    pet= await db_get_pet(db_session=db_session, pet_id=pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="No esta la mascota "+{pet_id})
    return pet


@app.get("/dballpets", response_model=list[PetWithId])
async def all_pet_db(db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    pets = await db_get_all_pet(db_session=db_session)
    if pets is None:
        raise HTTPException(status_code=404, detail="No tenemos mascotas")
    return pets


@app.put("/dbpet/{pet_id}")
async def modify_name_db(pet_id:int,new_name:str,db_session:Annotated[AsyncSession, Depends(get_db_session)]):
    pet = await db_update_pet(db_session=db_session,pet_id=pet_id,new_name=new_name)
    return pet


@app.delete("/dbpet/{pet_id}")
async def delete_pet_db(pet_id:int, db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    pet = await db_remove_pet(pet_id=pet_id, db_session=db_session)
    return pet

