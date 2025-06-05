from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class UserPlant(Base):
    __tablename__ = "user_plants"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(20), nullable=False)
    last_watering = Column(DateTime, nullable=False)
    last_sunfilling = Column(DateTime, nullable=False)
    image = Column(Text, nullable=False)
    thumbnail = Column(Text, nullable=False)
    
    owner = relationship("User", back_populates="plants")
    plant = relationship("Plant")