from fastapi import HTTPException
from fastapi.responses import Response
from app import crud
from app.schemas import *
from app.decorators.plants_database_decorator import plantsDBTransactional
from app import permissions_validator
from app.generators import uuid_generator, token_generator
from app.decorators.mongo_sensors_decorator import mongo_sensors_transactional
from app.mongo_sensors_database import sensors_db_collection
import pytz
from datetime import datetime, UTC
from app.weather_kafka_controller import WeatherKafkaController

weather_kafka_controller = WeatherKafkaController()

moisture_range = (0, 100)
temperature_range = (-100, 70)
illuminance_range = (0, 100000)

@plantsDBTransactional
def get_plant(plantUUID, access_token, email):
    user_uuid = permissions_validator.check_permissions(access_token, email)
    
    plant = crud.get_plant(plantUUID)
    if plant is None:
        raise HTTPException(status_code=400, detail="Plant does not exist!")

    if plant.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access forbidden!")
    
    responseMessage = {"name": plant.name,
        "min_temperature": plant.min_temperature,
        "opt_temperature": plant.opt_temperature,
        "max_temperature": plant.max_temperature,
        "min_moisture": plant.min_moisture,
        "opt_moisture": plant.opt_moisture,
        "max_moisture": plant.max_moisture,
        "min_illuminance": plant.min_illuminance,
        "opt_illuminance": plant.opt_illuminance,
        "max_illuminance": plant.max_illuminance
        }
    
    if plant.comments is not None:
        responseMessage["comments"] = plant.comments
                                  
    return responseMessage

@plantsDBTransactional
def add_plant(data: PlantAddSchema, access_token, email):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    if len(data.name) == 0:
        raise HTTPException(status_code=400, detail="Give valid plant name!")
    
    if data.comments is not None:
        if len(data.comments) == 0:
            raise HTTPException(status_code=400, detail="Write valid comments!")
    
    if data.min_temperature > data.max_temperature:
        raise HTTPException(status_code=400, detail="Minimum temperature can not be greater than maximum temperature!")
    
    if data.min_temperature < temperature_range[0]:
        raise HTTPException(status_code=400, detail=f"Minimum temperature is out of range" + 
                            " [{temperature_range[0]}, {temperature_range[1]}]!")
    
    if data.max_temperature > temperature_range[1]:
        raise HTTPException(status_code=400, detail=f"Maximum temperature is out of range" + 
                            " [{temperature_range[0]}, {temperature_range[1]}]!")
    
    if data.opt_temperature < data.min_temperature:
        raise HTTPException(status_code=400, detail="Optimal temperature can not be less than minimum temperature!")
    
    if data.opt_temperature > data.max_temperature:
        raise HTTPException(status_code=400, detail="Optimal temperature can not be greater than maximum temperature!")
    
    if data.min_moisture > data.max_moisture:
        raise HTTPException(status_code=400, detail="Minimum moisture can not be greater than maximum moisture!")
    
    if data.min_moisture < moisture_range[0]:
        raise HTTPException(status_code=400, detail=f"Minimum moisture is out of range" + 
                            " [{moisture_range[0]}, {moisture_range[1]}]!")
    
    if data.max_moisture > moisture_range[1]:
        raise HTTPException(status_code=400, detail=f"Maximum moisture is out of range" + 
                            " [{moisture_range[0]}, {moisture_range[1]}]!")
    
    if data.opt_moisture < data.min_moisture:
        raise HTTPException(status_code=400, detail="Optimal moisture can not be less than minimum moisture!")
    
    if data.opt_moisture > data.max_moisture:
        raise HTTPException(status_code=400, detail="Optimal moisture can not be greater than maximum moisture!")
    
    if data.min_illuminance > data.max_illuminance:
        raise HTTPException(status_code=400, detail="Minimum illuminance can not be greater than maximum illuminance!")
    
    if data.min_illuminance < illuminance_range[0]:
        raise HTTPException(status_code=400, detail=f"Minimum illuminance is out of range" + 
                            " [{illuminance_range[0]}, {illuminance_range[1]}]!")
    
    if data.max_illuminance > illuminance_range[1]:
        raise HTTPException(status_code=400, detail=f"Maximum illuminance is out of range" + 
                            " [{illuminance_range[0]}, {illuminance_range[1]}]!")
    
    if data.opt_illuminance < data.min_illuminance:
        raise HTTPException(status_code=400, detail="Optimal illuminance can not be less than minimum illuminance!")
    
    if data.opt_illuminance > data.max_illuminance:
        raise HTTPException(status_code=400, detail="Optimal illuminance can not be greater than maximum illuminance!")
    
    plant = crud.get_user_plant_by_name(user_uuid, data.name)
    if plant:
        raise HTTPException(status_code=400, detail="Plant with this name currently exists!")
        
    crud.add_plant(
        data.name, data.comments, data.min_temperature, data.opt_temperature,
        data.max_temperature, data.min_temperature, data.opt_moisture,
        data.max_moisture, data.min_illuminance, data.opt_illuminance,
        data.max_illuminance, user_uuid, uuid_generator.generate_uuid()
    )
                                  
    return Response(status_code = 200)

