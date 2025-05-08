from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.plant import Plant

def get_plant(db: Session, plant_id: int) -> Optional[Plant]:
    """Отримати рослину за її ID"""
    return db.query(Plant).filter(Plant.id == plant_id).first()

def get_plants_for_dropdown(db: Session) -> List[Dict[str, Any]]:
    """
    Отримати список рослин для випадаючого списку, використовуючи
    збережену процедуру getPlantNamesForDropdown.
    """
    from sqlalchemy import text
    
    result = db.execute(text("CALL getPlantNamesForDropdown()"))
    plants = result.fetchall()
    
    dropdown_options = []
    for plant in plants:
        if hasattr(plant, 'id') and (hasattr(plant, 'common_name') or hasattr(plant, 'scientific_name')):
            display_name = plant.common_name if plant.common_name else plant.scientific_name
            dropdown_options.append({
                "id": plant.id,
                "display_name": display_name
            })
        else:
            plant_id = plant[0] if len(plant) > 0 else None
            common_name = plant[1] if len(plant) > 1 else None
            scientific_name = plant[2] if len(plant) > 2 else None
            
            display_name = common_name if common_name else scientific_name
            if plant_id and display_name:
                dropdown_options.append({
                    "id": plant_id,
                    "display_name": display_name
                })
    
    return dropdown_options