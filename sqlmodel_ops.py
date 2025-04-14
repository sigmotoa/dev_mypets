from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlmodel_db import PetSQL

#Creation of one pet in DB
async def create_pet_sql(session: Session, pet:PetSQL):
    db_pet = PetSQL.model_validate(pet, from_attributes=True)
    db_pet.created_at = datetime.now()

    session.add(db_pet)
    await session.commit()
    await session.refresh(db_pet)

    return db_pet


#Get pet by the id
async def get_pet(session:Session, pet_id:int):
    return await session.get(PetSQL, pet_id)


#Get all pets of the list
async def get_all_pets(session:Session):
    query = select(PetSQL)
    results = await session.exec(query)
    pets = results.all()
    return pets

#update_pet
async def update_pet(session:Session, pet_id:int, pet_update:Dict[str, Any]):
    pet = await session.get(PetSQL, pet_id)
    if pet is None:
        return None

    pet_data = pet.dict()
    for key, value in pet_update.items():
        if value is not None:
            pet_data[key]=value

    pet_data["updated_at"] = datetime.now()

    for key, value in pet_data.items():
        setattr(pet, key, value)

    session.add(pet)
    await session.commit()
    await session.refresh(pet)

    return pet

#Modify pet status.
async def mark_pet_inactive(session:Session, pet_id:int):
    return await update_pet(session, pet_id, {"is_alive":False,"updated_at":datetime.now()})