from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import Pets

async def create_pet(
        db_session:AsyncSession,
        name:str,
        breed:str=None,
        birth:int=None,
        kind:str=None,
        female:bool=None,
):
    pet = Pets(
        name=name,
        breed=breed,
        birth=birth,
        kind=kind,
        female=female,
    )
    async with db_session.begin():
        db_session.add(pet)
        await db_session.flush()
        pet_id = pet.id
        await db_session.commit()
    return pet_id