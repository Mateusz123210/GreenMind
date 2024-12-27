from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from app.plants_database import plants_engine
from app.plants_database import PlantsBase
from app.users_database import users_engine
from app.users_database import UsersBase
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
from app.old_data_remover import OldDataRemover


class SecondThread:

    def __init__(self):
        self.working = True
        self.remover = OldDataRemover()

    def stop_work(self):
        self.remover.stop_work()

    def work(self):    
        self.remover.wait_for_time()

second_thread = SecondThread()
PlantsBase.metadata.create_all(bind=plants_engine)
UsersBase.metadata.create_all(bind=users_engine)

@asynccontextmanager
async def lifespan(app: FastAPI):

    thread = Thread(name='daemon', target=second_thread.work)
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
