from pydantic import BaseModel


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













