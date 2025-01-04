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

@app.get("/api/prediction")
def get_prediction(plantationUUID: str, access_token: str, email: str):
    return services.get_predictions_data(plantationUUID, access_token, email)
    
@app.get("/api/sensor-data")
def get_sensors_data(plantationUUID: str, access_token: str, email: str):
    return services.get_sensors_data(plantationUUID, access_token, email)

@app.get("/api/weather-data")
def get_weather_data(plantationUUID: str, access_token: str, email: str):
    return services.get_weather_data(plantationUUID, access_token, email)

@app.get("/api/statistics")
def get_statistics(plantationUUID: str, access_token: str, email: str):
    return services.get_statistics(plantationUUID, access_token, email)