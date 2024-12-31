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
def get_user_plant_by_uuid(user_uuid, uuid, plants_db):
    return plants_db.query(plants_models.PlantType).filter(plants_models.PlantType.user_id == user_uuid) \
        .filter(plants_models.PlantType.uuid == uuid) \
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

@plants_db
def get_plantation(uuid, plants_db):
    return plants_db.query(plants_models.Plant).filter(plants_models.Plant.uuid == uuid).first()

@plants_db
def get_plant_name(plant_uuid, plants_db):
    return plants_db.query(plants_models.PlantType).filter(plants_models.PlantType.uuid == plant_uuid).first()

@plants_db
def get_user_plantation_by_name(user_uuid, name, plants_db):
    return plants_db.query(plants_models.Plant).filter(plants_models.Plant.user_id == user_uuid) \
        .filter(plants_models.Plant.name == name) \
        .first()

@plants_db
def get_plant_with_token(token, plants_db):
    return plants_db.query(plants_models.Plant).filter(plants_models.Plant.token == token).first()


@plants_db
def add_plantation(name, token, user_id, plant_id,
        latitude, longtitude, uuid, plants_db):
    db_plantation = plants_models.Plant(name = name, token = token, user_id = user_id,
            plant_id = plant_id, latitude = latitude, longtitude = longtitude,
            uuid = uuid)
    plants_db.add(db_plantation)
    plants_db.flush()

@plants_db
def get_user_plantations(user_id, plants_db):
    return plants_db.query(plants_models.Plant).filter(plants_models.Plant.user_id == user_id).all()

@plants_db
def edit_plantation(plantation_uuid, edit_data, plants_db):

    plants_db.query(plants_models.Plant).filter(plants_models.Plant.uuid == plantation_uuid).update(edit_data)

    plants_db.flush()

@plants_db
def delete_plantation(plantation: plants_models.Plant, plants_db):
    plants_db.delete(plantation)
    plants_db.flush()

@plants_db
def get_user_plantation_by_token(user_uuid, token, plants_db):
    return plants_db.query(plants_models.Plant).filter(plants_models.Plant.user_id == user_uuid) \
        .filter(plants_models.Plant.token == token) \
        .first()

@plants_db
def update_token(plantation_uuid, token, plants_db):
    plants_db.query(plants_models.Plant).filter(plants_models.Plant.uuid == plantation_uuid).update({"token": token})