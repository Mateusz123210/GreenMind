import pandas as pd
import ast
import numpy as np
from datetime import datetime

from pathlib import Path



def parse_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                record = ast.literal_eval(line.strip())
                data.append({
                    'inside_temperature': record['temperature'],
                    'lighting_level': record['illuminance']
                })
            except (SyntaxError, ValueError) as e:
                print(f"Skipping invalid line: {line.strip()} - Error: {e}")
    return pd.DataFrame(data)

file_path = Path(__file__).parent / "sensor_data_24h.fakejson"
parsed_data = parse_data(file_path)

np.random.seed(42)  
parsed_data['outside_temperature'] = np.random.uniform(0, 5, len(parsed_data))
parsed_data['uv_index'] = np.random.uniform(100, 100, len(parsed_data))


print(parsed_data.head())

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error



X = parsed_data[['outside_temperature', 'uv_index']]
y = parsed_data[['inside_temperature', 'lighting_level']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")


new_data = pd.DataFrame({'outside_temperature': [25], 'uv_index': [5]})
predicted_values = model.predict(new_data)
print(f"Predicted inside_temperature and lighting_level: {predicted_values}")

def predict_indoor_hourly(datetime: datetime, outside_temperature, uv_index):
    return {
                "inside_temperature": "",
                "lighting_level": "",
            }