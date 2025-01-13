# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 00:10:49 2025

@author: tomfi
"""

import pandas as pd
import requests
from datetime import datetime, timedelta

# Define the filenames
file_names = ["sensor_data_monstera.json", "sensor_data_3.json"]
output_file = "merged_aggregated_sensor_data.json"
water_log_file = "water_log.json"
location_lat = 51.1093
location_lon = 17.0386

# Water log data
water_log_data = [
    {"datetime": "2024-11-28 09:30", "water_added_ml": 250},
    {"datetime": "2024-12-01 20:30", "water_added_ml": 125},
    {"datetime": "2024-12-06 08:30", "water_added_ml": 250},
    {"datetime": "2024-12-16 20:30", "water_added_ml": 200}
]

# Parse the file
def parse_sensor_data(file_name):
    data = []
    with open(file_name, "r") as file:
        for line in file:
            match = re.search(r"\{'timestamp': (\d+), 'id': (\d+), 'temperature': ([\d.]+), 'illuminance': (\d+), 'moisture': (\d+)\}", line)
            if match:
                data.append({
                    "timestamp": int(match.group(1)),
                    "id": int(match.group(2)),
                    "temperature": float(match.group(3)),
                    "illuminance": int(match.group(4)),
                    "moisture": int(match.group(5)),
                })
    return data

# Convert to DataFrame
def prepare_dataframe(data):
    df = pd.DataFrame(data)
    # Convert timestamp to datetime and round down to the nearest hour
    df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
    df["hour"] = df["datetime"].dt.floor("H")
    
    # Group by hour and calculate the average
    aggregated_df = df.groupby("hour").mean().reset_index()
    aggregated_df = aggregated_df.drop(columns=["timestamp", "id"])
    return aggregated_df


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load the data from the JSON file
df = pd.read_json('merged_aggregated_sensor_data.json')

# Check the structure of the DataFrame (optional, just to verify)
print(df.head())

# Select relevant features
X = df[["temperature_2m", "precipitation", "uv_index"]]
y_temp = df["temperature"]
y_illuminance = df["illuminance"]

# Split the data into training and testing sets
X_train, X_test, y_temp_train, y_temp_test = train_test_split(X, y_temp, test_size=0.2, random_state=42)
X_train, X_test, y_illuminance_train, y_illuminance_test = train_test_split(X, y_illuminance, test_size=0.2, random_state=42)

# Initialize and train the RandomForestRegressor model for temperature prediction
model_temp = RandomForestRegressor(n_estimators=100, random_state=42)
model_temp.fit(X_train, y_temp_train)

# Predict temperature on the test set
y_temp_pred = model_temp.predict(X_test)

# Initialize and train the RandomForestRegressor model for illuminance prediction
model_illuminance = RandomForestRegressor(n_estimators=100, random_state=42)
model_illuminance.fit(X_train, y_illuminance_train)

# Predict illuminance on the test set
y_illuminance_pred = model_illuminance.predict(X_test)

# Evaluate the models using metrics like Mean Squared Error (MSE)
mse_temp = mean_squared_error(y_temp_test, y_temp_pred)
mae_temp = mean_absolute_error(y_temp_test, y_temp_pred)
r2_temp = r2_score(y_temp_test, y_temp_pred)

mse_illuminance = mean_squared_error(y_illuminance_test, y_illuminance_pred)
mae_illuminance = mean_absolute_error(y_illuminance_test, y_illuminance_pred)
r2_illuminance = r2_score(y_illuminance_test, y_illuminance_pred)

# Output results
print(f"Temperature Prediction - MSE: {mse_temp}, MAE: {mae_temp}, R²: {r2_temp}")
print(f"Illuminance Prediction - MSE: {mse_illuminance}, MAE: {mae_illuminance}, R²: {r2_illuminance}")

import pandas as pd

# Assuming the data is loaded from the 'merged_aggregated_sensor_data.json' file
df = pd.read_json('merged_aggregated_sensor_data.json')

# Calculate the percentage change of the 'moisture' column
df['moisture_pct_change'] = df['moisture'].pct_change() * 100  # Multiply by 100 to get percentage

# Display the updated DataFrame with the 'moisture_pct_change' column
print(df[['hour', 'moisture', 'moisture_pct_change']])

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load the data from the JSON file
df = pd.read_json('merged_aggregated_sensor_data.json')

# Calculate the percentage change of the 'moisture' column
df['moisture_pct_change'] = df['moisture'].pct_change() * 100  # Multiply by 100 to get percentage

# Drop the first row where 'moisture_pct_change' will be NaN
df = df.dropna(subset=['moisture_pct_change'])
df = df[df['water_added_ml'] <= 0]

# Select relevant features (temperature and illuminance) and target variable (moisture_pct_change)
X = df[['temperature', 'illuminance']]  # Features: temperature and illuminance
y = df['moisture_pct_change']           # Target: moisture_pct_change

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the RandomForestRegressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict moisture_pct_change on the test set
y_pred = model.predict(X_test)

# Evaluate the model using metrics like Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Output the results
print(f"Moisture Percentage Change Prediction - MSE: {mse}, MAE: {mae}, R²: {r2}")

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from feature_predictor import FeaturePredictor

# Step 1: Load the data from JSON
df = pd.read_json('merged_aggregated_sensor_data.json')

# Calculate moisture_pct_change (percentage change in moisture)
df['moisture_pct_change'] = df['moisture'].pct_change() * 100
df = df.dropna(subset=['moisture_pct_change'])

# Step 2: Prepare data for the first model (predict temperature and illuminance)
X_first_model = df[['temperature_2m', 'precipitation', 'uv_index']]
y_temp = df['temperature']
y_illuminance = df['illuminance']

# Step 3: Train the first model (predict temperature and illuminance)
model_temp = RandomForestRegressor(n_estimators=100, random_state=42)
model_temp.fit(X_first_model, y_temp)

model_illuminance = RandomForestRegressor(n_estimators=100, random_state=42)
model_illuminance.fit(X_first_model, y_illuminance)

# Step 4: Prepare data for the second model (predict moisture_pct_change)
X_second_model = df[['temperature', 'illuminance']]  # From the first model's predictions
y_moisture_pct_change = df['moisture_pct_change']

# Step 5: Train the second model (predict moisture_pct_change)
model_moisture_pct_change = RandomForestRegressor(n_estimators=100, random_state=42)
model_moisture_pct_change.fit(X_second_model, y_moisture_pct_change)

# Step 6: Create the pipeline with two steps
pipeline = Pipeline([
    ('feature_predictor', FeaturePredictor(temperature_model=model_temp, illuminance_model=model_illuminance)),
    ('moisture_model', model_moisture_pct_change)
])

# Step 7: Test the pipeline on the original data (excluding NaN rows for moisture_pct_change)
X_test_pipeline = df[['temperature_2m', 'precipitation', 'uv_index']].dropna()
y_test = df.loc[X_test_pipeline.index, 'moisture_pct_change']

# Step 8: Make predictions using the pipeline
y_pred_pipeline = pipeline.predict(X_test_pipeline)

# Step 9: Evaluate the model
mse = mean_squared_error(y_test, y_pred_pipeline)
mae = mean_absolute_error(y_test, y_pred_pipeline)
r2 = r2_score(y_test, y_pred_pipeline)

print(f"Moisture Percentage Change Prediction (Pipeline) - MSE: {mse}, MAE: {mae}, R²: {r2}")

# Import Pickle
import pickle

# Save the model to a file
with open('model.pkl', 'wb') as file:
    pickle.dump(pipeline, file)