@plantsDBTransactional
def edit_plant(data: PlantEditSchema, access_token, email):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    plant = crud.get_plant(data.plantUUID)
    if plant is None:
        raise HTTPException(status_code=400, detail="Plant with this id does not exist!")
    
    if plant.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="You do not have access to this plant!")

    edit_data = {}

    if data.name is None and data.comments is None and data.min_temperature is None and \
        data.opt_temperature is None and data.max_temperature is None and \
        data.min_moisture is None and data.opt_moisture is None and \
        data.max_moisture is None and data.min_illuminance is None and data.opt_illuminance is None and \
        data.max_illuminance is None:
        raise HTTPException(status_code=400, detail="Change minimum one parameter to update plant!")
    
    if data.name == plant.name and data.comments == plant.comments and data.min_temperature == plant.min_temperature and \
        data.opt_temperature == plant.opt_temperature and data.max_temperature == plant.max_temperature and \
        data.min_moisture == plant.min_moisture and data.opt_moisture == plant.opt_moisture and \
        data.max_moisture == plant.max_moisture and data.min_illuminance == plant.min_illuminance and \
        data.opt_illuminance == plant.opt_illuminance and data.max_illuminance == plant.max_illuminance:
        raise HTTPException(status_code=400, detail="Change minimum one parameter to update plant!")
        
    if data.name is not None:
        if len(data.name) == 0:
            raise HTTPException(status_code=400, detail="Give valid plant name!")
        edit_data["name"] = data.name
    
    if data.comments is not None:
        if len(data.comments) == 0:
            edit_data["comments"] = data.comments
    
    new_min_temperature = None
    new_opt_temperature = None
    new_max_temperature = None

    if data.min_temperature is not None:
        edit_data["min_temperature"] = data.min_temperature
        new_min_temperature = data.min_temperature
    else:
        new_min_temperature = plant.min_temperature

    if data.opt_temperature is not None:
        edit_data["opt_temperature"] = data.opt_temperature
        new_opt_temperature = data.opt_temperature
    else:
        new_opt_temperature = plant.opt_temperature

    if data.max_temperature is not None:
        edit_data["max_temperature"] = data.max_temperature
        new_max_temperature = data.max_temperature
    else:
        new_max_temperature = plant.max_temperature
    
    if new_min_temperature > new_max_temperature:
        raise HTTPException(status_code=400, detail="Minimum temperature can not be greater than maximum temperature!")
    
    if new_min_temperature < temperature_range[0]:
        raise HTTPException(status_code=400, detail=f"Minimum temperature is out of range" + 
                            " [{temperature_range[0]}, {temperature_range[1]}]!")
    
    if new_max_temperature > temperature_range[1]:
        raise HTTPException(status_code=400, detail=f"Maximum temperature is out of range" + 
                            " [{temperature_range[0]}, {temperature_range[1]}]!")
    
    if new_opt_temperature < new_min_temperature:
        raise HTTPException(status_code=400, detail="Optimal temperature can not be less than minimum temperature!")
    
    if new_opt_temperature > new_max_temperature:
        raise HTTPException(status_code=400, detail="Optimal temperature can not be greater than maximum temperature!")
    
    new_min_moisture = None
    new_opt_moisture = None
    new_max_moisture = None

    if data.min_moisture is not None:
        edit_data["min_moisture"] = data.min_moisture
        new_min_moisture = data.min_moisture
    else:
        new_min_moisture = plant.min_moisture

    if data.opt_moisture is not None:
        edit_data["opt_moisture"] = data.opt_moisture
        new_opt_moisture = data.opt_moisture
    else:
        new_opt_moisture = plant.opt_moisture

    if data.max_moisture is not None:
        edit_data["max_moisture"] = data.max_moisture
        new_max_moisture = data.max_moisture
    else:
        new_max_moisture = plant.max_moisture
    
    if new_min_moisture > new_max_moisture:
        raise HTTPException(status_code=400, detail="Minimum moisture can not be greater than maximum moisture!")
    
    if new_min_moisture < moisture_range[0]:
        raise HTTPException(status_code=400, detail=f"Minimum moisture is out of range" + 
                            " [{moisture_range[0]}, {moisture_range[1]}]!")
    
    if new_max_moisture > moisture_range[1]:
        raise HTTPException(status_code=400, detail=f"Maximum moisture is out of range" + 
                            " [{moisture_range[0]}, {moisture_range[1]}]!")
    
    if new_opt_moisture < new_min_moisture:
        raise HTTPException(status_code=400, detail="Optimal moisture can not be less than minimum moisture!")
    
    if new_opt_moisture > new_max_moisture:
        raise HTTPException(status_code=400, detail="Optimal moisture can not be greater than maximum moisture!")
    
    new_min_illuminance = None
    new_opt_illuminance = None
    new_max_illuminance = None

    if data.min_illuminance is not None:
        edit_data["min_illuminance"] = data.min_illuminance
        new_min_illuminance = data.min_illuminance
    else:
        new_min_illuminance = plant.min_illuminance

    if data.opt_illuminance is not None:
        edit_data["opt_illuminance"] = data.opt_illuminance
        new_opt_illuminance = data.opt_illuminance
    else:
        new_opt_illuminance = plant.opt_illuminance

    if data.max_illuminance is not None:
        edit_data["max_illuminance"] = data.max_illuminance
        new_max_illuminance = data.max_illuminance
    else:
        new_max_illuminance = plant.max_illuminance
    
    if new_min_illuminance > new_max_illuminance:
        raise HTTPException(status_code=400, detail="Minimum illuminance can not be greater than maximum illuminance!")
    
    if new_min_illuminance < illuminance_range[0]:
        raise HTTPException(status_code=400, detail=f"Minimum illuminance is out of range" + 
                            " [{illuminance_range[0]}, {illuminance_range[1]}]!")
    
    if new_max_illuminance > illuminance_range[1]:
        raise HTTPException(status_code=400, detail=f"Maximum illuminance is out of range" + 
                            " [{illuminance_range[0]}, {illuminance_range[1]}]!")
    
    if new_opt_illuminance < new_min_illuminance:
        raise HTTPException(status_code=400, detail="Optimal illuminance can not be less than minimum illuminance!")
    
    if new_opt_illuminance > new_max_illuminance:
        raise HTTPException(status_code=400, detail="Optimal illuminance can not be greater than maximum illuminance!")
    print(edit_data) 
    crud.edit_plant(plant.uuid, edit_data)
                                  
    return Response(status_code = 200)

