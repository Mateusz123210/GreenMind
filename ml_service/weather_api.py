# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 15:37:37 2024

@author: tomfi
"""

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
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,uv_index_max",
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
        uv_index = daily_data.get("uv_index_max", [])
        
        # Find the index of the requested date
        if date in dates:
            index = dates.index(date)
            return {
                "date": date,
                "max_temp": max_temps[index],
                "min_temp": min_temps[index],
                "precipitation": precipitations[index],
                "uv_index": uv_index[index]
            }
        
        # If the date is not found in the response
        return {"error": "No forecast available for the specified date."}
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
def get_weather_forecast_for_hour(location_lat, location_lon, date, hour):
    try:
        # Base URL for Open-Meteo API
        base_url = "https://api.open-meteo.com/v1/forecast"
        
        # Define query parameters
        params = {
            "latitude": location_lat,
            "longitude": location_lon,
            "start_date": date,
            "end_date": date,
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
        
        # Combine date and hour to form the target time string
        target_time = f"{date}T{hour:02d}:00"
        
        # Find the index of the requested time
        if target_time in times:
            index = times.index(target_time)
            return {
                "time": target_time,
                "temperature": temperatures[index],
                "precipitation": precipitations[index],
                "uv_index": uv_indexes[index]
            }
        
        # If the time is not found in the response
        return {"error": "No forecast available for the specified hour."}
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    
def get_historical_weather(location_lat, location_lon, date):
    """
    Fetch the historical weather data for a specific location and date using Open-Meteo API.
    
    Args:
        location_lat (float): Latitude of the location.
        location_lon (float): Longitude of the location.
        date (str): The date for the historical data in 'YYYY-MM-DD' format.
        
    Returns:
        dict: Historical weather details if successful, or an error message.
    """
    try:
        # Base URL for Open-Meteo API
        base_url = "https://api.open-meteo.com/v1/forecast"
        
        # Define query parameters
        params = {
            "latitude": location_lat,
            "longitude": location_lon,
            "start_date": date,
            "end_date": date,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,uv_index_max",
            "timezone": "auto"  # Automatically adjust timezone based on location
        }
        
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the response JSON
        weather_data = response.json()
        
        # Extract daily historical data
        daily_data = weather_data.get("daily", {})
        dates = daily_data.get("time", [])
        max_temps = daily_data.get("temperature_2m_max", [])
        min_temps = daily_data.get("temperature_2m_min", [])
        precipitations = daily_data.get("precipitation_sum", [])
        uv_indexes = daily_data.get("uv_index_max", [])
        
        # Find the index of the requested date
        if date in dates:
            index = dates.index(date)
            return {
                "date": date,
                "max_temp": max_temps[index],
                "min_temp": min_temps[index],
                "precipitation": precipitations[index],
                "uv_index": uv_indexes[index]
            }
        
        # If the date is not found in the response
        return {"error": "No historical data available for the specified date."}
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
# Example usage
if __name__ == "__main__":
    location_lat = 40.7128  # Latitude for New York City
    location_lon = -74.0060  # Longitude for New York City
    date = "2024-11-17"
    forecast = get_historical_weather(location_lat, location_lon, date)
    print(forecast)