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