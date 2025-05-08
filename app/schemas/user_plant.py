from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.plant import PlantResponse

class CareStatus(BaseModel):
    watering_level: int
    watering_days_ago: float
    watering_interval: int
    
    sunfilling_level: int  
    sunfilling_days_ago: float 
    sunfilling_threshold: float  

class UserPlantBase(BaseModel):
    plant_id: int
    name: str = Field(..., max_length=20)
    last_watering: datetime
    last_sunfilling: datetime
    image: str
    thumbnail: str

class UserPlantListItem(BaseModel):
    id: int
    plant_id: int
    name: str
    thumbnail: str
    watering_level: Optional[int] = None
    sunfilling_level: Optional[int] = None
    
    class Config:
        from_attributes = True

class UserPlantUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=20)
    last_watering: Optional[datetime] = None
    last_sunfilling: Optional[datetime] = None
    image: Optional[str] = None
    thumbnail: Optional[str] = None

class UserPlantResponse(UserPlantBase):
    id: int
    owner_id: int
    plant: Optional[PlantResponse] = None
    care_status: Optional[CareStatus] = None
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

from app.schemas.plant import PlantResponse
UserPlantResponse.model_rebuild()