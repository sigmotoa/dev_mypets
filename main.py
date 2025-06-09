from datetime import datetime
from http.client import responses

from aiohttp import request
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

from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.responses import RedirectResponse

#Imports for templates
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_404_NOT_FOUND
from websockets.legacy.server import HTTPResponse

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
from routers.pets.web import router

#Importar modelos SQLMODEL
from sqlmodel_conn import get_session, init_db
from sqlmodel_db import PetSQL
import sqlmodel_ops as crud
from sqlmodel_ops import get_pet, mark_pet_inactive
from utils.file_utils import save_upload_file, upload_img_supabase
from utils.terms import *
from utils import file_utils

from routers.pets import web as pets
from routers.pets import api as api
from routers.pets import file as file


@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Pets de sigmotoa",
    description="Mascotas de los amigos de sigmotoa",
    version="2.0.0",
    lifespan=lifespan)
app.mount("/pet_images", StaticFiles(directory="pet_images"), name="pet_images")

templates = Jinja2Templates(directory="templates")

app.include_router(pets.router, tags=["WEB"], prefix="/web")
app.include_router(api.router, tags=["API"])
app.include_router(file.router, tags=["CSV"])

@app.get("/")
async def home():
    return pets.home()



'''
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
'''









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

'''
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
    ]'''




@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request,exc):
    if exc.status_code == HTTP_404_NOT_FOUND:
        return templates.TemplateResponse("404.html", {"request":request}, status_code=404)
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

