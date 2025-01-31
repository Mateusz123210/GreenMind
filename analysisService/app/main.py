from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    pass
    thread = Thread(name='daemon', target=second_thread.consume_messsages_from_kafka)
    thread.start()

    yield

    second_thread.stop_work()
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

@app.post("/working")
async def working():
    return Response()
