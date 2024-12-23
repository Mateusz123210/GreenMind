from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from app.database import engine
from app.database import Base
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
from app.weather_kafka_controller import WeatherKafkaController
from app.analysis_kafka_controller import AnalysisKafkaController
from app.decorators.mongo_weather_decorator import mongo_weather_transactional
from app.mongo_weather_database import weather_db_collection
from app.decorators.mongo_sensors_decorator import mongo_sensors_transactional
from app.mongo_sensors_database import sensors_db_collection


class SecondThread:

    def __init__(self):
        self.working = True
        self.producer = WeatherKafkaController()

    def stop_work(self):
        self.producer.stop_creating_tasks()

    def work(self):    
        self.producer.wait_for_time()


class ThirdThread:

    def __init__(self):
        self.working = True
        self.producer = AnalysisKafkaController()

    def stop_work(self):
        self.producer.stop_creating_tasks()

    def work(self):
        self.producer.wait_for_time()


second_thread = SecondThread()
third_thread = ThirdThread()
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):

    thread = Thread(name='daemon', target=second_thread.work)
    thread.start()
    thread2 = Thread(name='daemon', target=third_thread.work)
    thread2.start()

    yield

    second_thread.stop_work()
    thread.join()
    third_thread.stop_work()
    thread2.join()

app = FastAPI(lifespan=lifespan)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/working")
async def working():
    return Response()