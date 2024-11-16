from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.database import Base
from app.schemas import *
from app import services
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
import time


class SecondThread:

    def __init__(self):
        self.working = True

    def stop_work(self):
        self.working = False

    def delete_unnecessary_data_from_database(self):
        time_counter = 0
        while self.working is True:

            if time_counter >= 10000:
                time_counter = 0
                services.delete_expired_tokens()
            time_counter += 1

            time.sleep(0.01)

second_thread = SecondThread()
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):

    thread = Thread(name='daemon', target=second_thread.delete_unnecessary_data_from_database)
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

@app.post('/register')
async def register(data: Login):
    return services.register(data)

@app.post('/login')
async def login(data: Login):
    return services.login(data)

@app.post('/refresh-password')
async def refresh_password(data: Email):
    return services.refresh_password(data)

@app.post('/logout')
async def logout(access_token: str, email: str):
    return services.logout(access_token, email)

@app.post('/refresh-token')
async def refresh_token(refresh_token: str, email: str):
    return services.refresh_token(refresh_token, email)

@app.delete('/account')
async def delete_account(access_token: str, email: str):
    return services.delete_account(access_token, email)
