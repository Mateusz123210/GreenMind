import json
from confluent_kafka import Producer
import time

class WeatherKafkaController:

    def __init__(self):

        self.weather_fetch_time = 360000
        self.producer = Producer({"bootstrap.servers": "20.215.41.25:9092"})
        self.working = True
        self.delivery_report = None

    def add_weather_task(self, location):
     
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