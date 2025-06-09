from typing import Optional, List
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


router = APIRouter(prefix="/file")

#show all pets
@router.get("/pet", response_model=list[PetWithId])
async def show_all_pets():
    pets=read_all_pets()
    return pets


@router.get("/pet/{pet_id}", response_model=PetWithId)
async def show_pet(pet_id:int):
    pet= read_one_pet(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet doesnt found")
    return pet

#Delete one pet by the ID
@router.delete("/pet/{pet_id}", response_model=Pet)
def delete_one_pet(pet_id:int):
    removed_pet=remove_pet(pet_id)
    if not removed_pet:
        raise HTTPException(
            status_code=404, detail="Pet not deleted"
        )
    return removed_pet

@router.put("/pet/{pet_id}", response_model=PetWithId)
def update_pet(pet_id:int, pet_update:UpdatedPet):
    modified=modify_pet(
        pet_id,pet_update.model_dump(exclude_unset=True),
    )
    if not modified:
        raise HTTPException(status_code=404, detail="Pet not modified")

    return modified


##Adding a pet into the file
@router.post("/pet", response_model=PetWithId)
def add_pet(pet:Pet):
    return new_pet(pet)

