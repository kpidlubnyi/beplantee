from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.schemas.plant_type import PlantTypeBase, PlantTypeList
from app.database import get_db
from app.models.plant import Plant

router = APIRouter(prefix="/plant-types", tags=["plant types"])

@router.get("/", response_model=PlantTypeList)
def get_all_plant_types(db: Session = Depends(get_db)):
    """
    Zwraca minimalną informację o wszystkich rodzajach istniejących w bazie danych roślin.
    """
    plants = db.query(Plant).with_entities(
        Plant.id, 
        Plant.scientific_name, 
        Plant.common_name
    ).order_by(Plant.common_name, Plant.scientific_name).all()
    
    plant_list = [
        {
            "id": plant.id,
            "scientific_name": plant.scientific_name,
            "common_name": plant.common_name
        }
        for plant in plants
    ]
    
    return {"plant_types": plant_list}

@router.get("/search", response_model=PlantTypeList)
def search_plant_types(query: str, db: Session = Depends(get_db)):
    """
    Szuka rodzaj rośliny po wskazanemu imieniu (naukowe lub powszechne).
    """
    search_term = f"%{query}%"
    
    plants = db.query(Plant).with_entities(
        Plant.id, 
        Plant.scientific_name, 
        Plant.common_name
    ).filter(
        (Plant.scientific_name.ilike(search_term)) | 
        (Plant.common_name.ilike(search_term))
    ).order_by(Plant.common_name, Plant.scientific_name).all()
    
    plant_list = [
        {
            "id": plant.id,
            "scientific_name": plant.scientific_name,
            "common_name": plant.common_name
        }
        for plant in plants
    ]
    
    return {"plant_types": plant_list}
