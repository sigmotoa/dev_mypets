from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, Response
from sqlmodel import Session

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
from utils.terms import Kind, Genre
from utils.file_utils import upload_img_supabase

router = APIRouter(prefix="/other")

pets:List[Pet]=[]
@router.post("/pet", response_model=Pet)
async def create_pet(pet:Pet):
    #pets.append(pet)
    return pet



@router.post("/dbpet", response_model=dict[str, int])
async def add_pet_db(pet: models.Pet, db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    pet_id=await db_create_pet(db_session,
                               pet.name,
                               pet.breed,
                               pet.birth,
                               pet.kind,
                               pet.female, )
    return {"Nueva mascota":pet_id}


@router.get("/dbpet/{pet_id}", response_model=PetWithId)
async def one_pet_db(pet_id:int, db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    pet= await db_get_pet(db_session=db_session, pet_id=pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="No esta la mascota "+{pet_id})
    return pet


@router.get("/dballpets", response_model=list[PetWithId])
async def all_pet_db(db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    pets = await db_get_all_pet(db_session=db_session)
    if pets is None:
        raise HTTPException(status_code=404, detail="No tenemos mascotas")
    return pets


@router.put("/dbpet/{pet_id}")
async def modify_name_db(pet_id:int,new_name:str,db_session:Annotated[AsyncSession, Depends(get_db_session)]):
    pet = await db_update_pet(db_session=db_session,pet_id=pet_id,new_name=new_name)
    return pet


@router.delete("/dbpet/{pet_id}")
async def delete_pet_db(pet_id:int, db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    pet = await db_remove_pet(pet_id=pet_id, db_session=db_session)
    return pet

