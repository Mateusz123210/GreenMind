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
def get_plant(plantUUID: str, access_token: str, email: str):
    return services.get_plant(plantUUID, access_token, email)

@app.post("/plant")
def create_plant(plant: PlantAddSchema, access_token: str, email: str):
    return services.add_plant(plant, access_token, email)

@app.put("/plant")
def update_plant(plant: PlantEditSchema, access_token: str, email: str):
    return services.edit_plant(plant, access_token, email)

@app.delete("/plant")
def delete_plant(plantUUID: str, access_token: str, email: str):
    return services.delete_plant(plantUUID, access_token, email)

@app.get("/plants")
def get_all_plants(access_token: str, email: str):
    return services.get_all_plants(access_token, email)

# @app.get("/plantation")
# def get_plantation(plantationId: int, access_token: str, email: str):
#     return 

# @app.post("/plantation")
# def create_plantation(plantation: Plantation, access_token: str, email: str):
#     return 

# @app.put("/plantation")
# def edit_plantation(plantation: Plantation, access_token: str, email: str):
#     return

# @app.delete("/plantation")
# def delete_plantation(plantationId: int, access_token: str, email: str):
#     return 

# @app.get("/plantations")
# def get_all_plantations(access_token: str, email: str):
#     return 

# @app.post("/water")
# def add_watering_info(watering_info: WateringInfo, access_token: str, email: str):
#     return 