@plantsDBTransactional
def delete_plant(plantUUID: str, access_token: str, email: str):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    plant = crud.get_plant(plantUUID)
    if plant is None:
        raise HTTPException(status_code=400, detail="Plant does not exist!")
    
    if plant.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="You do not have access to this plant!")
    
    plant_plantations = crud.get_plant_plantations(plant.uuid)

    if len(plant_plantations) > 0:
        raise HTTPException(status_code=403, detail="You can not delete plant, because this plant is present" + 
                            " in minimum one plantation!")

    crud.delete_plant(plant = plant)

    return Response(status_code = 200)

@plantsDBTransactional
def get_all_plants(access_token, email):
    user_uuid = permissions_validator.check_permissions(access_token, email)
    
    plants = crud.get_user_plants(user_uuid)
    if len(plants) == 0:
        return Response(status_code = 204)
    
    response_plants = []
    for plant in plants:
        response_plants.append({"name": plant.name, "uuid": plant.uuid})

    return {"plants": response_plants}

@plantsDBTransactional
def get_plantation(plantationUUID, access_token, email):
    user_uuid = permissions_validator.check_permissions(access_token, email)
    
    plantation = crud.get_plantation(plantationUUID)
    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation does not exist!")

    if plantation.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access forbidden!")

    plant_name = crud.get_plant_name(plantation.plant_id)
  
    return {
        "name": plantation.name,
        "token": plantation.token,
        "plant_name": plant_name.name,
        "latitude": plantation.latitude,
        "longtitude": plantation.longtitude
    }

