from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from fastapi import HTTPException, UploadFile
from datetime import datetime
from app.models.user_plant import UserPlant
from app.models.plant import Plant
from app.utils.image_handler import save_image, delete_image, get_default_image_path
from app.utils.care_calculator import calculate_care_status, calculate_days_since, get_watering_level, get_sunfilling_level, WATERING_INTERVALS

def get_user_plant(db: Session, id: int, user_id: int) -> Optional[UserPlant]:
    """Отримати конкретну рослину користувача за id"""
    db_user_plant = db.query(UserPlant).filter(
        UserPlant.id == id, 
        UserPlant.owner_id == user_id
    ).first()
    
    if db_user_plant:
        plant_info = db.query(Plant).filter(Plant.id == db_user_plant.plant_id).first()
        if plant_info:
            db_user_plant.care_status = calculate_care_status(
                db_user_plant.last_watering,
                db_user_plant.last_sunfilling,
                plant_info.watering
            )
    
    return db_user_plant

def get_user_plants_minimal(db: Session, user_id: int) -> List[dict]:
    """Отримати всі рослини користувача у мінімальному форматі"""
    from sqlalchemy import text
    
    result = db.execute(
        text("""
        SELECT up.id, up.plant_id, up.name, up.thumbnail, up.last_watering, up.last_sunfilling,
               p.watering
        FROM user_plants up
        JOIN plants p ON up.plant_id = p.id
        WHERE up.owner_id = :owner_id
        """),
        {"owner_id": user_id}
    )
    
    rows = result.fetchall()
    
    user_plants = []
    for row in rows:
        watering_days_ago = calculate_days_since(row.last_watering)
        sunfilling_days_ago = calculate_days_since(row.last_sunfilling)
        
        watering_interval = WATERING_INTERVALS.get(row.watering, 7)
        
        watering_level = get_watering_level(watering_days_ago, watering_interval)
        sunfilling_level = get_sunfilling_level(sunfilling_days_ago)
        
        user_plants.append({
            "id": row.id,
            "plant_id": row.plant_id,
            "name": row.name,
            "thumbnail": row.thumbnail,
            "watering_level": watering_level,
            "sunfilling_level": sunfilling_level
        })
    
    return user_plants

