from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.plants_database import PlantsBase


class Plant(PlantsBase):
    __tablename__ = "plants"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)    
    token = Column(String, nullable = False, unique = True)
    user_id = Column(String, nullable = False)
    plant_id = Column(String, ForeignKey("plants_types.uuid"), nullable = False) 
    latitude = Column(Float, nullable = False)
    longtitude = Column(Float, nullable = False)
    uuid = Column(String, nullable = False, unique = True)

    plants_types = relationship("PlantType", back_populates="plants")


class PlantType(PlantsBase):
    __tablename__ = "plants_types"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    comments = Column(String, nullable = True)
    min_temperature = Column(Float, nullable = False)
    opt_temperature = Column(Float, nullable = False)
    max_temperature = Column(Float, nullable = False)
    min_moisture = Column(Float, nullable = False)
    opt_moisture = Column(Float, nullable = False)
    max_moisture = Column(Float, nullable = False)
    min_illuminance = Column(Float, nullable = False)
    opt_illuminance = Column(Float, nullable = False)
    max_illuminance = Column(Float, nullable = False)
    user_id = Column(String, nullable = False)
    uuid = Column(String, nullable = False, unique = True)

    plants = relationship("Plant", back_populates="plants_types")