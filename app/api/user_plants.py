from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.user_plant import UserPlantResponse, UserPlantListItem
from app.services.user_plant_service import (
    get_user_plants_minimal, delete_user_plant, record_watering, 
    record_sunfilling, create_user_plant_with_image, remove_plant_image,
    create_user_plant_without_image, update_user_plant
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
    Utworzyć nową roślinę użytkownika za pomocą formularza.
    Jeśli zdjęcie nie podane, używamy standardowego.
    """
    try:
        if len(name) > 20:
            raise HTTPException(status_code=400, detail="Plant name cannot exceed 20 characters")
            
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
    Otrzymać wszystkie rośliny użytkownika w sproszczonym formacie.
    """
    return get_user_plants_minimal(db, current_user.id)

@router.get("/{id}", response_model=UserPlantResponse)
def get_single_user_plant(
    id: int,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Otrzymać informację o konkretnej roślinie użytkownika po id.
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
    Usunąć roślinę z kolekcji użytkownika po id.
    """
    return delete_user_plant(db, id, current_user.id)

@router.post("/{id}/water", response_model=UserPlantResponse)
def water_plant(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Zapisać datę ostatniego podlewu rośliny po id.
    """
    return record_watering(db, id, current_user.id)

@router.post("/{id}/sunfill", response_model=UserPlantResponse)
def sunfill_plant(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Zapisać datę ostatniego sunfillingu dla rośliny po id.
    """
    return record_sunfilling(db, id, current_user.id)

@router.delete("/{id}/image")
async def delete_plant_image(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Usunąć zdjęcie rośliny po id i ustawić standardowe 
    """
    success = await remove_plant_image(id, current_user.id, db)
    return {"success": success, "message": "Image removed and set to default"}

@router.patch("/{id}", response_model=UserPlantResponse)
async def update_user_plant_endpoint(
    id: int,
    name: Optional[str] = Form(None),
    plant_id: Optional[int] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Aktualizuje istniejącą roślinę użytkownika.
    Można zmienić nazwę, rodzaj rośliny lub dodać nowe zdjęcie.
    """
    try:
        if not any([name, plant_id, file]):
            raise HTTPException(
                status_code=400, 
                detail="At least one of the fields (name, plant_id, file) must be provided"
            )
        
        update_data = {}
        if name:
            update_data["name"] = name
        if plant_id:
            update_data["plant_id"] = plant_id
        
        valid_file = False
        if file is not None:
            try:
                await file.seek(0)
                content = await file.read(1)
                valid_file = len(content) > 0
                await file.seek(0)
            except:
                valid_file = False
        
        result = await update_user_plant(db, id, current_user.id, update_data, file if valid_file else None)
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))