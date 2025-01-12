from kafka import KafkaConsumer
import json
from app.mongo_weather_database import weather_db_collection
from app.decorators.mongo_weather_decorator import mongo_weather_transactional
import time as tm
from datetime import datetime, UTC
from app import services
import pytz

class KafkaController:

    def __init__(self):
        self.latitude_range = (0, 100)
        self.longtitude_range = (-100, 70)
        self.illuminance_range = (0, 100000)
        self.consumer = KafkaConsumer('weather-fetch', bootstrap_servers=['40.113.165.28:9092'], 
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


    def validate(self, message: str):

        loaded = None

        try:

            loaded = json.loads(message.replace("'", '"'))

        except json.JSONDecodeError:
            return
        
        if len(loaded.keys()) != 3:
            return
        
        valid_keys = ["latitude", "longtitude", "time"] 

        for key in valid_keys:
            if key not in loaded.keys():
                return

        try:
            latitude = int(loaded["latitude"])
            longtitude = int(loaded["longtitude"])
            time = float(loaded["time"])
        
        except ValueError:
            return
        
        if latitude < self.latitude_range[0] or latitude > self.latitude_range[1] or \
            longtitude < self.longtitude_range[0] or longtitude > self.longtitude_range[1] or \
            time < 1733913402:
            return
        
        current_time = tm.time()

        if current_time > time + 3600:
            return
        weather = services.get_weather_forecast_for_hour(latitude, longtitude, datetime.now().strftime('%Y-%m-%d'))
        if weather is None:
            return
        
        self.add_to_database(latitude, longtitude, weather)


    @mongo_weather_transactional
    def add_to_database(self, latitude, longtitude, weather, session):

        db_key = str(latitude) + "_" + str(longtitude)
        weather_fetched = weather_db_collection.find_one({"location": db_key}, session=session)

        if weather_fetched:

            weather_data = weather_fetched["weather_data"]
            if (len(weather_data)>0):
                del weather_data[0]
            utc = pytz.UTC
            weather_data = [weather, str(datetime.now(UTC))]

            filter = { '_id': weather_fetched["_id"] }
            new_values = { "$set": { 'weather_data': [weather_data] } }

            weather_db_collection.update_one(filter, new_values, session=session)

        else:
            
            insert_data = {"location": db_key, "weather_data": [[weather, datetime.now(UTC)]]}
            weather_db_collection.insert_one(insert_data)
