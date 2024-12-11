from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)    
    token = Column(String, nullable = False)
    user_id = Column(Integer, nullable = False)
    latitude = Column(Float, nullable = False)
    longtitude = Column(Float, nullable = False)