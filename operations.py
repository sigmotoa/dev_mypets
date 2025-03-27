import csv
from typing import Optional
from models import Pet,PetWithId

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