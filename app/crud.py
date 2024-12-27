from app import plants_models, users_models, schemas
from app.decorators.plants_database_decorator import plants_db
from app.decorators.users_database_decorator import users_db

@plants_db
def get_all_plants(plants_db):
    return plants_db.query(plants_models.Plant).all()

@plants_db
def delete_plant(plant: plants_models.Plant, plants_db):
    plants_db.delete(plant)
    plants_db.flush()

@plants_db
def add_plant(plant: schemas.PlantAddSchema, plants_db):
    db_plant = plants_models.Plant(name = plant.name, token = plant.token, user_id = plant.user_id, latitude = plant.latitude, 
                            longtitude = plant.longtitude)
    plants_db.add(db_plant)
    plants_db.flush()

@plants_db
def delete_plant(plant: plants_models.Plant, plants_db):
    plants_db.delete(plant)
    plants_db.flush()

@plants_db
def delete_user_plants(user_plants, plants_db):
    for plant in user_plants:
        plants_db.delete(plant)
    plants_db.flush()

@plants_db
def get_user_plants(user_id, plants_db):
    return plants_db.query(plants_models.Plant).filter(plants_models.Plant.user_id == user_id).all()

@plants_db
def get_plant(token, plants_db):
    return plants_db.query(plants_models.Plant).filter(plants_models.Plant.token == token).first()

     

