from kafka import KafkaConsumer
import json
from app import crud
from app.mongo_database import collection_green_mind
from app.decorators.mongo_database import mongo_transactional
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

    def consume(self):
        
        try:
            for message in self.consumer:
                self.validate(message.value.decode('utf-8'))
                
        except Exception:
            pass

    def stop_consuming(self):
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

        self.add_to_database(token = fetched_plant.token, moisture = moisture, 
                           temperature = temperature, illuminance = illuminance, timestamp = timestamp)

    @mongo_transactional
    def add_to_database(self, token, moisture, temperature, illuminance, timestamp, session):

        sensor = collection_green_mind.find_one({"token": token}, session=session)

        if sensor:

            sensor_data = sensor["sensor_data"]

            if len(sensor_data) > self.max_measurements_number:
                del sensor_data[0]
            
            utc=pytz.UTC
            sensor_data.append([moisture, temperature, illuminance, timestamp, datetime.now(UTC)])

            filter = { '_id': sensor["_id"] }
            new_values = { "$set": { 'sensor_data': sensor_data } }

            collection_green_mind.update_one(filter, new_values, session=session)
        
        else:

            insert_data = {"token": token, "sensor_data": [[moisture, temperature, illuminance, timestamp, datetime.now(UTC)]]}
            collection_green_mind.insert_one(insert_data)