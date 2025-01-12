from fastapi import HTTPException
from fastapi.responses import StreamingResponse
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
from datetime import datetime, timedelta, UTC
import time
import json
import pytz
from typing import Generator

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
        if len(sensor_data) < 100:
            for x in sensor_data:
                returned_data.append([x[0], x[1], x[2], x[3]])
        elif len(sensor_data) < 20161:
            reversed_data = sensor_data[::-1]
            for x in range(0, len(reversed_data), 60):
                returned_data.append([reversed_data[x][0], reversed_data[x][1], reversed_data[x][2], 
                                      reversed_data[x][3]])
        else:
            reversed_data = sensor_data[::-1][:20161]
            for x in range(0, len(reversed_data), 60):
                returned_data.append([reversed_data[x][0], reversed_data[x][1], reversed_data[x][2], 
                                      reversed_data[x][3]])

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
            returned_data.append(x[0])

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

@mongo_sensors_transactional
@plantsDBTransactional
def get_statistics(plantationUUID: str, access_token: str, email: str, sensors_session):
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
            return {"message": "There is no sensors data to generate statistics!"} 
        
        sensors_returned_data = {}

        for x in sensor_data:
            measurement_date = str(datetime.fromtimestamp(x[3]).date())

            if measurement_date not in sensors_returned_data.keys():
                sensors_returned_data[measurement_date] = [x[0], x[1], x[2], 1]

            else:
                sensors_returned_data[measurement_date] = \
                    [sensors_returned_data[measurement_date][0] + x[0], \
                     sensors_returned_data[measurement_date][1] + x[1], \
                     sensors_returned_data[measurement_date][2] + x[2], \
                     sensors_returned_data[measurement_date][3] + 1]

        returned_data = []

        for key, value in sensors_returned_data.items():
            moisture = round(value[0] / float(value[3]), 2)
            temperature = round(value[1] / float(value[3]), 2)
            illuminance = round(value[2] / float(value[3]), 2)
            returned_data.append([key, moisture, temperature, illuminance])
        
        return {"Average plant conditions by days": returned_data}

    else:

        return {"message": "There is no sensors data to generate statistics!"} 

@mongo_sensors_transactional
def get_sensors_data_from_db(plantationUUID: str, sensors_session):
    sensor = sensors_db_collection.find_one({"id": plantationUUID}, session = sensors_session)

    if sensor:

        sensor_data = sensor["sensor_data"]

        if len(sensor_data) == 0:
            return None
        
        last_values = sensor_data[-1]

        try:

            if datetime.fromtimestamp(float(last_values[3])) < (datetime.now() - timedelta(hours = 12)):
                return None

        except ValueError:
            return None

        return [last_values[0], last_values[1], last_values[2], last_values[3]]

    return None    

def sensors_stream(plantationUUID) -> Generator[str, None, None]:
    try:
        while True:
            time.sleep(10)
              
            data = get_sensors_data_from_db(plantationUUID)
            if data is None: 
                response = {"message": "No sensors data available!"}
                yield f"data: {json.dumps(response)}\n\n"
                continue
                
            yield f"data: {json.dumps(data)}\n\n"

    except GeneratorExit:
        return

def convert_to_string(obj):
    if isinstance(obj, dict):
        return {k: str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_string(item) for item in obj]
    else:
        return str(obj)
        
@mongo_weather_transactional
def get_weather_data_from_db(plantation_location: str, weather_session):

    weather = weather_db_collection.find_one({"location": plantation_location}, session = weather_session)

    if weather:

        weather_data = weather["weather_data"]
 
        if len(weather_data) == 0:
            return None

        utc = pytz.utc

        if datetime.strptime(weather_data[0][0][0]["time"], "%Y-%m-%dT%H:%M") < datetime.now() - timedelta(days = 14):
            return None   

        return convert_to_string(weather_data[0])

    return None    

def weather_stream(plantation_location) -> Generator[str, None, None]:
    try:
        while True:
            time.sleep(10)
                      
            data = get_weather_data_from_db(plantation_location)
            if data is None: 
                response = {"message": "No weather data available!"}
                yield f"data: {json.dumps(response)}\n\n"
                continue
            
            yield f"data: {json.dumps(data)}\n\n"
    
    except GeneratorExit:
        return

@mongo_predictions_transactional
def get_predictions_data_from_db(plantationUUID: str, predictions_session):

    prediction = predictions_db_collection.find_one({"id": plantationUUID}, session = predictions_session)

    if prediction:

        prediction_data = prediction["prediction_data"]

        if len(prediction_data) == 0:
            return None
        
        last_value = prediction_data[-1]
        
        utc = pytz.utc

        if utc.localize(last_value[1]) < datetime.now(UTC) - timedelta(hours = 12):

            return None

        return last_value[0]

    return None    

def predictions_stream(plantationUUID: str) -> Generator[str, None, None]:
    try:
        while True:
            time.sleep(10)
            
            data = get_predictions_data_from_db(plantationUUID)
            if data is None: 
                response = {"message": "No predictions available!"}
                yield f"data: {json.dumps(response)}\n\n"
                continue
    
            yield f"data: {json.dumps(data)}\n\n"
    except GeneratorExit:
        return

@plantsDBTransactional
def get_actual_sensors_data(plantationUUID: str, access_token: str, email: str):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    plantation = crud.get_plantation(plantationUUID)
    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation does not exist!")
    
    if plantation.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access forbidden!")
    
    return StreamingResponse(sensors_stream(plantationUUID), media_type="text/event-stream")

@plantsDBTransactional
def get_actual_weather_data(plantationUUID: str, access_token: str, email: str):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    plantation = crud.get_plantation(plantationUUID)
    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation does not exist!")

    if plantation.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access forbidden!")
    
    plantation_location = (str(int(plantation.latitude)) if plantation.latitude.is_integer() else str(plantation.latitude)) + "_" + \
            (str(int(plantation.longtitude)) if plantation.longtitude.is_integer() else str(plantation.longtitude))
    
    return StreamingResponse(weather_stream(plantation_location), media_type="text/event-stream")

@plantsDBTransactional
def get_actual_predictions_data(plantationUUID: str, access_token: str, email: str):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    plantation = crud.get_plantation(plantationUUID)
    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation does not exist!")

    if plantation.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access forbidden!")
    
    return StreamingResponse(predictions_stream(plantationUUID), media_type="text/event-stream")
    
