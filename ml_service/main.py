# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from fastapi import FastAPI
import random, json
import weather_api
from datetime import datetime as dt
from datetime import date as _date

app=FastAPI()

@app.get("/")
async def root():
    return {"message": "GreenMind ml_service"}

@app.get("/weather")
async def weather(date: str = "", lat: float = 0, lon: float=0):
    a = dt.strptime(date, "%Y-%m-%d").date()
    b = _date.today()
    print(b)
    if(a<b):
        return weather_api.get_historical_weather(lat, lon, date)
    else:
        return weather_api.get_weather_forecast(lat, lon, date)

@app.get("/prediction")
async def water_usage_prediction():
    data = {}
    data["random"]= random.random()
    return data


