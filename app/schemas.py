from pydantic import BaseModel
from typing import List


class UserIDSchema(BaseModel):
    user_id: int


    class Config:
        from_attributes = True


class PlantSchema(UserIDSchema):
    token: str
    

    class Config:
        from_attributes = True


class PlantAddSchema(PlantSchema):
    name : str 
    latitude: float
    longtitude: float
    

    class Config:
        from_attributes = True


class PlantParameters(BaseModel):
    temperature: List[float]
    illuminance: List[float]
    moisture: List[float]


    class Config:
        from_attributes = True


class Plant(BaseModel):
    name: str
    comments: List[str] | None = None
    plantParameters: PlantParameters


    class Config:
        from_attributes = True


class Plantation(BaseModel):
    name: str
    latitude: List[float] | None = None
    longitude: List[float] | None = None
    additionalInfo: List[List[str]] | None = None


    class Config:
        from_attributes = True


class WateringInfo(BaseModel):
    id: int
    waterAmount: float
    wateringTime: str
    

    class Config:
        from_attributes = True








