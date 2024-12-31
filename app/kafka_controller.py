from kafka import KafkaConsumer
import json
from app import crud
from app.mongo_sensors_database import sensors_db_collection
from app.decorators.mongo_sensors_decorator import mongo_sensors_transactional
from app.decorators.database import transactional
from datetime import datetime, UTC
import pytz

class KafkaController:

    def __init__(self):
        self.moisture_range = (0, 100)
        self.temperature_range = (-100, 70)
        self.illuminance_range = (0, 100000)
        self.max_measurements_number = 527040 #60 x 24 x 366
        self.consumer = KafkaConsumer('plants-info', bootstrap_servers=['20.254.227.50:9092'], 
                         auto_offset_reset='earliest', group_id = "group1")
        self.consuming = True

    def consume(self):

        while self.consuming is True:
            message = self.consumer.poll(timeout_ms=1000, max_records=1) 

            if message:  
                for msg in message.values():
                    for m in msg:

                        try:
                            self.validate(m.value.decode('utf-8'))

                        except Exception:
                            pass

    def stop_consuming(self):
        self.consuming = False
        self.consumer.close()

    @transactional
    def validate(self, message: str):

        loaded = None

        try:

            loaded = json.loads(message.replace("'", '"'))

        except json.JSONDecodeError:
            return
        
        if len(loaded.keys()) != 5:
            return
        
        valid_keys = ["token", "timestamp", "temperature", "illuminance", "moisture"] 

        for key in valid_keys:
            if key not in loaded.keys():
                return
            
        token = loaded["token"]

        fetched_plant = crud.get_plant(token)
        if fetched_plant is None:
            return
        
        try:
            moisture = int(loaded["moisture"])
            temperature = int(loaded["temperature"])
            illuminance = int(loaded["illuminance"])
            timestamp = float(loaded["timestamp"])
        
        except ValueError:
            return

        if moisture < self.moisture_range[0] or moisture > self.moisture_range[1] or \
            temperature < self.temperature_range[0] or temperature > self.temperature_range[1] or \
            illuminance < self.illuminance_range[0] or illuminance > self.illuminance_range[1] or \
            timestamp < 1733913402:
            return

        self.add_to_database(id = fetched_plant.uuid, moisture = moisture, 
                           temperature = temperature, illuminance = illuminance, timestamp = timestamp)

    @mongo_sensors_transactional
    def add_to_database(self, id, moisture, temperature, illuminance, timestamp, session):

        sensor = sensors_db_collection.find_one({"id": id}, session=session)

        if sensor:

            sensor_data = sensor["sensor_data"]

            if len(sensor_data) > self.max_measurements_number:
                del sensor_data[0]
            
            utc=pytz.UTC
            sensor_data.append([moisture, temperature, illuminance, timestamp, datetime.now(UTC)])

            filter = { '_id': sensor["_id"] }
            new_values = { "$set": { 'sensor_data': sensor_data } }

            sensors_db_collection.update_one(filter, new_values, session=session)
        
        else:

            insert_data = {"id": id, "sensor_data": [[moisture, temperature, illuminance, timestamp, datetime.now(UTC)]], 
                           "watering_info": []}
            sensors_db_collection.insert_one(insert_data)