from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, Response
from sqlmodel import Session

from routers.pets.web import router
from sqlmodel_conn import get_session
from sqlmodel_db import PetSQL
import sqlmodel_ops as crud
from utils.terms import Kind, Genre
from utils.file_utils import upload_img_supabase

router = APIRouter(prefix="/api")

@router.get("/pets", response_model=list[PetSQL], tags=["SQLMODEL"])
async def read_pets_img(session:Session = Depends(get_session)):
    pets = await crud.get_all_pets(session=session)
    return pets




@router.post("/pets", response_model=PetSQL, tags=["SQLMODEL"])
async def create_pet_img(
        name: str = Form(...),
    breed: Optional[str] = Form(None),
    birth: Optional[int] = Form(None),
    kind: Optional[Kind] = Form(None),
    genre: Optional[Genre] = Form(None),
    image: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session)
):

    image_url= await upload_img_supabase(image)
    #print("OK", image_url)

    pet_data=PetSQL(
        name=name,
        breed=breed,
        birth=birth,
        kind=kind,
        genre=genre,
        image_path=image_url

    )
    pet = await crud.create_pet_sql(session, pet_data)

    session.add(pet)
    #await session.commit()
    #await session.refresh(pet)
    return pet
