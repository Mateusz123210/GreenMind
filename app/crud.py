from app import models, schemas
from app.schemas import *
from app.decorators.database import db

@db
def get_all_plants(db):
    return db.query(models.Plant).all()

     

