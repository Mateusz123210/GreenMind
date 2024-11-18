# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from fastapi import FastAPI
import random, json
import weather_api

app=FastAPI()

@app.get("/")
async def root():
    return {"message": "GreenMind"}

@app.get("/weather")
async def weather(date: str = "", lat: float = 0, lon: float=0): 
    return weather_api.get_weather_forecast(lat, lon, date)

@app.get("/prediction")
async def water_usage_prediction():
    data = {}
    data["random"]= random.random()
    return data

