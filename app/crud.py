from app import models
from app.decorators.database import db

@db
def get_plant(token, db):
    return db.query(models.Plant).filter(models.Plant.token == token).first()
