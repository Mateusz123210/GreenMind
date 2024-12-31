from pydantic import BaseModel
from typing import List


class PlantAddSchema(BaseModel):
    name: str
    comments: str | None = None
    min_temperature: float
    opt_temperature: float
    max_temperature: float
    min_moisture: float
    opt_moisture: float
    max_moisture: float
    min_illuminance: float
    opt_illuminance: float
    max_illuminance: float


    class Config:
        from_attributes = True


class PlantEditSchema(BaseModel):
    name: str | None = None
    comments: str | None = None
    min_temperature: float | None = None
    opt_temperature: float | None = None
    max_temperature: float | None = None
    min_moisture: float | None = None
    opt_moisture: float | None = None
    max_moisture: float | None = None
    min_illuminance: float | None = None
    opt_illuminance: float | None = None
    max_illuminance: float | None = None
    plantUUID: str 


    class Config:
        from_attributes = True


# class Plantation(BaseModel):
#     name: str
#     latitude: List[float] | None = None
#     longitude: List[float] | None = None
#     additionalInfo: List[List[str]] | None = None


#     class Config:
#         from_attributes = True


# class WateringInfo(BaseModel):
#     id: int
#     waterAmount: float
#     wateringTime: str


#     class Config:
#         from_attributes = True








