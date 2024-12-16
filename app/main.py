from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.database import Base
from app.schemas import *
from app import services
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
from app.kafka_controller import KafkaController
from datetime import datetime as dt
import time
from app.weather_api_fetcher import WeatherApiFetcher


class SecondThread:

    def __init__(self):
        self.working = True
        self.consumer = KafkaController()

    def stop_work(self):
        self.consumer.stop_consuming()

    def consume_messsages_from_kafka(self):
        
        self.consumer.consume()


class ThirdThread:

    def __init__(self):
        self.working = True
        self.weather_api_fetcher = WeatherApiFetcher()

    def stop_work(self):
        self.working = False

    def fetch_weather(self):
        counter = 0
        while self.working is True:
            if counter == 360000:
                thread = Thread(name='daemon', target=self.weather_api_fetcher.fetch_weather())
                thread.start()
                counter = 0
            else:
                counter += 1
            time.sleep(0.01)


second_thread = SecondThread()
third_thread = ThirdThread()
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    pass
    thread = Thread(name='daemon', target=second_thread.consume_messsages_from_kafka)
    thread.start()
    # thread = Thread(name='daemon', target=third_thread.fetch_weather)
    # thread.start()

    # yield
    yield

    second_thread.stop_work()
    thread.join()
    # third_thread.stop_work()
    # thread.join()

app = FastAPI(lifespan=lifespan)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.post("/weather-fetch")
# async def fetch_weather(latitude: float, longtitude: float):
   
   
#    date: str = ""
#    lat: float = 0
#    lon: float=0
    # a = dt.strptime(date, "%Y-%m-%d").date()
    # b = _date.today()
    # print(b)
    # if(a<b):
    #     return weather_api.get_historical_weather(lat, lon, date)
    # else:
    #     return weather_api.get_weather_forecast(lat, lon, date)




# @app.get("/weather")
# async def weather(date: str = "", lat: float = 0, lon: float=0):
#     a = dt.strptime(date, "%Y-%m-%d").date()
#     b = _date.today()
#     print(b)
#     if(a<b):
#         return weather_api.get_historical_weather(lat, lon, date)
#     else:
#         return weather_api.get_weather_forecast(lat, lon, date)

# @app.get("/prediction")
# async def indoor_coonditions_prediction(datetime, outside_temperature, uv_index):
#     return pred.predict_indoor_hourly(datetime, outside_temperature, uv_index)

