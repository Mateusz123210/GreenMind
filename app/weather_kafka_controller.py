import json
from app import crud
from app.decorators.database import transactional
import time
from threading import Thread
from confluent_kafka import Producer


class WeatherKafkaController:

    def __init__(self):

        self.weather_fetch_time = 360000
        self.producer = Producer({"bootstrap.servers": "20.254.227.50:9092"})
        self.working = True
        self.delivery_report = None

    def wait_for_time(self):

        counter = self.weather_fetch_time

        while self.working is True:

            if counter == self.weather_fetch_time:
                thread = Thread(name='daemon', target=self.create_tasks())
                thread.start()
                counter = 0

            else:
                counter += 1

            time.sleep(0.01)

    @transactional
    def create_tasks(self):
        
        all_plants = crud.get_all_plants()
        locations = []
        
        for plant in all_plants:
            location = [plant.latitude, plant.longtitude]

            if location not in locations:
                locations.append(location)

        for location in locations:            
            plant_localization = {"latitude": location[0], "longtitude": location[1], "time": str(time.time())}
            self.send_message(json.dumps(plant_localization).encode("utf-8"))

    def stop_creating_tasks(self):

        self.working = False
        self.producer.close()

    def send_message(self, data):

        self.producer.poll(0)

        self.producer.produce(
            "weather-fetch",
            data,
        )
