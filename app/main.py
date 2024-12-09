from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.database import Base
from app.schemas import *
from app import services
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
from app.kafka_controller import KafkaController


class SecondThread:

    def __init__(self):
        self.working = True
        self.consumer = KafkaController()

    def stop_work(self):
        self.consumer.stop_consuming()

    def consume_messsages_from_kafka(self):
        
        self.consumer.consume()

second_thread = SecondThread()
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    pass
    # thread = Thread(name='daemon', target=second_thread.consume_messsages_from_kafka)
    # thread.start()

    # yield
    yield

    # second_thread.stop_work()
    # thread.join()

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

@app.get('/sensor-data')
async def get_sensor_data(data: str):
    return services.get_sensor_data(data)

