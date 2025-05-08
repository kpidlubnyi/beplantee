from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.user_plant import UserPlantResponse, UserPlantListItem
from app.services.user_plant_service import (
    get_user_plants_minimal, delete_user_plant, record_watering, 
    record_sunfilling, create_user_plant_with_image, remove_plant_image,
    create_user_plant_without_image
)
from app.utils.image_handler import get_default_image_path
from app.database import get_db
from app.utils.security import get_current_user
from app.models.user import User
from app.models.user_plant import UserPlant
from app.models.plant import Plant

router = APIRouter(prefix="/user-plants", tags=["user plants"])

@router.post("/create-with-form", response_model=UserPlantResponse)
async def create_user_plant_form(
    plant_id: int = Form(...),
    name: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Створити нову рослину користувача через форму.
    Якщо зображення не надано, використовується дефолтне.
    """
    try:
        plant = db.query(Plant).filter(Plant.id == plant_id).first()
        if not plant:
            raise HTTPException(status_code=404, detail="Рослину не знайдено в базі даних")
        
        valid_file = False
        if file is not None:
            try:
                await file.seek(0)
                content = await file.read(1)
                valid_file = len(content) > 0
                await file.seek(0)
            except:
                valid_file = False
        
        plant_data = {
            "plant_id": plant_id,
            "name": name
        }
        
        if not valid_file:
            default_image = get_default_image_path()
            result = await create_user_plant_without_image(db, plant_data, current_user.id, default_image)
        else:
            result = await create_user_plant_with_image(db, plant_data, current_user.id, file)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[UserPlantListItem])
def get_all_user_plants(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Отримати всі рослини користувача у спрощеному форматі.
    """
    return get_user_plants_minimal(db, current_user.id)

@router.get("/{id}", response_model=UserPlantResponse)
def get_single_user_plant(
    id: int,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Отримати інформацію про конкретну рослину користувача за id.
    """
    plant = db.query(UserPlant).filter(
        UserPlant.id == id, 
        UserPlant.owner_id == current_user.id
    ).first()
    
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found in your collection")
    return plant

@router.delete("/{id}")
def remove_user_plant(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Видалити рослину з колекції користувача за id.
    """
    return delete_user_plant(db, id, current_user.id)

@router.post("/{id}/water", response_model=UserPlantResponse)
def water_plant(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Записати дату останнього поливу для рослини за id.
    """
    return record_watering(db, id, current_user.id)

@router.post("/{id}/sunfill", response_model=UserPlantResponse)
def sunfill_plant(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Записати дату останнього насонечнювання для рослини за id.
    """
    return record_sunfilling(db, id, current_user.id)

@router.delete("/{id}/image")
async def delete_plant_image(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Видалити зображення рослини та встановити стандартне за id.
    """
    success = await remove_plant_image(id, current_user.id, db)
    return {"success": success, "message": "Image removed and set to default"}
