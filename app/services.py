from fastapi import HTTPException
from fastapi.responses import Response
from app import crud
from app.schemas import *
from app.decorators.database import transactional
from app.decorators.mongo_database import mongo_transactional
from app.mongo_database import collection_green_mind

@mongo_transactional
@transactional
def get_current_numbers(session):
    
    




    

    return Response(status_code=200)


@transactional
def add_plant(data: PlantAddSchema):
    
    plant = crud.get_plant(data.token)
    if plant:
        raise HTTPException(status_code=400, detail="This plant currently exists!")

    crud.add_plant(plant = data)
                                  
    return Response(status_code = 200)

@transactional
def delete_plant(data: PlantSchema):
    
    plant = crud.get_plant(data.token)
    if plant is None:
        raise HTTPException(status_code=4090, detail="This plant does not exists!")

    crud.delete_plant(plant = plant)

    return Response(status_code = 200)

@transactional
def delete_user(data: UserIDSchema):
    
    user_plants = crud.get_user_plants(user_id = data.user_id)

    if len(user_plants) == 0:
        raise HTTPException(status_code=400, detail="User has no plants!")
    
    crud.delete_user_plants(user_plants = user_plants)

    return Response(status_code = 200)