from fastapi import HTTPException
from fastapi.responses import Response
from app import crud
from app.schemas import *
from app.decorators.plants_database_decorator import plantsDBTransactional
from app.decorators.mongo_sensors_decorator import mongo_sensors_transactional
from app.mongo_sensors_database import sensors_db_collection

@mongo_sensors_transactional
@plantsDBTransactional
def get_sensor_data(token: str, session):

    fetched_token = crud.get_token(token)
    if fetched_token is None:
        raise HTTPException(status_code=400, detail="This sensor does not exist!")

    sensor = sensors_db_collection.find_one({"token": token},
                                                      session=session)
    sensor_data = sensor["sensor_data"]
    

    return sensor_data

@plantsDBTransactional
def add_plant(data: PlantAddSchema):
    
    plant = crud.get_plant(data.token)
    if plant:
        raise HTTPException(status_code=400, detail="This plant currently exists!")

    crud.add_plant(plant = data)
                                  
    return Response(status_code = 200)

@plantsDBTransactional
def delete_plant(data: PlantSchema):
    
    plant = crud.get_plant(data.token)
    if plant is None:
        raise HTTPException(status_code=4090, detail="This plant does not exists!")

    crud.delete_plant(plant = plant)

    return Response(status_code = 200)

@plantsDBTransactional
def delete_user(data: UserIDSchema):
    
    user_plants = crud.get_user_plants(user_id = data.user_id)

    if len(user_plants) == 0:
        raise HTTPException(status_code=400, detail="User has no plants!")
    
    crud.delete_user_plants(user_plants = user_plants)

    return Response(status_code = 200)