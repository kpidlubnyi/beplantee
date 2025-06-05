from pydantic import BaseModel
from typing import Optional

class PlantBase(BaseModel):
    common_name: Optional[str] = None
    scientific_name: str
    family: Optional[str] = None
    origin: Optional[str] = None
    type: Optional[str] = None
    dimension: Optional[str] = None
    cycle: Optional[str] = None
    watering: Optional[str] = None
    sunlight: Optional[str] = None
    pruning_month: Optional[str] = None
    poisonous_to_humans: Optional[str] = None
    poisonous_to_pets: Optional[str] = None
    description: Optional[str] = None
    watering_description: Optional[str] = None
    sunlight_description: Optional[str] = None
    pruning_description: Optional[str] = None

class PlantResponse(PlantBase):
    id: int
    
    class Config:
        from_attributes = True
        