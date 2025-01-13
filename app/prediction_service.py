import sklearn
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
import pandas as pd



def average_moisture(data):
    if not data or not all(isinstance(sublist, list) and sublist for sublist in data):
        raise ValueError("Input data must be a list of non-empty lists.")

    first_positions = [sublist[0] for sublist in data]
    return sum(first_positions) / len(first_positions)


def predict_moisture_drop(model_pipeline, weather_data, start_moisture_level, min_moisture_level):  
    moisture_level = start_moisture_level
    for i, row in weather_data.iterrows():
        input_data = row[['temperature_2m', 'precipitation', 'uv_index']].values.reshape(1, -1)
        
        predicted_pct_change = model_pipeline.predict(input_data)[0]
        print(predicted_pct_change)
        
        moisture_level = moisture_level * (1 + predicted_pct_change / 100)  # Decrease moisture based on percentage drop
        
        if moisture_level < min_moisture_level:
            return row['hour']  # Assumes 'hour' column contains the timestamp
    
    return None # "Moisture level did not drop below the minimum threshold during the forecast period."