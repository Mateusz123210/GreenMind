from app import models, schemas
from app.schemas import *
from app.decorators.database import db

@db
def add_plant(plant: schemas.PlantAddSchema, db):
    db_plant = models.Plant(name = plant.name, token = plant.token, user_id = plant.user_id, latitude = plant.latitude, 
                            longtitude = plant.longtitude)
    db.add(db_plant)
    db.flush()

@db
def delete_plant(plant: models.Plant, db):
    db.delete(plant)
    db.flush()

@db
def delete_user_plants(user_plants, db):
    for plant in user_plants:
        db.delete(plant)
    db.flush()

@db
def get_user_plants(user_id, db):
    return db.query(models.Plant).filter(models.Plant.user_id == user_id).all()

@db
def get_plant(token, db):
    return db.query(models.Plant).filter(models.Plant.token == token).first()

     

