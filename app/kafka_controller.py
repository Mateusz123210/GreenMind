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
        self.humidity_range = (0, 100)
        self.temperature_range = (-100, 70)
        self.light_range = (0, 100000)
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
        
        if len(loaded.keys()) != 4:
            return
        
        valid_keys = ["token", "humidity", "temperature", "light"] 

        for key in valid_keys:
            if key not in loaded.keys():
                return
            
        token = loaded["token"]

        fetched_token = crud.get_token(token)
        if fetched_token is None:
            return
        
        try:
            humidity = int(loaded["humidity"])
            temperature = int(loaded["temperature"])
            light = int(loaded["light"])
        
        except ValueError:
            return
        
        if humidity < self.humidity_range[0] or humidity > self.humidity_range[1] or \
            temperature < self.temperature_range[0] or temperature > self.temperature_range[1] or \
            light < self.light_range[0] or light > self.light_range[1]:
            return

        self.add_to_database(token = fetched_token.token, humidity = humidity, 
                           temperature = temperature, light = light)

    @mongo_transactional
    def add_to_database(self, token, humidity, temperature, light, session):
        sensor = collection_green_mind.find_one({"token": token}, session=session)

        if sensor:

            sensor_data = sensor["sensor_data"]

            if len(sensor_data) > self.max_measurements_number:
                del sensor_data[0]
            
            utc=pytz.UTC
            sensor_data.append([humidity, temperature, light, datetime.now(UTC)])

            filter = { '_id': sensor["_id"] }
            new_values = { "$set": { 'sensor_data': sensor_data } }

            collection_green_mind.update_one(filter, new_values, session=session)
        
        else:

            insert_data = {"token": token, "sensor_data": [[humidity, temperature, light, datetime.now(UTC)]]}
            collection_green_mind.insert_one(insert_data)