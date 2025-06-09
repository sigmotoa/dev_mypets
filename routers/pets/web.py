from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session

# Modelos y operaciones
from sqlmodel_conn import get_session
from sqlmodel_db import PetSQL
import sqlmodel_ops as crud
from utils.terms import Kind, Genre
from utils.file_utils import upload_img_supabase

router = APIRouter()

templates = Jinja2Templates(directory="templates")





@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("pets/home.html", {"request": request})


# All pets
@router.get("/pets", response_class=HTMLResponse)
async def pets_list(request: Request, session: Session = Depends(get_session)):
    pets = await crud.get_all_pets(session=session)
    return templates.TemplateResponse("pets/list.html",
                                      {"request": request, "pets": pets, "view_type": "list", "show_actions": False,
                                       "show_full_image": False})


@router.get("/new", response_class=HTMLResponse)
async def create_pet(request: Request):
    return templates.TemplateResponse("pets/create.html", {
        "request": request,
        "kinds": [kind.value for kind in Kind],
        "genres": [genre.value for genre in Genre]
    })


@router.post("/new", response_class=HTMLResponse)
async def create_pet_process(
        request: Request,
        name: str = Form(...),
        breed: Optional[str] = Form(None),
        birth: Optional[int] = Form(None),
        kind: Optional[Kind] = Form(None),
        genre: Optional[Genre] = Form(None),
        image: Optional[UploadFile] = File(None),
        session: Session = Depends(get_session)
):
    image_url = await upload_img_supabase(image)

    pet_data = PetSQL(
        name=name,
        breed=breed,
        birth=birth,
        kind=kind,
        genre=genre,
        image_path=image_url

    )
    pet = await crud.create_pet_sql(session, pet_data)

    session.add(pet)

    return RedirectResponse("/web/pets", status_code=303)


@router.get("/pets/search")
async def search_pet(q: str):
    id = int(q)
    return RedirectResponse(f"/web/pets/{id}", status_code=303)

@router.get("/pets/{pet_id}", response_class=HTMLResponse)
async def one_pet(request: Request, pet_id: int, session: Session = Depends(get_session)):
    pet = await crud.get_pet(session=session, pet_id=pet_id)
    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Amigo no encontrado"
        )
    # "request": request, "pets": pets, "view_type":"list", "show_actions":False, "show_full_image":False
    return templates.TemplateResponse("pets/pet.html",
                                      {"request": request, "pet": pet, "view_type": "detail", "show_actions": False,
                                       "show_full_image": True})



