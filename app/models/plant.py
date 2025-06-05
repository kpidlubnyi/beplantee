from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Plant(Base):
    __tablename__ = "plants"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    common_name = Column(String(50), nullable=True)
    scientific_name = Column(String(100), nullable=False)
    family = Column(String(50), nullable=True)
    origin = Column(String(50), nullable=True)
    type = Column(String(50), nullable=True)
    dimension = Column(String(50), nullable=True)
    cycle = Column(String(50), nullable=True)
    watering = Column(String(50), nullable=True)
    sunlight = Column(String(50), nullable=True)
    pruning_month = Column(String(256), nullable=True)
    poisonous_to_humans = Column(String(50), nullable=True)
    poisonous_to_pets = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    watering_description = Column(Text, nullable=True)
    sunlight_description = Column(Text, nullable=True)
    pruning_description = Column(Text, nullable=True)