from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.schemas.plant import PlantResponse
from app.services.plant_service import get_plant, get_plants_for_dropdown
from app.database import get_db

router = APIRouter(prefix="/plants", tags=["plants"])

@router.get("/dropdown-options", response_model=List[Dict[str, Any]])
def get_plants_dropdown(db: Session = Depends(get_db)):
    """
    Otrzymać listę roślin do droplisty.
    Używa procedury getPlantNamesForDropdown.
    """
    return get_plants_for_dropdown(db)

@router.get("/{plant_id}", response_model=PlantResponse)
def read_plant(plant_id: int, db: Session = Depends(get_db)):
    """
    Otrzymać informację o konkretnej roślinie.
    """
    plant = get_plant(db, plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

