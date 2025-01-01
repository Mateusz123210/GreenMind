from fastapi import HTTPException
from app import crud
from app.schemas import *
from app.decorators.plants_database_decorator import plantsDBTransactional
from app.decorators.mongo_sensors_decorator import mongo_sensors_transactional
from app.mongo_sensors_database import sensors_db_collection
from app.decorators.mongo_weather_decorator import mongo_weather_transactional
from app.mongo_weather_database import weather_db_collection
from app.decorators.mongo_predictions_decorator import mongo_predictions_transactional
from app.mongo_predictions_database import predictions_db_collection
from app import permissions_validator

@mongo_sensors_transactional
@plantsDBTransactional
def get_sensors_data(plantationUUID: str, access_token: str, email: str, sensors_session):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    plantation = crud.get_plantation(plantationUUID)
    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation does not exist!")

    if plantation.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access forbidden!")

    sensor = sensors_db_collection.find_one({"id": plantation.uuid}, session = sensors_session)

    if sensor:

        sensor_data = sensor["sensor_data"]

        if len(sensor_data) == 0:
            return {"message": "In system there is no measurements from sensors yet!"}  

        returned_data = []
        for x in sensor_data:
            returned_data.append([x[0], x[1], x[2], x[3]])

        return {"sensorsMeasurements": returned_data}
    
    else:
        return {"message": "In system there is no measurements from sensors yet!"} 

@mongo_weather_transactional
@plantsDBTransactional
def get_weather_data(plantationUUID: str, access_token: str, email: str, weather_session):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    plantation = crud.get_plantation(plantationUUID)
    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation does not exist!")

    if plantation.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access forbidden!")

    plantation_location = (str(int(plantation.latitude)) if plantation.latitude.is_integer() else str(plantation.latitude)) + "_" + \
            (str(int(plantation.longtitude)) if plantation.longtitude.is_integer() else str(plantation.longtitude))
    weather = weather_db_collection.find_one({"location": plantation_location}, session = weather_session)

    if weather:

        weather_data = weather["weather_data"]
 
        if len(weather_data) == 0:
            return {"message": "In system there is no weather data for your plantation location yet!"}  

        returned_data = []
        for x in weather_data:
            returned_data.append([x[0], x[1], x[2], x[3]])

        return {"weatherData": returned_data}
    
    else:
        return {"message": "In system there is no weather data for your plantation location yet!"}

@mongo_predictions_transactional
@plantsDBTransactional
def get_predictions_data(plantationUUID: str, access_token: str, email: str, predictions_session):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    plantation = crud.get_plantation(plantationUUID)
    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation does not exist!")

    if plantation.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access forbidden!")
    
    prediction = predictions_db_collection.find_one({"id": plantation.uuid}, session = predictions_session)

    if prediction:

        prediction_data = prediction["prediction_data"]

        if len(prediction_data) == 0:
            return {"message": "In system there is no predictions for your plantation yet!"}  

        returned_data = []
        for x in prediction_data:
            returned_data.append([x[0]])

        return {"predictions": returned_data}
    
    else:
        return {"message": "In system there is no predictions for your plantation yet!"} 


@mongo_predictions_transactional
@plantsDBTransactional
def get_statistics(plantationUUID: str, access_token: str, email: str, predictions_session):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    plantation = crud.get_plantation(plantationUUID)
    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation does not exist!")

    if plantation.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access forbidden!")
    
    raise HTTPException(status_code=500, detail="Not implemented yet!")