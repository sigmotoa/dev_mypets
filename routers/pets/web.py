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
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/pets", response_class=HTMLResponse)
async def pets_list(request: Request, session: Session = Depends(get_session)):
    pets = await crud.get_all_pets(session=session)
    return templates.TemplateResponse("pets/list.html",
                                      {"request": request, "pets": pets})
