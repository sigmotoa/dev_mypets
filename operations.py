import csv
from typing import Optional


from models import *

DATABASE_FILENAME = "pets.csv"
column_fields = ["id", "name", "breed", "birth", "kind", "female"]


#show all pets in file
def read_all_pets():
    with open(DATABASE_FILENAME) as csvfile:
        reader = csv.DictReader(
            csvfile,
        )
        return [PetWithId(**row) for row in reader]


##Show a pet by the ID
def read_one_pet(pet_id):
    with open(DATABASE_FILENAME) as csvfile:
        reader=csv.DictReader(
            csvfile,
        )
        for row in reader:
            if int(row["id"])==pet_id:
                return PetWithId(**row)


##Add a pet in the file
#neccesary to implements a strategy for the ID of the new pet.
#First obtain the last ID from the db.
#Then create the new pet with the new ID

##First
def get_next_ID():
    try:
        with open(DATABASE_FILENAME, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            max_id=max(int(row["id"])for row in reader)
            return (max_id +1)
    except(FileNotFoundError, ValueError):
        return 1


##Write or save a new pet in CSV
def write_pet_into_csv(pet:PetWithId):
    with open(DATABASE_FILENAME, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=column_fields,)
        writer.writerow(pet.model_dump())


##Then, create a new pet
def new_pet(pet:Pet):
    id:int=get_next_ID()
    pet_with_id=PetWithId(id=id, **pet.model_dump())
    write_pet_into_csv(pet_with_id)
    return pet_with_id

#Edit a pet
def modify_pet(id: int, pet: dict):
    updated_pet: Optional[PetWithId] = None
    pets = read_all_pets()


    pet_found = False

    # Iterate through pets to find and update the specific pet
    for number, pet_ in enumerate(pets):
        if pet_.id == id:

            if pet.get("name") is not None:
                pets[number].name = pet["name"]
            if pet.get("breed") is not None:
                pets[number].breed = pet["breed"]

            updated_pet = pets[number]
            pet_found = True
            break  # Exit the loop once the pet is found and updated

    # Only write to file if a pet was actually modified
    if pet_found:
        with open(DATABASE_FILENAME, mode="w", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=column_fields,
            )
            writer.writeheader()
            for pet in pets:
                writer.writerow(pet.model_dump())

        return updated_pet

    # Return None if no pet was found
    return None


#Delete a pet
def remove_pet(id:int):
    deleted_pet: Optional[Pet] = None
    pets =read_all_pets()
    with open(DATABASE_FILENAME, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields,
        )

        writer.writeheader()
        for pet in pets:
            if pet.id == id:
                deleted_pet=pet
                continue
            writer.writerow(pet.model_dump())
    if deleted_pet:
        dict_pet_without_id = (
            deleted_pet.model_dump()
        )
        del dict_pet_without_id["id"]
        return Pet(**dict_pet_without_id)