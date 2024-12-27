from app import plants_models, users_models
from app.decorators.plants_database_decorator import plants_db
from app.decorators.users_database_decorator import users_db

@plants_db
def get_all_plants(plants_db):
    return plants_db.query(plants_models.Plant).all()

@plants_db
def delete_plant(plant: plants_models.Plant, plants_db):
    plants_db.delete(plant)
    plants_db.flush()

@users_db
def get_all_users(users_db):
    return users_db.query(users_models.User).all()     