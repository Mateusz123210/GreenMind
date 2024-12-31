import time
from app.decorators.mongo_sensors_decorator import mongo_sensors_transactional
from app.decorators.mongo_weather_decorator import mongo_weather_transactional
from app.decorators.mongo_predictions_decorator import mongo_predictions_transactional
from app.decorators.plants_database_decorator import plantsDBTransactional
from app.decorators.users_database_decorator import usersDBTransactional
from app.mongo_predictions_database import predictions_db_collection
from app.mongo_sensors_database import sensors_db_collection
from app.mongo_weather_database import weather_db_collection
from app import crud


class OldDataRemover:

    def __init__(self):
        self.working = True
        self.delete_time = 6000

    def stop_work(self):
        self.working = False

    def wait_for_time(self):
        counter = self.delete_time

        while self.working is True:

            if counter == self.delete_time:
                self.delete_old_data()
                counter = 0

            else:
                counter += 1

            time.sleep(0.01)

    @plantsDBTransactional
    @usersDBTransactional
    @mongo_sensors_transactional
    @mongo_weather_transactional
    @mongo_predictions_transactional
    def delete_old_data(self, sensors_session, weather_session, predictions_session):

        all_users = crud.get_all_users()
        users_uuids = [x.uuid for x in all_users]

        all_plants = crud.get_all_plants()
        plants_uuids = []
        plants_references_to_types = []
        
        for plant in all_plants:
            plants_uuids.append(plant.uuid)
            plants_references_to_types.append(plant.plant_id)
        
        plants_references_to_types = list(set(plants_references_to_types))
        
        for index, plant in enumerate(reversed(all_plants)):
            if plant.user_id not in users_uuids:
                crud.delete_plant(plant)
                del all_plants[len(all_plants) - index - 1]
                del plants_uuids[len(all_plants) - index - 1]

        all_plants_types = crud.get_all_plants_types()
        
        for index, plant_type in enumerate(reversed(all_plants_types)):
            if plant_type.user_id not in users_uuids:
                crud.delete_plant_type(plant_type)
                del all_plants_types[len(all_plants_types) - index - 1]

        sensors_data = sensors_db_collection.find()

        to_delete = []

        for sensor in sensors_data:

            if sensor["id"] not in plants_uuids:
                to_delete.append(sensor["id"])

        for x in to_delete:
            sensors_db_collection.delete_one({"id": x})

        plants_locations = set()

        for plant in all_plants:
            plants_locations.add((str(int(plant.latitude)) if plant.latitude.is_integer() else str(plant.latitude)) + "_" + 
            (str(int(plant.longtitude)) if plant.longtitude.is_integer() else str(plant.longtitude)))

        weather_data = weather_db_collection.find()

        to_delete = []

        for weather in weather_data:

            if weather["location"] not in plants_locations:
                to_delete.append(weather["location"])

        for x in to_delete:
            weather_db_collection.delete_one({"location": x})
        
        predictions_data = predictions_db_collection.find()

        to_delete = []

        for prediction in predictions_data:

            if prediction["id"] not in plants_uuids:
                to_delete.append(prediction["id"])

        for x in to_delete:
            predictions_db_collection.delete_one({"id": x})
        