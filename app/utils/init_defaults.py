import os
import shutil
from app.config import settings
from PIL import Image

def init_default_images():
    """
    Ініціалізує дефолтні зображення при запуску сервера.
    Копіює дефолтні зображення з ресурсів у папку uploads.
    """
    os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIRECTORY, "thumbnails"), exist_ok=True)
    
    default_image_path = os.path.join(settings.UPLOAD_DIRECTORY, "default_plant.png")
    default_thumbnail_path = os.path.join(settings.UPLOAD_DIRECTORY, "thumbnails", "default_plant_thumbnail.png")
    
    if not os.path.exists(default_image_path):
        resources_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
        source_image_path = os.path.join(resources_dir, "default_plant.png")
        
        if os.path.exists(source_image_path):
            shutil.copy(source_image_path, default_image_path)
        else:
            img = Image.new('RGB', (500, 500), color=(76, 153, 93))
            img.save(default_image_path)
    
    if not os.path.exists(default_thumbnail_path):
        resources_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
        source_thumbnail_path = os.path.join(resources_dir, "default_plant_thumbnail.png")
        
        if os.path.exists(source_thumbnail_path):
            shutil.copy(source_thumbnail_path, default_thumbnail_path)
        else:
            if os.path.exists(default_image_path):
                img = Image.open(default_image_path)
                img.thumbnail((200, 200))
                img.save(default_thumbnail_path)
            else:
                img = Image.new('RGB', (200, 200), color=(76, 153, 93))
                img.save(default_thumbnail_path)

    return {
        "filename": "default_plant.png",
        "thumbnail": "thumbnails/default_plant_thumbnail.png"
    }