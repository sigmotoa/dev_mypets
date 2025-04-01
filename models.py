from typing import Optional

from pydantic import BaseModel, Field

class Pet(BaseModel):
    name:str = Field(..., min_length=3, max_length=20)
    breed:str = Field(...,min_length=3,max_length=25)
    birth:int = Field(...,gt=2000,lt=2025)
    kind:str = Field(...,min_length=3,max_length=25)
    female:bool=Field(...)

class PetWithId(Pet):
    id:int

    #For more info for validations look at:
    #https: // docs.pydantic.dev / latest / concepts / fields /


class PetResponse(BaseModel):
    name:str
    kind:str


class UpdatedPet(BaseModel):
    name: Optional[str] = Field(..., min_length=3, max_length=20)
    breed:Optional[str] = Field(..., min_length=3, max_length=25)


