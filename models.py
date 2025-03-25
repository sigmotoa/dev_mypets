from pydantic import BaseModel

class Pet(BaseModel):
    name:str
    breed:str
    birth:int
    kind:str


