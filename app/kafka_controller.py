from kafka import KafkaConsumer
import json
from datetime import datetime, UTC
import pytz
from app.decorators.mongo_predictions_decorator import mongo_predictions_transactional
from app.mongo_predictions_database import predictions_db_collection
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import sklearn
import os
from app.prediction_service import average_moisture, predict_moisture_drop




class KafkaController:

    def __init__(self):

        self.consumer = KafkaConsumer('analysis-start', bootstrap_servers=['40.113.165.28:9092'], 
                         auto_offset_reset='earliest', group_id = "group1")

    def consume(self):
        
        try:
            for message in self.consumer:
                self.handle_task(message.value.decode('utf-8'))
                
        except Exception:
            pass

    def stop_consuming(self):
        self.consumer.close()


    def handle_task(self, message: str):
        print('aaa')
        loaded = None

        try:

            loaded = json.loads(message.replace("'", '"'))
                
        except json.JSONDecodeError:
            return
        
        #print(loaded)
        #print(loaded["uuid"])
        
        weather_data=loaded['weather_data']
        # Convert weather data to a DataFrame
        weather_df = pd.DataFrame(weather_data)
        weather_df=weather_df.rename(columns={"temperature": "temperature_2m", "time": "hour"})
        opt_moisture_level =loaded['plant_requirements']['opt_moisture']
        # Example usage:
        sensors_data= loaded['sensors_data']
        start_moisture_level = average_moisture(sensors_data)
        print(f"Average of first positions: {start_moisture_level}")
        try:
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

            with open(os.path.join(__location__, 'model.pkl'), 'rb') as model_file:
                model_pipeline = pickle.load(model_file)

            
            result = predict_moisture_drop(model_pipeline, weather_df, start_moisture_level, opt_moisture_level)
            print(result)
            new_prediction_data={}
            new_prediction_data["predicted_watering_time"] = result
        except Exception as e:
            print(e)
            return 

        self.save_to_database(id = loaded["uuid"], new_prediction_data = new_prediction_data)

    @mongo_predictions_transactional
    def save_to_database(self, id, new_prediction_data, session):
        prediction = predictions_db_collection.find_one({"id": id}, session=session)

        if prediction:

            prediction_data = prediction["prediction_data"]

            if len(prediction_data) > 0:
                del prediction_data[0]
            
            utc=pytz.UTC
            prediction_data = [[new_prediction_data, datetime.now(UTC)]]

            filter = { '_id': prediction["_id"] }
            new_values = { "$set": { 'prediction_data': prediction_data } }

            predictions_db_collection.update_one(filter, new_values, session=session)
        
        else:
            utc=pytz.UTC
            insert_data = {"id": id, "prediction_data": [[new_prediction_data, datetime.now(UTC)]]}
            predictions_db_collection.insert_one(insert_data)