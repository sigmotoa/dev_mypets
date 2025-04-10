from sqlmodel import Session, select
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlmodel_db import Pet

#Creation of one pet in DB
async def create_pet_sql(session: Session, pet:Pet):
    db_pet = Pet.from_orm(pet)
    db_pet.created_at = datetime.now()

    session.add(db_pet)
    session.commit()
    session.refresh(db_pet)

    return db_pet