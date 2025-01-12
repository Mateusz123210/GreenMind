from kafka import KafkaConsumer
import json
from datetime import datetime, UTC
import pytz
from app.decorators.mongo_predictions_decorator import mongo_predictions_transactional
from app.mongo_predictions_database import predictions_db_collection


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

    def average_moisture(data):
        if not data or not all(isinstance(sublist, list) and sublist for sublist in data):
          raise ValueError("Input data must be a list of non-empty lists.")

        first_positions = [sublist[0] for sublist in data]
        return sum(first_positions) / len(first_positions)


    def handle_task(self, message: str):
        print('aaa')
        loaded = None

        try:

            loaded = json.loads(message.replace("'", '"'))
                
        except json.JSONDecodeError:
            return
        
        print(loaded)
        print(loaded["uuid"])

        weather_data=loaded['weather_data']

        

        # Example usage:
        sensors_data= loaded['sensors_data']
        result = average_moisture(sensors_data)
        print(f"Average of first positions: {result}")

        new_prediction_data = {"Ile podlać": "2 litry", "kiedy": "jutro"}
        #do prediction
        #prediction=do_prediction(loaded)

        
    
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