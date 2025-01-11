import requests
from datetime import timedelta, datetime, UTC

def get_weather_forecast_for_hour(location_lat, location_lon, startdate):
    try:
        # Base URL for Open-Meteo API
        base_url = "https://api.open-meteo.com/v1/forecast"

        end_date = (datetime.strptime(startdate, "%Y-%m-%d") + timedelta(days=14)).date()
        # Define query parameters
        params = {
            "latitude": location_lat,
            "longitude": location_lon,
            "start_date": startdate,
            "end_date": end_date,
            "hourly": "temperature_2m,precipitation,uv_index",
            "timezone": "auto"  
        }
        
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the response JSON
        weather_data = response.json()
        
        # Extract daily forecasts
        hourly_data = weather_data.get("hourly", {})
        times = hourly_data.get("time", [])
        temperatures = hourly_data.get("temperature_2m", [])
        precipitations = hourly_data.get("precipitation", [])
        uv_indexes = hourly_data.get("uv_index", [])
        
        # Combine the data into a list of dictionaries
        forecast = [
            {
                "time": times[i],
                "temperature": temperatures[i],
                "precipitation": precipitations[i],
                "uv_index": uv_indexes[i]
            }
            for i in range(len(times))
        ]

        return forecast

    except requests.exceptions.RequestException as e:
        return None