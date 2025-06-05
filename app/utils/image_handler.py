import os
import uuid
from fastapi import UploadFile, HTTPException
from app.config import settings
from PIL import Image, ExifTags
from io import BytesIO
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_SIZE = (1200, 1200)  
THUMBNAIL_SIZE = (300, 300)

def validate_image(file: UploadFile) -> bool:
    """Перевіряє, чи завантажений файл є зображенням"""
    valid_content_types = ["image/jpeg", "image/png", "image/gif"]
    if file.content_type not in valid_content_types:
        return False
    return True

async def optimize_image(image_content: bytes, filename: str) -> tuple:
    """
    Оптимізує зображення: змінює розмір та створює мініатюру.
    Повертає кортеж (оптимізоване_зображення, мініатюра).
    """
    try:
        img = Image.open(BytesIO(image_content))
        
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            
            exif = dict(img._getexif().items())
            
            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            pass
        
        img.thumbnail(MAX_SIZE)
        
        thumbnail = img.copy()
        thumbnail.thumbnail(THUMBNAIL_SIZE)
        
        base_name, extension = os.path.splitext(filename)
        optimized_filename = f"{base_name}{extension}"
        thumbnail_filename = f"{base_name}_thumbnail{extension}"
        
        optimized_buffer = BytesIO()
        thumbnail_buffer = BytesIO()
        
        if extension.lower() in ['.jpg', '.jpeg']:
            img.save(optimized_buffer, format='JPEG', quality=85, optimize=True)
            thumbnail.save(thumbnail_buffer, format='JPEG', quality=75, optimize=True)
        elif extension.lower() == '.png':
            img.save(optimized_buffer, format='PNG', optimize=True)
            thumbnail.save(thumbnail_buffer, format='PNG', optimize=True)
        else:
            img.save(optimized_buffer, format=img.format)
            thumbnail.save(thumbnail_buffer, format=img.format)
        
        return (
            (optimized_filename, optimized_buffer.getvalue()),
            (thumbnail_filename, thumbnail_buffer.getvalue())
        )
    
    except Exception as e:
        logger.error(f"Error optimizing image: {str(e)}")
        return None, None

async def save_image(file: UploadFile) -> dict:
    """Зберігає завантажене зображення та повертає шляхи до нього"""
    if not validate_image(file):
        raise HTTPException(status_code=400, detail="File must be a valid image (jpeg, png, gif)")
    
    os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIRECTORY, "thumbnails"), exist_ok=True)
    
    file_extension = os.path.splitext(file.filename)[1]
    unique_id = str(uuid.uuid4())
    unique_filename = f"{unique_id}{file_extension}"
    
    try:
        await file.seek(0)
        content = await file.read()
        
        (optimized_filename, optimized_content), (thumbnail_filename, thumbnail_content) = await optimize_image(content, unique_filename)
        
        if not optimized_content:
            logger.warning("Image optimization failed, saving original file")
            
            file_path = os.path.join(settings.UPLOAD_DIRECTORY, unique_filename)
            
            with open(file_path, "wb") as buffer:
                buffer.write(content)
            
            return {
                "filename": unique_filename,
                "thumbnail": None
            }
        
        optimized_path = os.path.join(settings.UPLOAD_DIRECTORY, optimized_filename)
        with open(optimized_path, "wb") as buffer:
            buffer.write(optimized_content)
        
        thumbnail_path = os.path.join(settings.UPLOAD_DIRECTORY, "thumbnails", thumbnail_filename)
        with open(thumbnail_path, "wb") as buffer:
            buffer.write(thumbnail_content)
        
        return {
            "filename": optimized_filename,
            "thumbnail": os.path.join("thumbnails", thumbnail_filename)
        }
        
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving image: {str(e)}")

def delete_image(filename: str) -> bool:
    """Видаляє зображення та його мініатюру"""
    try:
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, filename)
        
        base_name, extension = os.path.splitext(filename)
        thumbnail_filename = f"{base_name}_thumbnail{extension}"
        thumbnail_path = os.path.join(settings.UPLOAD_DIRECTORY, "thumbnails", thumbnail_filename)
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
        
        if os.path.exists(thumbnail_path) and os.path.isfile(thumbnail_path):
            os.remove(thumbnail_path)
            
        return True
    except Exception as e:
        logger.error(f"Error deleting image: {str(e)}")
        return False

def get_default_image_path() -> dict:
    """Повертає шляхи до стандартного зображення"""
    return {
        "filename": "default_plant.png",
        "thumbnail": "thumbnails/default_plant_thumbnail.png"
    }