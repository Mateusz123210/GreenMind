from fastapi import HTTPException
from fastapi.responses import Response
from app import crud
from app.schemas import *
from app.decorators.database import transactional
from app.decorators.mongo_database import mongo_transactional
from app.mongo_database import collection_green_mind

@mongo_transactional
@transactional
def get_sensor_data(token: str, session):

    fetched_token = crud.get_token(token)
    if fetched_token is None:
        raise HTTPException(status_code=400, detail="This sensor does not exist!")

    sensor = collection_green_mind.find_one({"token": token},
                                                      session=session)
    sensor_data = sensor["sensor_data"]
    

    return sensor_data
