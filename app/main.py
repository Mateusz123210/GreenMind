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
        self.producer = KafkaController()

    def stop_work(self):
        self.producer.stop_creating_tasks()

    def work(self):
        
        self.producer.wait_for_time()


class ThirdThread:

    def __init__(self):
        self.working = True
        self.producer = KafkaController()

    def stop_work(self):
        self.producer.stop_creating_tasks()

    def work(self):
        
        self.producer.wait_for_time()


second_thread = SecondThread()
third_thread = ThirdThread()
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    pass
    thread = Thread(name='daemon', target=second_thread.work)
    thread.start()
    # thread = Thread(name='daemon', target=third_thread.fetch_weather)
    # thread.start()

    # yield
    yield

    # second_thread.stop_work()
    # thread.join()
    third_thread.stop_work()
    thread.join()

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

