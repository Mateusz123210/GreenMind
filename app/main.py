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

@app.get("/plant")
def get_plant(plantId: int):
    return {"plantId": plantId, "data": "Sample Plant Data"}

@app.post("/plant")
def create_plant(plant: Plant):
    return {"message": "Plant created", "plant": plant}

@app.put("/plant")
def update_plant(id: int, plant: Plant):
    return {"message": "Plant updated", "id": id, "plant": plant}

@app.delete("/plant")
def delete_plant(plantId: int):
    return {"message": "Plant deleted", "plantId": plantId}

@app.get("/plants")
def get_all_plants():
    return {"plants": ["Plant1", "Plant2"]}

@app.get("/plantation")
def get_plantation(plantationId: int):
    return {"plantationId": plantationId, "data": "Sample Plantation Data"}

@app.post("/plantation")
def create_plantation(plantation: Plantation):
    return {"message": "Plantation created", "plantation": plantation}

@app.put("/plantation")
def edit_plantation(id: int, plantation: Plantation):
    return {"message": "Plantation updated", "id": id, "plantation": plantation}

@app.delete("/plantation")
def delete_plantation(plantationId: int):
    return {"message": "Plantation deleted", "plantationId": plantationId}

@app.post("/water")
def add_watering_info(watering_info: WateringInfo):
    return {"message": "Watering information added", "info": watering_info}
