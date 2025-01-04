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

@app.get("/api/plant")
def get_plant(plantUUID: str, access_token: str, email: str):
    return services.get_plant(plantUUID, access_token, email)

@app.post("/api/plant")
def create_plant(plant: PlantAddSchema, access_token: str, email: str):
    return services.add_plant(plant, access_token, email)

@app.put("/api/plant")
def update_plant(plant: PlantEditSchema, access_token: str, email: str):
    return services.edit_plant(plant, access_token, email)

@app.delete("/api/plant")
def delete_plant(plantUUID: str, access_token: str, email: str):
    return services.delete_plant(plantUUID, access_token, email)

@app.get("/api/plants")
def get_all_plants(access_token: str, email: str):
    return services.get_all_plants(access_token, email)

@app.get("/api/plantation")
def get_plantation(plantationUUID: str, access_token: str, email: str):
    return services.get_plantation(plantationUUID, access_token, email)

@app.post("/api/plantation")
def create_plantation(plantation: PlantationAddSchema, access_token: str, email: str):
    return services.add_plantation(plantation, access_token, email)

@app.put("/api/plantation")
def edit_plantation(plantation: PlantationEditSchema, access_token: str, email: str):
    return services.edit_plantation(plantation, access_token, email)

@app.delete("/api/plantation")
def delete_plantation(plantationUUID: str, access_token: str, email: str):
    return services.delete_plantation(plantationUUID, access_token, email)

@app.get("/api/plantations")
def get_all_plantations(access_token: str, email: str):
    return services.get_all_plantations(access_token, email)

@app.put("/api/token")
def update_token(token: str, access_token: str, email: str):
    return services.update_token(token, access_token, email)

@app.get("/api/water")
def get_watering_info(plantationUUID: str, access_token: str, email: str):
    return services.get_watering_info(plantationUUID, access_token, email)

@app.post("/api/water")
def add_watering_info(watering_info: WateringInfo, access_token: str, email: str):
    return services.add_watering_info(watering_info, access_token, email)
