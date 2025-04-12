from tkinter.constants import CURRENT
from typing import Optional

from pydantic import ConfigDict
from sqlalchemy import Boolean, table
from sqlmodel import Field, SQLModel, create_engine, Session, select
from datetime import datetime
from utils.terms import *

CURRENT_YEAR=datetime.now().year
#Creation of the basic model of the pets
class PetBase(SQLModel):
    name: str = Field(index=True, min_length=3, max_length=20)
    breed:str = Field(default=None, min_length=3, max_length=30)
    #Using new types to be pro 🤓
    birth: Optional[int] = Field(default=None, le=CURRENT_YEAR)
    kind: Kind = Field(default=None)
    genre: Genre = Field(default=None)

    #Adding a new fields to look cool
    image_path: Optional[str]=Field(default=None)
    is_alive:bool = Field(default=True)
    created_at:datetime = Field(default_factory=datetime.now)
    updated_at:Optional[datetime] = Field(default=None)


class PetSQL(PetBase, table=True):
    __tablename__ = "pets"
    id: Optional[int] = Field(default=None, primary_key=True)

    model_config = ConfigDict(from_attributes=True)



