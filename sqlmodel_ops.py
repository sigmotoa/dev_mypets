from sqlmodel import Session, select
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