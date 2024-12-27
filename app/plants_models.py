from sqlalchemy import Column, Integer, String, Float
from app.plants_database import PlantsBase


class Plant(PlantsBase):
    __tablename__ = "plants"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)    
    token = Column(String, nullable = False, unique = True)
    user_id = Column(String, nullable = False)
    latitude = Column(Float, nullable = False)
    longtitude = Column(Float, nullable = False)
    uuid = Column(String, nullable = False, unique = True)
    