import json
from app import crud
from app.decorators.database import transactional
import time
from threading import Thread
from confluent_kafka import Producer
from app.decorators.mongo_sensors_decorator import mongo_sensors_transactional
from app.decorators.mongo_weather_decorator import mongo_weather_transactional

from app.mongo_sensors_database import sensors_db_collection
from app.mongo_weather_database import weather_db_collection
from datetime import datetime, UTC, timedelta
import pytz


class AnalysisKafkaController:

    def __init__(self):

        self.analysis_start_time = 30000
        self.producer = Producer({"bootstrap.servers": "40.113.165.28:9092"})
        self.working = True
        self.delivery_report = None

    def wait_for_time(self):

        counter = self.analysis_start_time

        while self.working is True:

            if counter == self.analysis_start_time:
                thread = Thread(name='daemon', target=self.create_tasks())
                thread.start()
                counter = 0

            else:
                counter += 1

            time.sleep(0.01)

    @mongo_sensors_transactional
    @mongo_weather_transactional
    @transactional
    def create_tasks(self, sensors_session, weather_session):
        
        all_plants = crud.get_all_plants()
        for plant in all_plants:
            analysis_data = [{"plantUUID": plant.uuid, "message": "Here will be data for prediction"}]
            #download data from sensor + weather
            
            sensor = sensors_db_collection.find_one({"id": plant.uuid}, session = sensors_session)

            if sensor:
                task = {}

                sensor_data = sensor["sensor_data"]

                if len(sensor_data) == 0:
                    return 
                
                utc=pytz.UTC
                datetime_now = datetime.now(UTC)

                sensors_returned_data = []

                data_length = len(sensor_data) 

                if data_length < 60:
                    try:
                        for x in sensor_data[(-1 * data_length):]:
                            if datetime.fromtimestamp(float(x[3]))>(datetime.now() - timedelta(hours=3)):
                                sensors_returned_data.append([x[0], x[1], x[2], x[3]])
                    except ValueError:
                        pass
                else:
                    try:
                        for x in sensor_data[-60:]:
                            if datetime.fromtimestamp(float(x[3]))>(datetime.now() - timedelta(hours=3)):
                                sensors_returned_data.append([x[0], x[1], x[2], x[3]])
                    except ValueError:
                        pass
                
                if len(sensors_returned_data) == 0:
                    return
                
                task["sensors_data"] = sensors_returned_data
                 
                plant_location = (str(int(plant.latitude)) if plant.latitude.is_integer() else str(plant.latitude)) + "_" + \
                    (str(int(plant.longtitude)) if plant.longtitude.is_integer() else str(plant.longtitude))
                
                weather = weather_db_collection.find_one({"location": plant_location}, session = weather_session)

                if weather:

                    weather_data = weather["weather_data"]
            
                    if len(weather_data) == 0:
                        return 
                    
                    
                    datetime_now = datetime.now(UTC)
                    #print(weather_data[0][1])
                    last_fetch_time = datetime.fromisoformat(weather_data[0][1])
                    if last_fetch_time < datetime_now - timedelta(days=1):
                        return 

                    task["weather_data"] = weather_data[0][0]
                    
                    plant_type = crud.get_plant(plant.plant_id)
                    plant_requirements = {
                        "min_temperature": plant_type.min_temperature, 
                        "opt_temperature": plant_type.opt_temperature,
                        "max_temperature": plant_type.max_temperature,
                        "min_moisture": plant_type.min_moisture,
                        "opt_moisture": plant_type.opt_moisture,
                        "max_moisture": plant_type.max_moisture,
                        "min_illuminance": plant_type.min_illuminance,
                        "opt_illuminance": plant_type.opt_illuminance,
                        "max_illuminance": plant_type.max_illuminance
                    }
                    task["plant_requirements"] = plant_requirements
                    task["uuid"] = plant.uuid
                    self.send_message(json.dumps(task).encode("utf-8"))                    
                
                else:
                    return 

            else:
                return

    def stop_creating_tasks(self):

        self.working = False
        self.producer.close()

    def send_message(self, data):

        self.producer.poll(0)

        self.producer.produce(
            "analysis-start",
            data,
        )
