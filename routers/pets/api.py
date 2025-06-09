from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, Response
from sqlmodel import Session


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


#Get one pet
@router.get("/pets/{pet_id}", response_model=PetSQL, tags=["SQLMODEL"])
async def read_pet_img(pet_id:int, session:Session = Depends(get_session)):
    pet = await crud.get_pet(session=session, pet_id=pet_id)
    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Mascota con img no encontrada"
        )
    return pet


#Get all pets

@router.get("/pets", response_model=list[PetSQL], tags=["SQLMODEL"])
async def read_pets_img(session:Session = Depends(get_session)):
    pets = await crud.get_all_pets(session=session)
    return pets



#Update one pet
@router.patch("/pets/{pet_id}", response_model=PetSQL, tags=["SQLMODEL"])
async def update_pet_img(pet_id:int, pet_update:PetSQL,session:Session=Depends(get_session)):
    pet = await crud.update_pet(session, pet_id, pet_update.dict(exclude_unset=True))
    if pet is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada para actualizar")
    return pet


#Deactive a pet
@router.patch("/pets/{pet_id}", response_model=PetSQL, tags=["SQLMODEL"])
async def deactive_pet_img(pet_id:int, sesion:Session=Depends(get_session)):
    pet = await crud.mark_pet_inactive(sesion, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada para desactivar")
    return pet