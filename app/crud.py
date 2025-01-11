from app import models
from app.decorators.database import db

@db
def get_all_plants(db):
    return db.query(models.Plant).all()

@db
def get_plant(plant_uuid, db):
    return db.query(models.PlantType).filter(models.PlantType.uuid == plant_uuid).first()
     

