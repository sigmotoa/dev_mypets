
from supabase import create_client
from dotenv import load_dotenv
import os
import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile
from typing import Optional
from PIL import Image, ImageOps

#from probe_supabase import supabase

# Decide the directory for save the pets images
SAVE_DIRECTORY = "pet_images"
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".bmp"}
# ENVIRONMENT VARIABLES
load_dotenv()
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create the directory
parent_path = os.path.dirname(os.getcwd())
save_path = os.path.join(parent_path, SAVE_DIRECTORY)

os.makedirs(save_path, exist_ok=True)


# upload img to supabase
async def upload_img_supabase(upload_file, directory="image"):
    file_ext = Path(upload_file.filename).suffix.lower()
    file_name = f"{directory}/{uuid.uuid4().hex[:8]}_{upload_file.filename}"

    contents = await upload_file.read()
    res = supabase.storage.from_(SUPABASE_BUCKET).upload(file_name, contents,
                                                         {"content-type": upload_file.content_type})

    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_name}"
    #print(public_url)
    return public_url

# saving a file
async def save_upload_file(
        upload_file: UploadFile,
        pet_id: int,
        pet_name: Optional[str] = None
):
    file_ext = Path(upload_file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXT:
        raise ValueError("Archivo no permitido")

    # Crear nombre para archivo
    base_name = f"pet_{pet_id}_"

    if pet_name:
        base_name = f"{base_name}{pet_name}"
    # Naming the file
    file_name = f"{base_name}_{uuid.uuid4().hex[:8]}{file_ext}"

    # Make the path
    file_path = os.path.join(save_path, file_name)

    # save the filee
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # Close the file
    await upload_file.close()

    return file_path
