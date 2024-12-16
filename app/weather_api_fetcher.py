import json
from app import crud
from app.mongo_database import collection_green_mind
from app.decorators.mongo_database import mongo_transactional
from app.decorators.database import transactional
from datetime import datetime, UTC
import pytz

class WeatherApiFetcher:

    def fetch_weather(self):
        
        all_plants = crud.get_all_plants()

        



