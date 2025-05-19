from pydantic import BaseModel
from typing import Optional, List

class PlantTypeBase(BaseModel):
    """Basic schema for plant types with minimal information"""
    id: int
    scientific_name: str
    common_name: Optional[str] = None

class PlantTypeList(BaseModel):
    """Schema for the list of plant types response"""
    plant_types: List[PlantTypeBase]
