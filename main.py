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
from starlette.exceptions import HTTPException as StarletteHTTPException
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
from routers.pets import others as others


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

app.include_router(pets.router, tags=["WEB"])
app.include_router(api.router, tags=["API"])
app.include_router(file.router, tags=["CSV"])
app.include_router(others.router, tags=["Others"])

@app.get("/")
async def home():
    return pets.home()



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

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:

        detail = getattr(exc, "detail", None)
        return templates.TemplateResponse("404.html", {"request": request, "detail": detail}, status_code=404)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": "¡Carambas, algo falló!",
            "detail": str(exc.detail),
            "path": str(request.url)
        },
    )



@app.get("/error")
async def raise_exception():
    raise HTTPException(status_code=400)