@plantsDBTransactional
def add_plantation(data: PlantationAddSchema, access_token, email):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    if len(data.name) == 0:
        raise HTTPException(status_code=400, detail="Give valid plantation name!")
        
    if data.latitude < -180 or data.latitude > 180:
        raise HTTPException(status_code=400, detail="Latitude should be in range [-180, 180]!")
    
    if data.longtitude < -90 or data.longtitude > 90:
        raise HTTPException(status_code=400, detail="Longtitude should be in range [-90, 90]!")
        
    plant = crud.get_user_plant_by_uuid(user_uuid, data.plant_id)
    if plant is None:
        raise HTTPException(status_code=400, detail="Plant with this id does not exist!")
    
    plantation = crud.get_user_plantation_by_name(user_uuid, data.name)
    if plantation:
        raise HTTPException(status_code=400, detail="Plantation with this name already exists!")
    
    token = token_generator.generate_base64_token()
    
    if crud.get_plant_with_token(token) is not None:
        raise HTTPException(status_code = 500, detail="System error occured!")
        
    crud.add_plantation(
        data.name, token, user_uuid, data.plant_id,
        data.latitude, data.longtitude, uuid_generator.generate_uuid()
    )
    weather_kafka_controller.add_weather_task([data.latitude, data.longtitude])
                                  
    return Response(status_code = 200)

@plantsDBTransactional
def edit_plantation(data: PlantationEditSchema, access_token, email):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    plantation = crud.get_plantation(data.plantationUUID)

    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation with this id does not exist!")
    
    if plantation.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access forbidden!")

    if data.name is None and data.latitude is None and data.longtitude is None:
        raise HTTPException(status_code=400, detail="Change minimum one parameter to update plantation!")
    
    if data.name == plantation.name and data.latitude == plantation.latitude and data.longtitude == plantation.longtitude:
        raise HTTPException(status_code=400, detail="Change minimum one parameter to update plantation!")

    edit_data = {}

    if data.name is not None:
        if len(data.name) == 0:
            raise HTTPException(status_code=400, detail="Give valid plantation name!")
        edit_data["name"] = data.name

    if data.latitude is not None:    
        if data.latitude < -180 or data.latitude > 180:
            raise HTTPException(status_code=400, detail="Latitude should be in range [-180, 180]!")
        edit_data["latitude"] = data.latitude
    
    if data.longtitude is not None:
        if data.longtitude < -90 or data.longtitude > 90:
            raise HTTPException(status_code=400, detail="Longtitude should be in range [-90, 90]!")
        edit_data["longtitude"] = data.longtitude
                
    crud.edit_plantation(
        data.plantationUUID, edit_data
    )
                                  
    return Response(status_code = 200)

