from fastapi import HTTPException
from fastapi.responses import Response
from app import crud
from app.schemas import *
from app.decorators.database import transactional
from app.decorators.mongo_database import mongo_transactional
from app.mongo_database import collection_green_mind

import requests

def get_weather_forecast(location_lat, location_lon, date):
    """
    Fetch the weather forecast for a specific location and date using Open-Meteo API.
    
    Args:
        location_lat (float): Latitude of the location.
        location_lon (float): Longitude of the location.
        date (str): The date for the forecast in 'YYYY-MM-DD' format.
        
    Returns:
        dict: Weather forecast details if successful, or an error message.
    """
    try:
        # Base URL for Open-Meteo API
        base_url = "https://api.open-meteo.com/v1/forecast"
        
        # Define query parameters
        params = {
            "latitude": location_lat,
            "longitude": location_lon,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto"  # Automatically adjust timezone based on location
        }
        
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the response JSON
        weather_data = response.json()
        
        # Extract daily forecasts
        daily_data = weather_data.get("daily", {})
        dates = daily_data.get("time", [])
        max_temps = daily_data.get("temperature_2m_max", [])
        min_temps = daily_data.get("temperature_2m_min", [])
        precipitations = daily_data.get("precipitation_sum", [])
        
        # Find the index of the requested date
        if date in dates:
            index = dates.index(date)
            return {
                "date": date,
                "max_temp": max_temps[index],
                "min_temp": min_temps[index],
                "precipitation": precipitations[index]
            }
        
        # If the date is not found in the response
        return {"error": "No forecast available for the specified date."}
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}