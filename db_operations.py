from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import Pets

##Adding a pet in DB
async def db_create_pet(
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


##Looking for a pet in DB
async def db_get_pet(db_session:AsyncSession, pet_id:int):
    query = (select(Pets).where(Pets.id == pet_id))

    result=await db_session.execute(query)
    pet = result.scalars().first()

    return pet


##Retorning all pets in DB
async def db_get_all_pet(db_session:AsyncSession):
    query = (select(Pets))

    result=await db_session.execute(query)
    pets = result.scalars().all()

    return pets



#Update a pet, just the name
async def db_update_pet(db_session:AsyncSession, pet_id:int, new_name:str):
    query = (
        update(Pets)
        .where(Pets.id==pet_id)
        .values(name=new_name)
             )
    result = await db_session.execute(query)
    await db_session.commit()
    if result.rowcount==0:
        return False
    return True


#Remove a Pet of the DB
async def db_remove_pet(db_session:AsyncSession, pet_id:int):
    result = await db_session.execute(
        delete(Pets).where(Pets.id==pet_id)
    )
    await db_session.commit()
    if result.rowcount==0:
        return False
    return True