@plantsDBTransactional
def delete_plantation(plantationUUID: str, access_token: str, email: str):
    user_uuid = permissions_validator.check_permissions(access_token, email)

    plantation = crud.get_plantation(plantationUUID)
    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation does not exist!")
    
    if plantation.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="You do not have access to this plantation!")
    
    crud.delete_plantation(plantation)

    return Response(status_code = 200)

@plantsDBTransactional
def get_all_plantations(access_token, email):
    user_uuid = permissions_validator.check_permissions(access_token, email)
    
    plantations = crud.get_user_plantations(user_uuid)
    if len(plantations) == 0:
        return Response(status_code = 204)
    
    response_plantations = []
    for plantation in plantations:
        response_plantations.append({"name": plantation.name, "uuid": plantation.uuid})

    return {"plantations": response_plantations}

@plantsDBTransactional
def update_token(token, access_token, email):
    user_uuid = permissions_validator.check_permissions(access_token, email)
    
    plantation = crud.get_user_plantation_by_token(user_uuid, token)
    
    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation does not exist!")
    
    token = token_generator.generate_base64_token()

    if crud.get_plant_with_token(token) is not None:
        raise HTTPException(status_code = 500, detail="System error occured!")

    crud.update_token(plantation.uuid, token)

    return {"newToken": token}

@mongo_sensors_transactional
@plantsDBTransactional
def get_watering_info(plantationUUID, access_token, email, sensors_session):
    user_uuid = permissions_validator.check_permissions(access_token, email)
    
    plantation = crud.get_plantation(plantationUUID)
    
    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation does not exist!")
    
    if plantation.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access forbidden!")
    sensor_watering_info = []
    
    sensor = sensors_db_collection.find_one({"id": plantation.uuid}, session = sensors_session)

    if sensor:

        sensor_watering_info = sensor["watering_info"]

        if len(sensor_watering_info) == 0:
            return Response(status_code = 204)    

    return {"wateringInfo": sensor_watering_info}

@mongo_sensors_transactional
@plantsDBTransactional
def add_watering_info(data: WateringInfo, access_token, email, sensors_session):
    user_uuid = permissions_validator.check_permissions(access_token, email)
    
    plantation = crud.get_plantation(data.plantationUUID)
    
    if plantation is None:
        raise HTTPException(status_code=400, detail="Plantation does not exist!")
    
    if plantation.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access forbidden!")
    
    if data.waterAmount <= 0:
        raise HTTPException(status_code=400, detail="Water amount can not be less than 0!")
    
    if data.wateringTime < 1733913402:
        raise HTTPException(status_code=400, detail="You gave too old time!")
    
    utc=pytz.UTC
    datetime_now = datetime.now(UTC).timestamp()
    watering_time = data.wateringTime

    if watering_time > datetime_now:
        raise HTTPException(status_code=400, detail= " Giving future time is forbidden!")
    
    sensor = sensors_db_collection.find_one({"id": plantation.uuid}, session = sensors_session)

    if sensor:

        sensor_watering_info = sensor["watering_info"]

        if len(sensor_watering_info) > 100:
            del sensor_watering_info[0]

        sensor_watering_info.append([data.waterAmount, data.wateringTime])

        filter = { '_id': sensor["_id"] }
        new_values = { "$set": { 'watering_info': sensor_watering_info } }

        sensors_db_collection.update_one(filter, new_values, session=sensors_session)
    
    else:
        insert_data = {"id": plantation.uuid, "sensor_data": [], 
                           "watering_info": [[data.waterAmount, data.wateringTime]]}
        sensors_db_collection.insert_one(insert_data)
    
    return Response(status_code = 200)