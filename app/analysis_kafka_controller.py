import json
from app import crud
from app.decorators.database import transactional
import time
from threading import Thread
from confluent_kafka import Producer


class AnalysisKafkaController:

    def __init__(self):

        self.analysis_start_time = 30000
        self.producer = Producer({"bootstrap.servers": "20.254.227.50:9092"})
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

    @transactional
    def create_tasks(self):
        
        all_plants = crud.get_all_plants()
        analysis_data = [{"message": "Here will be data for prediction"}]
        
        # for plant in all_plants:
        #     location = [plant.latitude, plant.longtitude]

        #     if location not in locations:
        #         locations.append(location)

        for data in analysis_data:            
            self.send_message(json.dumps(data).encode("utf-8"))

    def stop_creating_tasks(self):

        self.working = False
        self.producer.close()

    def send_message(self, data):

        self.producer.poll(0)

        self.producer.produce(
            "analysis-start",
            data,
        )
