import os
import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile
from typing import Optional
from PIL import Image, ImageOps

#Decide the directory for save the pets images
SAVE_DIRECTORY="pet_images"
ALLOWED_EXT={".jpg", ".jpeg", ".png",".bmp"}

#Create the directory
parent_path = os.path.dirname(os.getcwd())
save_path = os.path.join(parent_path, SAVE_DIRECTORY)

os.makedirs(save_path, exist_ok=True)

#saving a file
async def save_upload_file(
        upload_file:UploadFile,
        pet_id:int,
        pet_name:Optional[str] =None
):
    file_ext=Path(upload_file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXT:
        raise ValueError("Archivo no permitido")

    #Crear nombre para archivo
    base_name= f"pet_{pet_id}"

    if pet_name:
        base_name=f"{base_name}{pet_name}"
    #Naming the file
    file_name = f"{base_name}_{uuid.uuid4().hex[:8]}{file_ext}"

    #Make the path
    file_path=os.path.join(save_path, file_name)

    #save the filee
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    #Close the file
    await upload_file.close()

    return file_path

