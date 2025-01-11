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


    def handle_task(self, message: str):

        loaded = None

        try:

            loaded = json.loads(message.replace("'", '"'))
                
        except json.JSONDecodeError:
            return
        
        print(loaded)
        print(loaded["uuid"])

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