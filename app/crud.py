from app import plants_models, users_models, schemas
from app.decorators.plants_database_decorator import plants_db
from app.decorators.users_database_decorator import users_db

@users_db
def get_user_by_email(email, users_db):
    return users_db.query(users_models.User).filter(users_models.User.email == email).first()

@users_db
def get_user_tokens(user, users_db):
    return users_db.query(users_models.Token).filter(users_models.Token.user_id == user.uuid).all()

@plants_db
def get_plant(uuid, plants_db):
    return plants_db.query(plants_models.PlantType).filter(plants_models.PlantType.uuid == uuid).first()

@plants_db
def get_user_plant_by_name(user_uuid, name, plants_db):
    return plants_db.query(plants_models.PlantType).filter(plants_models.PlantType.user_id == user_uuid) \
        .filter(plants_models.PlantType.name == name) \
        .first()

@plants_db
def add_plant(name, comments, min_temperature, opt_temperature, max_temperature, min_moisture, 
              opt_moisture, max_moisture, min_illuminance, opt_illuminance, max_illuminance,
              user_id, uuid, plants_db):
    db_plant = plants_models.PlantType(name = name, comments = comments, min_temperature = min_temperature,
            opt_temperature = opt_temperature, max_temperature = max_temperature, min_moisture = min_moisture,
            opt_moisture = opt_moisture, max_moisture = max_moisture, min_illuminance = min_illuminance,
            opt_illuminance = opt_illuminance,max_illuminance = max_illuminance, user_id = user_id, 
            uuid = uuid)
    plants_db.add(db_plant)
    plants_db.flush()

@plants_db
def edit_plant(plant_uuid, edit_data, plants_db):

    plants_db.query(plants_models.PlantType).filter(plants_models.PlantType.uuid == plant_uuid).update(edit_data)

    plants_db.flush()

@plants_db
def get_plant_plantations(plant_uuid, plants_db):
    return plants_db.query(plants_models.Plant).filter(plants_models.Plant.plant_id == plant_uuid).all()

@plants_db
def delete_plant(plant: plants_models.PlantType, plants_db):
    plants_db.delete(plant)
    plants_db.flush()

@plants_db
def get_user_plants(user_id, plants_db):
    return plants_db.query(plants_models.PlantType).filter(plants_models.PlantType.user_id == user_id).all()

# @plants_db
# def get_all_plants(plants_db):
#     return plants_db.query(plants_models.Plant).all()

# @plants_db
# def delete_plant(plant: plants_models.Plant, plants_db):
#     plants_db.delete(plant)
#     plants_db.flush()

# @plants_db
# def add_plant(plant: schemas.PlantAddSchema, plants_db):
#     db_plant = plants_models.Plant(name = plant.name, token = plant.token, user_id = plant.user_id, latitude = plant.latitude, 
#                             longtitude = plant.longtitude)
#     plants_db.add(db_plant)
#     plants_db.flush()

# @plants_db
# def delete_plant(plant: plants_models.Plant, plants_db):
#     plants_db.delete(plant)
#     plants_db.flush()

# @plants_db
# def delete_user_plants(user_plants, plants_db):
#     for plant in user_plants:
#         plants_db.delete(plant)
#     plants_db.flush()

# @plants_db
# def get_user_plants(user_id, plants_db):
#     return plants_db.query(plants_models.Plant).filter(plants_models.Plant.user_id == user_id).all()


     

