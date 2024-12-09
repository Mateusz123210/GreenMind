from app import models, schemas
from app.schemas import *
from app.decorators.database import db

@db
def add_token(token: schemas.Token, db):
    db_token = models.Token(user_id = token.user_id, token = token.token)
    db.add(db_token)
    db.flush()

@db
def delete_token(token: models.Token, db):
    db.delete(token)
    db.flush()

@db
def delete_user_tokens(user_tokens, db):
    for token in user_tokens:
        db.delete(token)
    db.flush()

@db
def get_user_tokens(user_id, db):
    return db.query(models.Token).filter(models.Token.user_id == user_id).all()

@db
def get_token(token, db):
    return db.query(models.Token).filter(models.Token.token == token).first()

