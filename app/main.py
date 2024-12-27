from fastapi import FastAPI
from app.plants_database import plants_engine
from app.plants_database import PlantsBase
from app.users_database import users_engine
from app.users_database import UsersBase
from app.schemas import *
from app import services
from fastapi.middleware.cors import CORSMiddleware

PlantsBase.metadata.create_all(bind=plants_engine)
UsersBase.metadata.create_all(bind=users_engine)

app = FastAPI()

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

@app.get("/prediction")
def get_prediction(plantationId: int):
    return {"plantationId": plantationId, "predictionData": {"internalConditions": ["Condition1"], "externalConditions": ["Condition2"]}}

@app.get("/sensor-data")
def get_sensor_data(plantationId: int):
    return {"plantationId": plantationId, "data": "Sample Sensor Data"}

@app.get("/statistics")
def get_statistics(plantationId: int):
    return {"plantationId": plantationId, "data": "Sample Statistics Data"}