def create_user_plant(db: Session, user_plant, user_id: int) -> UserPlant:
    """Додати рослину до колекції користувача"""
    plant = db.query(Plant).filter(Plant.id == user_plant.plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found in database")
    
    db_user_plant = UserPlant(
        plant_id=user_plant.plant_id,
        owner_id=user_id,
        name=user_plant.name,
        last_watering=user_plant.last_watering or datetime.utcnow(),
        last_sunfilling=user_plant.last_sunfilling or datetime.utcnow(),
        image=user_plant.image,
        thumbnail=user_plant.thumbnail
    )
    
    db.add(db_user_plant)
    db.commit()
    db.refresh(db_user_plant)
    return db_user_plant

def delete_user_plant(db: Session, id: int, user_id: int) -> bool:
    """Видалити рослину з колекції користувача за id"""
    db_user_plant = get_user_plant(db, id, user_id)
    if not db_user_plant:
        raise HTTPException(status_code=404, detail="User plant not found")
    
    if db_user_plant.image and db_user_plant.image != get_default_image_path()["filename"]:
        delete_image(db_user_plant.image)
    
    db.delete(db_user_plant)
    db.commit()
    return True

async def remove_plant_image(id: int, user_id: int, db: Session) -> bool:
    """Видалити зображення рослини та встановити стандартне за id рослини"""
    db_user_plant = get_user_plant(db, id, user_id)
    if not db_user_plant:
        raise HTTPException(status_code=404, detail="User plant not found")
    
    try:
        default_image = get_default_image_path()
        if db_user_plant.image and db_user_plant.image != default_image["filename"]:
            delete_image(db_user_plant.image)
        
        db_user_plant.image = default_image["filename"]
        db_user_plant.thumbnail = default_image["thumbnail"]
        db.commit()
        
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to remove image: {str(e)}")

async def create_user_plant_with_image(db: Session, plant_data: Dict, user_id: int, file: Optional[UploadFile] = None) -> UserPlant:
    """Додати рослину до колекції користувача із зображенням"""
    try:
        plant_id = plant_data.get("plant_id")
        plant = db.query(Plant).filter(Plant.id == plant_id).first()
        if not plant:
            raise HTTPException(status_code=404, detail="Plant not found in database")
        
        default_image = get_default_image_path()
        
        image_filename = default_image["filename"]
        thumbnail_filename = default_image.get("thumbnail", None)
        
        if file and hasattr(file, "filename") and file.filename:
            try:
                image_data = await save_image(file)
                if image_data:
                    image_filename = image_data["filename"]
                    thumbnail_filename = image_data.get("thumbnail", None)
            except Exception as e:
                print(f"Error saving image: {str(e)}")
        
        now = datetime.utcnow()
        db_user_plant = UserPlant(
            plant_id=plant_id,
            owner_id=user_id,
            name=plant_data.get("name"),
            last_watering=now,
            last_sunfilling=now,
            image=image_filename,
            thumbnail=thumbnail_filename
        )
        
        db.add(db_user_plant)
        db.commit()
        db.refresh(db_user_plant)
        return db_user_plant
        
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create plant with image: {str(e)}")
    
async def create_user_plant_without_image(db: Session, plant_data: Dict, user_id: int, default_image: Dict) -> UserPlant:
    """Додати рослину до колекції користувача з дефолтним зображенням"""
    try:
        plant_id = plant_data.get("plant_id")
        plant = db.query(Plant).filter(Plant.id == plant_id).first()
        if not plant:
            raise HTTPException(status_code=404, detail="Plant not found in database")
        
        now = datetime.utcnow()
        db_user_plant = UserPlant(
            plant_id=plant_id,
            owner_id=user_id,
            name=plant_data.get("name"),
            last_watering=now,
            last_sunfilling=now,
            image=default_image["filename"],
            thumbnail=default_image.get("thumbnail")
        )
        
        db.add(db_user_plant)
        db.commit()
        db.refresh(db_user_plant)
        return db_user_plant
        
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create plant with default image: {str(e)}")

def record_watering(db: Session, id: int, user_id: int) -> UserPlant:
    """Записати дату останнього поливу за id рослини"""
    db_user_plant = get_user_plant(db, id, user_id)
    if not db_user_plant:
        raise HTTPException(status_code=404, detail="User plant not found")
    
    db_user_plant.last_watering = datetime.utcnow()
    db.commit()
    db.refresh(db_user_plant)
    return db_user_plant

def record_sunfilling(db: Session, id: int, user_id: int) -> UserPlant:
    """Записати дату останнього насонечнювання за id рослини"""
    db_user_plant = get_user_plant(db, id, user_id)
    if not db_user_plant:
        raise HTTPException(status_code=404, detail="User plant not found")
    
    db_user_plant.last_sunfilling = datetime.utcnow()
    db.commit()
    db.refresh(db_user_plant)
    return db_user_plant

async def update_user_plant(db: Session, id: int, user_id: int, update_data: Dict, file: Optional[UploadFile] = None) -> UserPlant:
    """Aktualizuje dane rośliny użytkownika (nazwa, zdjęcie, id rośliny) za pomocą id"""
    db_user_plant = get_user_plant(db, id, user_id)
    if not db_user_plant:
        raise HTTPException(status_code=404, detail="User plant not found")
    
    if update_data.get("plant_id"):
        plant = db.query(Plant).filter(Plant.id == update_data.get("plant_id")).first()
        if not plant:
            raise HTTPException(status_code=404, detail="Plant not found in database")
        db_user_plant.plant_id = update_data.get("plant_id")
    
    if update_data.get("name"):
        db_user_plant.name = update_data.get("name")
    
    if file and hasattr(file, "filename") and file.filename:
        try:
            default_image = get_default_image_path()
            if db_user_plant.image and db_user_plant.image != default_image["filename"]:
                delete_image(db_user_plant.image)
            
            image_data = await save_image(file)
            if image_data:
                db_user_plant.image = image_data["filename"]
                db_user_plant.thumbnail = image_data.get("thumbnail", None)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update image: {str(e)}")
    
    try:
        db.commit()
        db.refresh(db_user_plant)
        return db_user_plant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update plant: {str(e)}")